from django.urls import path
from .views import *

urlpatterns = [
    path('', proposal, name='proposal'),
    path('name', check_name, name='proposal_check_name'),
    path('question/<int:question_id>', check_answer, name='proposal_check_answer'),
    path('answer', final_answer, name='proposal_final_answer'),
]
