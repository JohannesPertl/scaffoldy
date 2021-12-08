import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from . import views

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('feedback/', views.feedback, name='feedback'),
    path('create_feedback/', views.FeedbackFormView.as_view(), name='create_feedback'),
    path('only_text_feedback/', views.OnlyTextFeedbackFormView.as_view(), name='only_text_feedback'),
    path('general_feedback/', views.GeneralFeedbackFormView.as_view(), name='general_feedback'),
    path('databases_feedback/', views.DatabasesFeedbackFormView.as_view(), name='databases_feedback'),
    path('messaging_feedback/', views.MessagingFeedbackFormView.as_view(), name='messaging_feedback'),
    path('caching_feedback/', views.CachingFeedbackFormView.as_view(), name='caching_feedback'),
    path('metrics_feedback/', views.MetricsFeedbackFormView.as_view(), name='metrics_feedback'),
    path('misc_feedback/', views.MiscFeedbackFormView.as_view(), name='misc_feedback'),
    path('download_feedback/', views.DownloadFeedbackFormView.as_view(), name='download_feedback'),
    # path('ratings/', include('star_ratings.urls', namespace='ratings')),
]

urlpatterns += staticfiles_urlpatterns()
if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
