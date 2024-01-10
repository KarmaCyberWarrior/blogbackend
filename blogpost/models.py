from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    displaypic = models.ImageField(upload_to='profileimages/', null=True)
    is_editor = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    published_post = models.IntegerField(default=0)
    draft_posts = models.IntegerField(default=0)
    total_posts = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    totalpost_impressions = models.IntegerField(default=0)

    def __str__(self):
        return self.fname + " @" + self.user.username

class Tag(models.Model):
    tag         = models.CharField(max_length = 20)

    def __str__(self):
        return self.tag


class Post(models.Model):
    title       = models.CharField(max_length=200)
    breif       = models.TextField()
    snippet     = models.TextField()
    headimg     = models.ImageField(upload_to='blogimages/', null=True)
    timestamp   = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    date        = models.DateField(verbose_name="dateposted created", auto_now_add=True)
    views       = models.IntegerField(default=0, null=True)
    commentcount = models.IntegerField(default=0)
    totalcount  = models.IntegerField(default=0)
    profile      = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    isPublished  = models.BooleanField(default=False)
    tag         = models.ForeignKey(Tag, on_delete = models.SET_NULL, null=True)
    slug			= models.SlugField(max_length=255, blank=True, unique=True)

    def __str__(self):
        return self.title
    
    
    def save(self, *args, **kwargs):
        # If slug is not set or is empty, generate it based on the title
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        
        
    
class Section(models.Model):
    blogpost    = models.ForeignKey(Post, on_delete = models.CASCADE)
    body        = models.TextField()
    secimg      = models.ImageField(upload_to='sectionimages/', blank=True, null=True)

    def __str__(self):
        return self.blogpost.title + " : section " + str(self.id)

class Comment(models.Model):
    name        = models.CharField(max_length=20, default="Anonymous")
    email       = models.CharField(max_length=100)
    message     = models.TextField(null=True)
    date        = models.DateTimeField(verbose_name="date_comented", auto_now_add=True)
    post        = models.ForeignKey(Post, on_delete= models.CASCADE)
    replycount  = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " commented on " + self.post.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.post.commentcount = Comment.objects.filter(post=self.post).count()
        self.post.totalcount   = Comment.objects.filter(post=self.post).count() + self.replycount
        self.post.save()

class Sub(models.Model):
    name        = models.CharField(max_length=20)
    email       = models.EmailField(verbose_name="email", max_length=60, unique=True)
    is_subscribed = models.BooleanField(default=True)


class Reply(models.Model):
    comment     = models.ForeignKey(Comment, on_delete= models.CASCADE)
    name        = models.CharField(max_length=20, default="Anonymous")
    message     = models.TextField()  

    def __str__(self):
        return self.name + " replied " + self.comment.name + " on " + self.comment.post.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.comment.replycount = Reply.objects.filter(comment=self.comment).count()
        self.comment.save()
