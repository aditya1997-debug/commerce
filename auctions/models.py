from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


CATEGORIES = [
    ('Other', 'Other'),
    ('Electronics', 'Electronics'),
    ('Fashion', 'Fashion'),
    ('Furniture', 'Furniture'),
    ('Toys', 'Toys'),
    ('Sports', 'Sports')
]
       
class User(AbstractUser):
    pass

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    category = models.CharField(max_length=255,choices=CATEGORIES,default=CATEGORIES[0][6:])
    price = models.FloatField()
    current_bid = models.FloatField(default=0)
    url = models.URLField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now())
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"        

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="fk_auction")
    bid = models.FloatField()

    def __str__(self):
        return f"  {self.user} bids {self.bid}\u20B9 on {self.auction.title}" 

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null= True)
    date_posted = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.user} on {self.auction.title} commented {self.comment}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Auction, blank=True)

    def __str__(self):
        return f"{self.user}'s watchlist"