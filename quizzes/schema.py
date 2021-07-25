import graphene
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django.filter import DjangoFilterConnectionField

from .models import Quizzes, Category, Question, Answer


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name')


# in the notes this is step 9.1
class QuizzesNode(DjangoObjectType):
    class Meta:
        model = Quizzes
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
        }
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
    # alternative to list django models: DjangoListField(AnswerType)
    all_answers = graphene.List(AnswerType, id=graphene.Int())
    # Queries with Relay
    # in the notes this is step 9
    quiz = graphene.relay.Node.Field(QuizzesNode)
    all_quizzes = DjangoFilterConnectionField(QuizzesNode)

    # in the notes this is step 7
    @staticmethod
    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)

    @staticmethod
    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)


# in the notes this is step 8

# in the notes this is step 8.1
class AddCategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return AddCategoryMutation(category=category)


class UpdateCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return UpdateCategoryMutation(category=category)


class DeleteCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        category.delete()
        return None


# in the notes this is step 8.2
class Mutation(graphene.ObjectType):
    add_category = AddCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
