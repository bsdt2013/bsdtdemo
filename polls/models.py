from google.appengine.ext import ndb
#import datetime
#from django.utils import timezone


class Poll(ndb.Model):
    title = ndb.StringProperty(required=True)
    pub_date = ndb.DateProperty(auto_now=True)

    #def was_published_recently(self):
    #    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(ndb.Model):
    poll = ndb.KeyProperty(kind=Poll)
    choice = ndb.StringProperty()
    votes = ndb.IntegerProperty()
