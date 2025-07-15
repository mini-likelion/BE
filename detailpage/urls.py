from django.urls import path
from .views import comment_create
from . import views

app_name = 'detailpage'

urlpatterns = [
    #path('movies/<int:movie_id>/comment/', comment_create, name='comment-create'),
    path('detailpage/<int:movie_id>/', views.movie_detail, name='movie_detail'),

]