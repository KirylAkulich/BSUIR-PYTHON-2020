from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
import django
import hashlib
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()




class AccountManager(BaseUserManager):

    def create_user(self,email,username,password=None):
        if email is None:
            raise  AttributeError('EMAIL')
        if username is None:
            raise AttributeError("Username")
        user=self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user=self.create_user(email,username,password)
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email=models.EmailField(verbose_name='email',max_length=60,unique=True,db_index=True)
    username=models.CharField(max_length=30,unique=True)
    avatar_hash=models.CharField(max_length=200)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    validate=models.BooleanField(default=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username',]


    objects=AccountManager()

    def __init__(self,*args,**kwargs):
        super(Account,self).__init__(*args,**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash=self.gravatar_hash()

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self,size=100,default='identicon',rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __str__(self):
        return self.email +" "+self.username

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True




class Post(models.Model):

    title=models.CharField(max_length=250,db_index=True)
    slug=models.SlugField(max_length=250,
                          unique_for_date='publish')
    author=models.ForeignKey(Account,
                             on_delete=models.CASCADE,
                             related_name='blog_posts')
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title

    objects=models.Manager()
    published=PublishedManager()

class Comment(models.Model):

    post=models.ForeignKey(Post,
                           on_delete=models.CASCADE,
                           related_name='comments')
    author=models.ForeignKey(Account,
                             on_delete=models.CASCADE,
                             related_name='commnets')
    name=models.CharField(max_length=80)
    email=models.EmailField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    activate=models.BooleanField(default=True)

    class Meta:
        ordering=('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name,self.post)



class Composer(models.Model):
    post=models.ForeignKey(Post,
                           on_delete=models.CASCADE,
                           related_name='composer')
    filepath=models.CharField(max_length=50)