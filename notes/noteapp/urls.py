from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('signup/', views.signup),
    path('notes/create/', views.create_note),
    path('notes/<int:id>/', views.get_note),
    path('notes/share/', views.share_note),
    path('notes/update/<int:id>/', views.update_note),
    path('notes/version-history/<int:id>/', views.version_history),
]