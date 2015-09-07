from django.db import transaction

from rest_framework import serializers

from questions.models import Question, Choice
from votes.models import Vote, VoteChoice
from streams.models import Stream
from ..accounts.serializers import AccountSerializer


class VoteChoiceUserSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)

    class Meta:
        model = VoteChoice
        fields = ('user', 'created')


class VoteChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteChoice
        fields = ('choice',)


class VoteSerializer(serializers.ModelSerializer):
    choices = VoteChoiceSerializer(many=True)

    class Meta:
        model = Vote
        fields = ('choices', 'user_agent', 'ip',)
        read_only_fields = ('user_agent', 'ip',)

    def validate(self, attrs):
        question = self.context['view'].get_question()
        user = self.context['request'].user

        if Vote.objects.filter(user=user, question=question).exists():
            raise serializers.ValidationError('Current user already voted for this question.')

        return attrs

    def create(self, validated_data):
        """
        Custom create method. Support nested multiple vote choices creation.

        """
        assert "choices" in validated_data

        choices_data = validated_data.pop("choices")

        vote = Vote(**validated_data)
        vote.save()

        self.create_choices(vote, choices_data)

        return vote

    def create_choices(self, vote, choices_data):
        VoteChoice.objects.bulk_create([VoteChoice(
            vote=vote,
            user_id=vote.user_id,
            **choice_data
        ) for choice_data in choices_data])


class ChoiceListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        iterable = data.all()

        view = self.context['view']
        if hasattr(view, 'get_question') and self.context['view'].get_question().is_randomized:
            iterable = iterable.order_by('?')

        return [
            self.child.to_representation(item) for item in iterable
        ]


class ChoiceSerializer(serializers.ModelSerializer):
    vote_choices = serializers.SerializerMethodField()
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        list_serializer_class = ChoiceListSerializer
        fields = ('id', 'title', 'vote_choices', 'votes_count')
        read_only_fields = ('id',)

    def get_vote_choices(self, choice):
        serializer = VoteChoiceUserSerializer(choice.vote_choices.all()[:14], many=True)
        return serializer.data

    def get_votes_count(self, choice):
        return choice.vote_choices.all().count()


class QuestionSerializer(serializers.ModelSerializer):
    stream = serializers.SlugRelatedField(queryset=Stream.objects.all(), slug_field='slug', required=False)
    slug = serializers.CharField(required=False)
    is_voted = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            'stream', 'title', 'slug', 'choices', 'modified', 'created', 'is_voted', 'is_owner', 'is_anonymous',
            'is_multiple', 'is_private', 'is_randomized'
        )
        read_only_fields = ('slug', 'modified', 'created', )

    @transaction.atomic
    def create(self, validated_data):
        """
        Custom create method. Prepare and create nested choices.

        """
        choices_data = validated_data.pop("choices", None)

        question = Question(**validated_data)
        question.save()

        self.create_choices(question, choices_data)

        return question

    def create_choices(self, question, choices_data):
        Choice.objects.bulk_create(
            [Choice(question=question, **choice_data) for choice_data in choices_data]
        )

    def get_is_voted(self, question):
        request = self.context.get("request")
        if not request.user.is_authenticated():
            return False

        return question.votes.filter(user=request.user).exists()

    def get_is_owner(self, question):
        request = self.context.get("request")
        if not request.user.is_authenticated():
            return False

        return question.user == request.user


class QuestionDetailSerializer(QuestionSerializer):
    class Meta(QuestionSerializer.Meta):
        read_only_fields = ('stream',)
