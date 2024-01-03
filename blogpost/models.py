from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)

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
    views       = models.IntegerField(default=0, null=True)
    commentcount = models.IntegerField(default=0)
    profile      = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    tag         = models.ForeignKey(Tag, on_delete = models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
    #def get_absolute_url(self):
	    #return reverse("blog_detail", kwargs={"slug": self.slug, "pk": self.id})

	#def save(self, *args, **kwargs):
	    #if not self.slug:
		    #self.slug = slugify(self.title)
        #return super().save(*args, **kwargs)
    
class Section(models.Model):
    blogpost    = models.ForeignKey(Post, on_delete = models.CASCADE)
    body        = models.TextField()
    secimg      = models.ImageField(upload_to='sectionimages/', blank=True, null=True)

    def __str__(self):
        return self.blogpost.title + " : section " + str(self.id)

class Comment(models.Model):
    name        = models.CharField(max_length=20, default="Anonymous")
    message     = models.TextField(null=True)
    date        = models.DateTimeField(verbose_name="date_comented", auto_now_add=True)
    post        = models.ForeignKey(Post, on_delete= models.CASCADE)

    def __str__(self):
        return self.name + " commented on " + self.post.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.post.commentcount = Comment.objects.filter(post=self.post).count()
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
