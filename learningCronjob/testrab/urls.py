from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'product1', views.Product1Viewset)
# router.register(r'product', views.ProductViewset)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('product/', views.ProductView.as_view()),
    path('product/<int:id>', views.GetProductone.as_view()),
]