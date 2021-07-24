from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

from books.schema import schema

app_name = 'books'

urlpatterns = [
    # in the notes this is step 5

    # if graphiql is equal to True, it provides us with a graphical interface
    # to carry out our queries

    path(
        'graphql',
        csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))
    ),
]
