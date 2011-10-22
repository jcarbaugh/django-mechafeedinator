from mechafeedinator.models import Feed, Item, Tag, Subscription
import datetime
import feedparser

def update_feed(feed):

    now = datetime.datetime.utcnow()

    rss = feedparser.parse(feed.url)

    for entry in rss.entries:

        if not 'id' in entry:
            # log error and skip to next entry
            continue

        try:

            # update existing item, if it exists

            item = Item.objects.get(feed=feed, uid=entry.id)
            populate_item(item, entry)

        except Item.DoesNotExist:

            # otherwise create a new item and populate from entry

            item = Item(
                feed=feed,
                uid=entry.id,
                title=entry.title,
                link=entry.link,
                date_fetched=now,
            )
            populate_item(item, entry)

    feed.last_fetched = now
    feed.save()

def populate_item(item, entry):

    item.summary = entry.get('summary', '')
    item.save()

    # get item content

    item.content.delete()

    if 'content' in entry:
        for content in entry.content:
            item.content.create(
                value=content.get('value', ''),
                mimetype=content.get('type', '')
            )

    # load tags from entry

    item.tags.delete()

    if 'tags' in entry:
        for name in entry.tags:
            item.tags.create(
                name=name.term,
                item=item,
            )

    # load enclosures

    item.enclosures.delete()

    if 'enclosures' in entry:
        for enclosure in entry.enclosures:
            item.enclosures.create(
                url=enclosure.href,
                mimetype=enclosure.get('type', ''),
            )
