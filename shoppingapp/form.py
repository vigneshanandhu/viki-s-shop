from django import forms
from .models import Review, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
      
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make fields required
        self.fields['rating'].required = True
        self.fields['comment'].required = True
        
        # Add custom widgets and attributes
        self.fields['rating'].widget = forms.NumberInput(attrs={
            'min': 1,
            'max': 5,
            'placeholder': 'Rate 1-5',
            'class': 'form-control'
        })
        self.fields['comment'].widget = forms.Textarea(attrs={
            'placeholder': 'Write your review here...',
            'rows': 4,
            'class': 'form-control'
        })
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None:
            raise forms.ValidationError('Rating is required.')
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating
    
    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if not comment or not comment.strip():
            raise forms.ValidationError('Comment is required.')
        return comment.strip()


class RegisterForm(forms.ModelForm):
  username = forms.CharField(label='username',max_length=100,required=True)
  email = forms.EmailField(label='email',max_length=100,required=True)
  password = forms.CharField(label='password',max_length=100,required=True)
  password_confirm = forms.CharField(label='confirm_password',max_length=100,required=True)
  class Meta:
    model = User
    fields = ['username','email','password']

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
      raise forms.ValidationError('Email is already in use')
    return email
  
  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get('password')
    password_confirm = cleaned_data.get('password_confirm')

    if password and password_confirm and password != password_confirm:
      raise forms.ValidationError("passwords do not match")
    

class LoginForm(forms.Form):
    username = forms.CharField(label='username',max_length=100,required=True)
    password = forms.CharField(label='password',max_length=100,required=True)

    def clean(self):
      cleaned_data = super().clean()
      username = cleaned_data.get('username')
      password = cleaned_data.get('password')
      
      if username and password:
        user = authenticate(username=username,password=password)
        if user is None:
          raise forms.ValidationError("invalid username and password")

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'city', 'zip_code']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Complete Delivery Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code'}),
        }


    
