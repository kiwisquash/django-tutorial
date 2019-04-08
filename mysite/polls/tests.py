import datetime as dt

from django.test import TestCase
from django.utils import timezone

from .models import Question

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
