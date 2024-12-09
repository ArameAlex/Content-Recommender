from django.db import models
from django.core.exceptions import ValidationError


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


class PostComment(models.Model):
    content = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=False, blank=False, db_index=True)
    replay = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{} by {} in {}'.format(self.message, self.user, self.content)

    def clean(self, *args, **kwargs):
        try:
            if self.replay.id is not None and self.content.id != self.replay.content.id:
                raise ValidationError("Please Comment In Right Post or Replay to Right Comment")
        except AttributeError:
            pass
