from .views import *
from django.urls import path
from knox import views as knox_views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('api/user/', UserAPI.as_view()),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),   
    
    path('api/category/', ListCategory.as_view(),name='category' ),
    path('api/products/', ProductView.as_view()),
    path('api/favorite/', FavoriteView.as_view()),
    path('api/products_by_category/', ProductByCategoryView.as_view()),
    path('api/search_product/', SearchView.as_view()),
    path('api/test/', PoductViewPagination.as_view()),
    path('api/cart/', CartItemView.as_view()),
    path('api/cart/add/', CartItemAddView.as_view()),
    path('api/cart/increse_quantity/<int:pk>/', CartItemAddOneView.as_view()),
    path('api/cart/reduce_quantity/<int:pk>/', CartItemReduceOneView.as_view()),
    path('api/cart/delete/<int:pk>/', CartItemDelView.as_view()),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


