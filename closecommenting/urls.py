from django.conf.urls.defaults import *
import views as text_views

# TODO:
# Propose raw formats (markdown and plain text) 
urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+).html$', view=text_views.text_detail, name='text_detail'),
    url(r'^(?P<slug>[-\w]+).mdx$', view=text_views.text_detail, name='text_detail'),
)