from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


User = get_user_model()


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name_plural = "Blogs"



def upload_to_images(instance, filename):
    return f"blogs/{slugify(instance.blog.title)}/{filename}"

class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_images)

    def __str__(self):
        return self.blog.title

    class Meta:
        verbose_name_plural = "Blog Images"



class Comment(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    context = RichTextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f"Comment from user: {self.user.email} in blog: {self.blog.title}"


    class Meta:
        verbose_name_plural = "Comments"

