from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'theapp.views.home', name='home'),
    
    url(r'^api/track/(\d+)$', 'theapp.views.track_details', name='track_details'),
    url(r'^api/track/(\d+)/items$', 'theapp.views.track_items', name='track_items'),
    
    
    
    url(r'^google_signin$', 'theapp.login_handler.google_signin', name='google_signin'),
    url(r'^post_login$', 'theapp.views.post_login', name='post_login'),
    
                       
    # Examples:
    # url(r'^$', 'ontrack.views.home', name='home'),
    # url(r'^ontrack/', include('ontrack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


urlpatterns +=  patterns(
                            (r'css/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': r'C:/work/ontrack/git/ontrack/code/ontrack/html/css'}),
                            
                            (r'img/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': r'C:/work/ontrack/git/ontrack/code/ontrack/html/img'}),
                            
                            (r'js/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': r'C:/work/ontrack/git/ontrack/code/ontrack/html/js'}),
                            
                            (r'media/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': r'C:/work/ontrack/git/ontrack/code/ontrack/html/media'}),
                            
                            (r'fancybox/?(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': r'C:/work/ontrack/git/ontrack/code/ontrack/html/fancybox/'}),
                            )