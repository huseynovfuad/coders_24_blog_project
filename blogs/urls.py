from django.urls import path
from . import views

app_name = "blogs"


urlpatterns = [
    path("", views.BlogListView.as_view(), name="list"),
    path("create/", views.BlogCreateView.as_view(), name="create"),
    path("detail/<id>/", views.BlogDetailView.as_view(), name="detail"),
    path("comments/create/", views.CommentCreateView.as_view(), name="comments-create"),
]