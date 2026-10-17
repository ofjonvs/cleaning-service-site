from django.test import TestCase
from .models import Question, Response
from . import views

# Create your tests here.

class ProposalTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(prompt='Where did we meet?', answers='paris|paris france', caption='Paris!')

    def post(self, url, data):
        return self.client.post(url, data, content_type='application/json').json()

    def test_page_renders_without_answers(self):
        response = self.client.get('/celiamiamor/')
        self.assertContains(response, 'Where did we meet?')
        self.assertNotContains(response, 'paris|paris france')

    def test_flow(self):
        url = f'/celiamiamor/question/{self.question.id}'
        self.assertFalse(self.client.post(url, {'answer': 'paris'}, content_type='application/json').json()['ok'])
        self.assertFalse(self.post('/celiamiamor/name', {'first': 'someone', 'last': 'else'})['ok'])
        self.assertTrue(self.post('/celiamiamor/name', {'first': ' célia ', 'last': views.LAST_NAME.upper()})['ok'])
        self.assertFalse(self.post(url, {'answer': 'london'})['ok'])
        self.assertTrue(self.post(url, {'answer': 'Paris  France'})['ok'])
        self.post('/celiamiamor/answer', {'answer': 'yes', 'no_attempts': 7})
        self.assertEqual(Response.objects.get().no_attempts, 7)
