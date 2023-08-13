from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from .ForbiddenWord import ForbiddenWord


User = get_user_model()
# Create your models here.
class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=40, blank=True)
    slug = slug = models.SlugField(max_length=400, unique=True, blank=True)
    bio = models.TextField()
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return self.fullname

    def contains_forbidden_words(self):
        forbidden_words = ForbiddenWord.objects.values_list('word', flat=True)
        content_words = self.bio.lower().split()  # Split content into words
        content_title = self.fullname.lower().split()  # Split content into words
        combined_words = content_words + content_title
        
        for word in combined_words:
            if word in forbidden_words:
                return True
        return False
    
    def save(self, *args, **kwargs):
        if self.contains_forbidden_words():
            raise ValueError("Post contains forbidden words.")
        if not self.slug:
            self.slug = slugify(self.fullname)
        super(Author, self).save(*args, **kwargs)
        

class Reply(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    account = models.CharField(max_length=30, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:100]

    class Meta:
        verbose_name_plural = "replies"

class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    account = models.CharField(max_length=30, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True)

    def __str__(self):
        return self.content[:100]
    @property
    def num_replies(self):
        return self.replies.count()

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug  = models.SlugField(max_length=400, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
    
    def get_url(self):
        return reverse("posts", kwargs={
            "slug":self.slug
        })
    
    @property
    def num_posts(self):
        return Post.objects.filter(categories=self).count()
    
    @property
    def last_post(self):
        return Post.objects.filter(categories=self).latest("date")
"""
class Reply(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:100]

    class Meta:
        verbose_name_plural = "replies"
        
class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True)

    def __str__(self):
        return self.content[:100]
"""

class Post(models.Model):
    title = models.CharField(max_length=400)
    type = models.CharField(max_length=6,blank=True)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    account = models.CharField(max_length=30, blank=True)
    content = models.TextField() 
    categories = models.ManyToManyField(Category)
    date = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    tags = TaggableManager()
    comments = models.ManyToManyField(Comment, blank=True)

    
    def contains_forbidden_words(self):
        forbidden_words = ForbiddenWord.objects.values_list('word', flat=True)
        content_words = self.content.lower().split()  # Split content into words
        content_title = self.title.lower().split()  # Split content into words
        combined_words = content_words + content_title
        
        for word in combined_words:
            if word in forbidden_words:
                return True
        return False

    def save(self, *args, **kwargs):
        if self.contains_forbidden_words():
            raise ValueError("Post contains forbidden words.")
        
        if not self.slug:
            self.slug = slugify(self.title)
        self.approved = True
        super(Post, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse("post", kwargs={
            "slug":self.slug
        })
    
    @property
    def num_comments(self):
        return self.comments.count()

    @property
    def last_reply(self):
        return self.comments.latest("date")


