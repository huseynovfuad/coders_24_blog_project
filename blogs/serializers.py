from rest_framework import serializers
from accounts.serializers import ProfileSerializer
from .models import Blog, BlogImage, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("blog", "context", "parent", "user")
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["replies"] = CommentSerializer(
            Comment.objects.filter(parent=instance), many=True
        ).data
        return repr_


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ("image", )


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True}
        }


    def create(self, validated_data):
        blog = Blog.objects.create(
            **validated_data
        )
        files = self.context.get("files")

        for file in files:
            BlogImage.objects.create(
                blog=blog, image=file
            )
        return blog


    def update(self, instance, validated_data):

        for key, val in validated_data.items():
            setattr(instance, key, val)

        BlogImage.objects.filter(blog=instance).delete()
        files = self.context.get("files")

        for file in files:
            BlogImage.objects.create(
                blog=instance, image=file
            )

        return instance


    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        # repr_["images"] = ImageSerializer(
        #     instance.blogimage_set.all(), many=True
        # ).data
        repr_["images"] = instance.blogimage_set.values_list("image", flat=True)
        repr_["user"] = ProfileSerializer(instance.user).data
        repr_["comments"] = CommentSerializer(
            Comment.objects.filter(parent__isnull=True, blog=instance), many=True
        ).data
        return repr_
