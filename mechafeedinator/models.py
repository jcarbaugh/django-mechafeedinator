from django.contrib.auth.models import User
from django.db import models
import datetime

class Feed(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    ttl = models.IntegerField(default=60)
    date_added = models.DateTimeField(auto_now_add=True)
    last_fetched = models.DateTimeField(blank=True, null=True)
    next_fetch = models.DateTimeField()

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        # do some date manipulating
        super(Feed, self).save(**kwargs)

class Item(models.Model):
    feed = models.ForeignKey(Feed, related_name="items")
    uid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    link = models.URLField(blank=True)
    summary = models.TextField(blank=True)
    author_name = models.CharField(max_length=255, blank=True)
    author_email = models.EmailField(blank=True, null=True)
    author_uri = models.URLField(blank=True, null=True)
    date_published = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    date_fetched = models.DateTimeField()

    class Meta:
        ordering = ('-date_published',)

    def __unicode__(self):
        return u"%s: %s" % (self.feed.title, self.title)


class Content(models.Model):
    item = models.ForeignKey(Item, related_name="content")
    value = models.CharField(blank=True)
    mimetype = models.CharField(max_length=128, blank=True)

    def __unicode__(self):
        return u"[%s] %s" % (self.mimetype, self.value[:30])

class Enclosure(models.Model):
    item = models.ForeignKey(Item, related_name="enclosures")
    url = models.URLField()
    mimetype = models.CharField(max_length=128, blank=True)

    def __unicode__(self):
        return self.url

class Tag(models.Model):
    item = models.ForeignKey(Item, related_name="tags")
    value = models.CharField(max_length=128)

    class Meta:
        ordering = ('value',)

    def __unicode__(self):
        return self.value

class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='subscriptions')
    feeds = models.ManyToManyField(Feed, related_name='subscriptions')

    class Meta:
        pass
