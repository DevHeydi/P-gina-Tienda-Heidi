from django.urls import path
# agregar ulrs de app1
from . import views

urlpatterns = [
    path('infor/', views.info, name='info'),
    path('', views.home, name='home'),
    path('stores/', views.stores_view, name='stores'),
    path('products/', views.products_view, name='products'),
    path('create_store/', views.create_store, name='create_store'),
    path('create_product/', views.create_product, name='create_product'),
    path('details/<int:id>/', views.details, name='details'),
    path('contact/', views.contact, name='contact'),
    path('filtro/', views.ProductosListView.as_view(), name='filtro'),
    path('update_product/', views.update_product, name='update_product'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('filtro_tienda/', views.StoreListView.as_view(), name='filtro_tienda'),
    path('update_store/', views.update_stores, name='update_store'),
    path('delete_stores/', views.delete_stores, name='delete_stores'),
]
