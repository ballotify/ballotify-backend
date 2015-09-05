from rest_framework import generics

from .serializers import UserSerializer
from ..streams.serializers import StreamSerializer
from ..questions.serializers import QuestionSerializer
from accounts.models import User
from questions.models import Question
from streams.models import Stream


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve/Update authenticated user`s details.

    """
    model = User
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

user_detail_view = UserDetailView.as_view()


class UserStreamsView(generics.ListAPIView):
    """
    List authenticated user`s streams.

    """
    model = Stream
    serializer_class = StreamSerializer

    def get_queryset(self):
        return self.request.user.owned_streams.public()

user_streams_view = UserStreamsView.as_view()


class UserQuestionsView(generics.ListAPIView):
    """
    List/Create questions.

    """
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data["user"] = self.request.user
        serializer.save()

user_questions_view = UserQuestionsView.as_view()
