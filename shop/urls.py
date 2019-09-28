from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.allProdCat, name='allProdCat'),
    path('<slug:c_slug>/', views.allProdCat, name='products_by_category'),
    path('product/<int:prod_id>/', views.product, name='productInfo'),
    path('<slug:c_slug>/<slug:product_slug>/', views.ProdCatDetail, name="ProdCatDetail"),
    path('myview/ss', views.myview, name="myview"),
]