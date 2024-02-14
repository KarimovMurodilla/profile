from django.urls import path
from . import views



from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    #Authentication
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('', views.getRoutes),


    #Profile
    path('profile/', views.getProfile, name='profile'),
    path('profile/<str:slug>', views.getProfileByUsername, name='profile'),
    path('profiles/', views.ProfileListView.as_view(), name='profiles'),
    path('profile/update/', views.updateProfile, name='update-profile'),


    #Comments
    path('comments/', views.getComments, name="comments"),
    path('users/<int:pk>/comments/', views.getUserComments, name="my-comments"),
    path('comments/create/<int:pk>', views.createComment, name="create-comment"),
]
