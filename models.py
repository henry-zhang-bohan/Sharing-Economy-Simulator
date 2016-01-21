from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User)
    capital = models.DecimalField(max_digits = 6, decimal_places = 2)
    
class Sharing(models.Model):
    user = models.OneToOneField(User)
    capital = models.DecimalField(max_digits = 6, decimal_places = 2)

class MarketItem(models.Model):
    name = models.CharField(max_length = 10)
    current_value = models.DecimalField(max_digits = 6, decimal_places = 2)
    
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

class Item(models.Model):
    owner = models.ForeignKey(User)
    on_market = models.BooleanField(default = False)
    time = models.DateTimeField()
    value = models.ForeignKey(MarketItem)
    selling_price = models.DecimalField(max_digits = 6, decimal_places = 2)
    sharing = models.BooleanField(default = False)

class Comment(models.Model):
    author = models.ForeignKey(User)
    comment_text = models.CharField(max_length = 200)
    time = models.DateTimeField()
