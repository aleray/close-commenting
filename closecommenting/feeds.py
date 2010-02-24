from django.contrib.syndication.feeds import Feed
from closecommenting.models import Text


class LatestEntries(Feed):
    title = "Close Commenting"
    link = "/"
    description = "Updates on changes and additions to Close Commenting."
    feed_copyright = 'Copyright (c) 2010, Your Name. Copyleft 2010 Your Name'
    
    def items(self):
        return Text.objects.order_by('-dc_date')[:5]
    
    def item_author_name(self, item):
        return item.dc_creator
    
    # def item_pubdate(self, item):
    #     return item.dc_date
    
    def item_categories(self, item):
        return item.dc_subject
    
    def item_copyright(self, item):
        return item.dc_rights

