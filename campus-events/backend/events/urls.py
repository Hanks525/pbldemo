from django.urls import path
from . import views

urlpatterns = [
    path('activities/', views.ActivityList.as_view(), name='activity-list'),
    path('activities/<int:pk>/', views.ActivityDetail.as_view(), name='activity-detail'),
    path('activities/<int:pk>/comments/', views.CommentList.as_view(), name='comment-list'),
    path('activities/<int:pk>/favorites/', views.FavoriteView.as_view(), name='favorite-view'),
    path('activities/<int:pk>/register/', views.RegistrationView.as_view(), name='registration-view'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]
