from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('Hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile', views.UserProfileViewset) #when registering a MODEl url no basename required
router.register('login', views.LoginViewSet, basename='login')
router.register('feed', views.UserProfileFeedItemViewSet)

urlpatterns=[
    path('hello-apiview', views.HelloApiView.as_view()),
    path('', include(router.urls)),
    
]