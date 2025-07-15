# from django.urls import path
# from .views import movie_detail_page, comment_create
# from . import views

# app_name = 'detailpage'

# urlpatterns = [
#     path('<int:movie_id>/', movie_detail_page, name='movie-detail'),
#     path('<int:movie_id>/comment/', comment_create, name='comment-create'),
# ]

from django.urls import path
from .views import movie_detail,comment_create

urlpatterns = [
    #path('', movie_list, name='movie_list'),
    path('<int:movie_id>/', movie_detail, name='movie_detail'), #영화 세부정보 url 
    path('<int:movie_id>/comments/create', comment_create, name='comment_create'), #코멘트 작성 url 
]
