import datetime as dt

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    '''
    Create a question with the given question_text, and the publication date that is *days* days
    from  now.
    '''
    time = timezone.now() + dt.timedelta(days=days)
    return Question.objects.create(question_text = question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        '''
        If no questions exist, an appropriate message is displayed.
        '''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_past_question(self):
        '''
        Questions with a past pub_date is displayed on the index page.
        '''
        create_question(question_text="Past Q.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions'], ['<Question: Past Q.>'])

    def test_future_question(self):
        '''
        Questions with a pub_date in the future aren't displayed on the index page.
        '''
        create_question(question_text="Future Q.", days=30)
        response =self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_future_and_past_question(self):
        '''
        Even if both past and future questions exist, only past questions are displayed on the index
        page.
        '''
        create_question(question_text="Future Q.", days=30)
        create_question(question_text="Past Q.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions'], ['<Question: Past Q.>'])

    def test_two_past_questions(self):
        '''
        The questions index page may display multiple questions.
        '''
        create_question(question_text="Past Q 1.", days=-5)
        create_question(question_text="Past Q 2.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions'], ['<Question: Past Q 1.>', '<Question: Past Q 2.>'])


class QuestionModelTests(TestCase):


    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently() returns False for
        questions whose pub_date is in the future.
        '''

        time = timezone.now() + dt.timedelta(days=20)
        future_q = Question(pub_date=time)

        self.assertIs(future_q.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        '''
        was_published_recently() returns False for
        questions whose pub_date is older than 1 day.
        '''

        time = timezone.now() - dt.timedelta(days=1,seconds=1)
        old_q = Question(pub_date=time)

        self.assertIs(old_q.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_question(self):
        '''
        was_published_recently() returns True for
        questions whose pub_date is within the last 1 day.
        '''

        time = timezone.now() - dt.timedelta(hours=23,minutes=59,seconds=59)
        recent_q = Question(pub_date=time)

        self.assertIs(recent_q.was_published_recently(), True)
