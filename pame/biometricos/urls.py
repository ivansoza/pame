from django.urls import path, include
from .views import search_face , search_face1, UserFaceCreateView, compare_faces

urlpatterns = [
    path('compare_faces', compare_faces, name='comparar'),
    path('create_face/', UserFaceCreateView.as_view(), name='create_user_face'),
    path('search_face/', search_face, name='search_face'),
    path('search_face1/', search_face1, name='search_face1'),

    
]
