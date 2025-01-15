from django.contrib.auth import views as auth_views
from . import views
from .views import product_search
from django.urls import path
from .views import register, login_view, profile



urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('foods/', views.all_foods, name='all_foods'),
    path('food/<int:food_id>/', q.food_detail, name='food_detail'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('category/<int:category_id>/', views.category_foods, name='category_foods'),
    path('food/add/', views.add_food, name='add_food'),
    path('food/edit/<int:food_id>/', views.edit_food, name='edit_food'),
    path('send-email/', views.send_email_view, name='send_email'),
    path('user-permissions/', views.user_permissions_view, name='user_permissions'),
    path('send-email/', views.send_email_view, name='send_email'),
    path('search/', product_search, name='product_search'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
]
