import graphene
from graphene_django import DjangoObjectType, DjangoListField

from .models import Quizzes, Category, Question, Answer


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name')


class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ('id', 'title', 'category', 'quiz')


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('title', 'quiz')


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ('question', 'answer_text')


class Query(graphene.ObjectType):
    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())
    # alternative to list django models: DjangoListField(AnswerType)

    # in the notes this is step 7
    @staticmethod
    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)

    @staticmethod
    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)


schema = graphene.Schema(query=Query)