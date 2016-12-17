from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from slates import views

urlpatterns = [
    url(r'^$', views.login_page),
    url(r'^api/login$', views.do_login),
    url(r'^api/logout$', views.do_logout),
    url(r'^home$', views.home),
    url(r'^marks$', views.marks),
    url(r'^events$', views.events),
    url(r'^profile$', views.profile),
    url(r'^flash$', views.flash),
    url(r'^mcq$', views.mcq),
    url(r'^news$', views.news),
    url(r'^view$', views.view),
    url(r'^manage$', views.manage),
    url(r'^users', views.UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^messages$', views.MessageList.as_view()),
    url(r'^message/(?P<pk>[0-9]+)/$', views.MessageDetail.as_view()),
    url(r'^flashcards$', views.FlashCardList.as_view()),
    url(r'^flashcard/(?P<pk>[0-9]+)/$', views.FlashCardDetail.as_view()),
    url(r'^mcqs$', views.MCQList.as_view()),
    url(r'^mcqsets$', views.MCQSetList.as_view()),
    url(r'^mcqdetail/(?P<pk>[0-9]+)/$', views.MCQDetail.as_view()),
    url(r'^event_list$', views.EventsList.as_view()),
    url(r'^event_upload$', views.EventUpload.as_view()),
    url(r'^event/(?P<pk>[0-9]+)/$', views.EventsDetail.as_view()),
    url(r'^mark_list$', views.MarkList.as_view()),
    url(r'^mark/(?P<user_id>[0-9]+)$', views.MarkDetail.as_view()),
    url(r'^signup$', views.SchoolList.as_view())
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.EVENTS_GALLERY_PATH, document_root=settings.EVENT_ROOT)
urlpatterns += static(settings.PROFILE_IMAGE_PATH, document_root=settings.PROFILE_ROOT)

