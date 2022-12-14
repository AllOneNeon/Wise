from django.urls import path, include


app_name = 'api'
urlpatterns = [
    path('users/', include('user.urls', namespace='auth')),
    path('pages/', include('core.urls', namespace='pages')),
    path('posts/', include('core.urls', namespace='posts')),
    path('subscribers/', include('core.urls', namespace='subscribers')),
]