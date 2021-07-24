from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

from quizzes.schema import schema

app_name = 'quizzes'

urlpatterns = [
    path(
        'graphql',
        csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))
    ),
]
