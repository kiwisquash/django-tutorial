import datetime as dt

from django.test import TestCase
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):

    def test_fish(self):
        '''
        was_published_recently() returns False for
        questions whose pub_date is in the future.
        '''

        time = timezone.now() + dt.timedelta(days=20)
        future_q = Question(pub_date=time)

        self.assertIs(future_q.was_published_recently(), False)
# Create your tests here.
