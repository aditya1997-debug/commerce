from tkinter import Widget
from django import forms
from django.forms import ModelForm
from auctions.models import Auction, Bid, Comment

class Auctionform(ModelForm):
    class Meta:
        model = Auction
        fields = ('title' , 'description', 'category', 'price', 'url')

        labels={
            'title':"",
            'description':"",
            'price':"",
            'url':"",
            'category':""

        }
        
        widgets = {
            'price' : forms.NumberInput(attrs={'min': '1' ,'step': "0.01" , 'placeholder': 'Price'}),
            'title' : forms.TextInput(attrs={'placeholder': 'Title of your listing...'}),
            'description' : forms.Textarea(attrs={'placeholder': 'Description...'}),
            'url': forms.TextInput(attrs={'placeholder': 'Paste image link of your listing...'}),
            'category':forms.Select(attrs={'placeholder' : 'Choose category of your listing...'})
    }
        


class Bidform(ModelForm):
    class Meta:
        model = Bid
        fields = ('bid',)

        labels={
            'bid':""
        }

        widgets={
            'bid' : forms.NumberInput(attrs={'min': '1' ,'step': "0.01", 'placeholder' : "Place Bid"})
        }

class Commentform(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)        

        labels = {
            'comment':""
        }

        widgets={
            'comment': forms.TextInput(attrs={'placeholder':'Say Something...','null':'False'})
        }