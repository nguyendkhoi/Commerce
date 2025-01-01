from django import forms
from .models import AuctionListings

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListings
        fields = ['title', 'price', 'image', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
