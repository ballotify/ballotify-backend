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
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Vote
        fields = ('choices', 'user_agent', 'ip', 'user')
        read_only_fields = ('user_agent', 'ip', 'user')

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


class ChoiceSerializer(serializers.ModelSerializer):
    vote_choices = serializers.SerializerMethodField()
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Choice
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
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('stream', 'title', 'slug', 'choices', 'modified', 'created',)

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


class QuestionDetailSerializer(QuestionSerializer):
    class Meta(QuestionSerializer.Meta):
        read_only_fields = ('stream',)
