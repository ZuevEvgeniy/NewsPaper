from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


article = '01'
news = '02'

TYPE = [
    (article, 'Статья'),
    (news, 'Новость')
]


class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    def update_rating(self):
        author_posts_rating = Post.objects.filter(author_id=self.pk).aggregate(
            post_rating_sum=Coalesce(Sum('rate') * 3, 0))
        author_comment_rating = Comment.objects.filter(user_id=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rate'), 0))
        author_post_comment_rating = Comment.objects.filter(author=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rate'), 0))
        self.rating_autor = author_posts_rating['posts_rating_sum'] + author_comment_rating['comments_rating_sum'] \
            + author_post_comment_rating['comments_rating_sum']
        self.save()


class Category(models.Model):

    name_category = models.CharField(max_length=250, unique=True)


class Post(models.Model):

    objects = None
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPE, default=article)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    head_name = models.CharField(max_length=250, unique=True)
    article_text = models.TextField()
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self):
        article_text = self.article_text
        preview = article_text[0:124]
        points = "..."
        return preview + points


class PostCategory(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):

    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()