from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.product_list),
    path('collections/', views.collections_list),
    path('products/<int:id>/',views.product_details),
    path('collections/<int:pk>/',views.collections_details,name = 'collection-details')
]
