from rest_framework import generics
from rest_framework.response import Response
from .serializers import BlogSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Blog, BlogImage, Comment
from .permissions import IsOwnerOrReadOnly
from .paginations import BlogPagination


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = BlogPagination
    # permission_classes = (IsOwnerOrReadOnly, )


class BlogCreateView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        files = request.data.getlist("file")
        serializer = self.serializer_class(data=request.data, context={"files": files})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

    # def perform_create(self, serializer):
    #     return serializer.save(user=self.request.user)



class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    lookup_field = "id"
    permission_classes = (IsOwnerOrReadOnly, )

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        files = request.data.getlist("file") or []
        serializer = self.serializer_class(data=request.data, instance=obj, context={"files": files})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        files = request.data.getlist("file")
        serializer = self.serializer_class(data=request.data, instance=obj, partial=True, context={"files": files})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)



class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)