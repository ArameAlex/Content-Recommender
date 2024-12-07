from django.db import models

from UserApp.models import User


class CategoryModel(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class ContentModel(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/content', null=True, blank=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    description = models.TextField()
    # viewed by all users
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ViewCountModel(models.Model):
    content = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # one user view count to keep track of user visited contents
    view_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('content', 'user')

    def __str__(self):
        return self.content.name


class FavoritePosts(models.Model):
    content = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.content.name}, {self.user.username}'
