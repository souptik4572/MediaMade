from django.urls import include, path

urlpatterns = [
    path('user/', include('api.user.urls')),
    path('media/', include('api.urls.media')),
]
