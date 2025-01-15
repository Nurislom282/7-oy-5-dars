from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Food, Comment
from .forms import FoodForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import ProductSearchForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, ProductForm
from django.contrib.auth import login, authenticate



def home(request):
    foods = Food.objects.all()
    return render(request, 'home.html', {'foods': foods})

def all_foods(request):
    foods = Food.objects.all()
    return render(request, 'all_food.html', {'foods': foods})

def food_detail(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    comments = food.comments.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.food = food
            comment.user = request.user
            comment.save()
            return redirect('food_detail', food_id=food.id)
    else:
        form = CommentForm()

    return render(request, 'food_detail.html', {
        'food': food,
        'comments': comments,
        'form': form,
        'user': request.user,
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
    return redirect('food_detail', food_id=comment.food.id)

def category_foods(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    foods = Food.objects.filter(category=category)
    return render(request, 'category_foods.html', {'category': category, 'foods': foods})

def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_foods')
    else:
        form = FoodForm()
    return render(request, 'add_food.html', {'form': form})

def edit_food(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            return redirect('food_detail', food_id=food.id)
    else:
        form = FoodForm(instance=food)
    return render(request, 'edit_food.html', {'form': form, 'food': food})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
@permission_required('app_name.can_add_modelname', raise_exception=True)
def send_email_view(request):
    subject = 'Sizning so’rovingizni qabul qildik'
    message = 'Salom! Sizning so’rovingiz muvaffaqiyatli yuborildi.'
    from_email = 'from_email@example.com'
    recipient_list = ['to_email@example.com']

    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse("Xabar yuborildi!")
    except Exception as e:
        return HttpResponse(f"Xatolik: {str(e)}")


@login_required
def user_permissions_view(request):
    user_permissions = request.user.get_all_permissions()

    can_add = 'app_name.can_add_modelname' in user_permissions
    can_change = 'app_name.can_change_modelname' in user_permissions
    can_delete = 'app_name.can_delete_modelname' in user_permissions

    context = {
        'can_add': can_add,
        'can_change': can_change,
        'can_delete': can_delete,
    }

    return render(request, 'permissions_template.html', context)



def product_search(request):
    form = ProductSearchForm(request.GET)
    products = None
    if form.is_valid():
        products = form.search()

    return render(request, 'product_search.html', {'form': form, 'products': products})




def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def profile(request):
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_profile_form.is_valid():
            user_profile_form.save()
    else:
        user_profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'profile.html', {'user_profile_form': user_profile_form})
