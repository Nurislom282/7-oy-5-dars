from .models import Food, Comment
from .models import User
from .validators import validate_age
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile



class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'description', 'category', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Taom nomi'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Taom tavsifi',
                'rows': 3
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Narxi'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Izohingizni kiriting...', 'rows': 3}),
        }



class ProductSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search')

    def search(self):
        query = self.cleaned_data.get('query')
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.none()



class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'date_of_birth', 'profile_picture']

    date_of_birth = forms.DateField(validators=[validate_age])

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'profile_picture']
