from django.conf.urls.defaults import *
import views as text_views
from closecommenting.feeds import LatestEntries

# TODO:
# Propose raw formats (markdown and plain text) 
urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+).html$', view=text_views.text_detail, name='closecommenting-detail'),
    url(r'^(?P<slug>[-\w]+).mdx$', view=text_views.text_detail, name='closecommenting-mdx'),
)

feeds = {
    'latest': LatestEntries, 
}

urlpatterns += patterns('django.contrib.syndication.views',
    (r'^feeds/(?P<url>.*)/$', 'feed', {'feed_dict': feeds}),
)

