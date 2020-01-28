from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Quote(models.Model):
    author = models.ForeignKey(User,related_name='author',on_delete=models.CASCADE)
    quote = models.CharField(max_length=255,blank=False)