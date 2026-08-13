from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProductViewSet, WristSizeViewSet, featured_products, health_check, me, contact_create, contact_list, contact_delete

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"wrist-sizes", WristSizeViewSet, basename="wristsize")

urlpatterns = [
    path("", include(router.urls)),
    path("featured/", featured_products, name="featured-products"),
    path("health/", health_check, name="health-check"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/me/", me, name="me"),
    path("contact/", contact_create, name="contact-create"),
    path("contacts/", contact_list, name="contact-list"),
    path("contacts/<int:pk>/", contact_delete, name="contact-delete"),
]

