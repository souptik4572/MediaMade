from django.urls import path

from .views import (delete_existing_media, get_all_medias_of_logged_user,
                    get_all_medias, create_new_media, edit_existing_media, delete_existing_media)

urlpatterns = [
    path('', get_all_medias_of_logged_user,
         name='api.get_all_medias_of_logged_user'),
    path('all/', get_all_medias, name='api.get_all_medias'),
    path('new/', create_new_media, name='api.create_new_media'),
    path('<int:media_id>/edit/', edit_existing_media,
         name='api.edit_existing_media'),
    path('<int:media_id>/delete/', delete_existing_media,
         name='api.delete_existing_media')
]
