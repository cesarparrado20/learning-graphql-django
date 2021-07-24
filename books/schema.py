import graphene
from graphene_django import DjangoObjectType

from .models import Book


# in the notes this is step 1
class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('id', 'title', 'excerpt')


# in the notes this is step 2
class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)

    # in the notes this is step 6
    @staticmethod
    def resolve_all_books(root, info):
        return Book.objects.all()


# in the notes this is step 3
schema = graphene.Schema(query=Query)
