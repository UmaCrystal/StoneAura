from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Q
from .models import Product, WristSize, ContactMessage
from .serializers import ProductSerializer, WristSizeSerializer, ContactMessageSerializer


from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1000  # Load all by default to make sure client sees everything
    page_size_query_param = 'page_size'
    max_page_size = 5000

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "stone_type", "material", "color"]
    ordering_fields = ["price", "name", "created_at"]
    ordering = ["name"]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        qs = super().get_queryset()
        collection = self.request.query_params.get("collection")
        category  = self.request.query_params.get("category")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        stone     = self.request.query_params.get("stone_type")
        if collection:
            qs = qs.filter(collection__icontains=collection)
        if category:
            qs = qs.filter(category__icontains=category)
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        if stone:
            qs = qs.filter(stone_type__icontains=stone)
        return qs

    def perform_create(self, serializer):
        from django.utils.text import slugify
        name = serializer.validated_data.get("name", "")
        slug = slugify(name)
        base = slug
        n = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base}-{n}"
            n += 1
        wa = "https://wa.me/919510010383?text=Hi%2C%20I%20am%20interested%20in%20" + name.replace(" ", "%20")
        
        # Handle file upload if present
        image_url = serializer.validated_data.get("image_url", "")
        uploaded_file = self.request.FILES.get("image")
        if uploaded_file:
            image_url = self._save_uploaded_image(uploaded_file)
        elif not image_url:
            image_url = f"https://placehold.co/480x480/f5f0e8/c9a84c?text={name.replace(' ', '+')}"
            
        serializer.save(slug=slug, whatsapp_link=wa, image_url=image_url)

    def perform_update(self, serializer):
        image_url = serializer.validated_data.get("image_url", None)
        uploaded_file = self.request.FILES.get("image")
        if uploaded_file:
            image_url = self._save_uploaded_image(uploaded_file)
            
        if image_url is not None:
            instance = serializer.save(image_url=image_url)
        else:
            instance = serializer.save()
            
        if not instance.whatsapp_link:
            wa = "https://wa.me/919510010383?text=Hi%2C%20I%20am%20interested%20in%20" + instance.name.replace(" ", "%20")
            instance.whatsapp_link = wa
            instance.save()

    def _save_uploaded_image(self, uploaded_file):
        import os
        from django.conf import settings
        import shutil
        import requests
        from requests.auth import HTTPBasicAuth
        
        private_key = os.environ.get("IMAGEKIT_PRIVATE_KEY")
        url_endpoint = os.environ.get("IMAGEKIT_URL_ENDPOINT")
        
        # Try uploading to ImageKit first if credentials are set
        if private_key and url_endpoint:
            try:
                upload_url = "https://upload.imagekit.io/api/v1/files/upload"
                auth = HTTPBasicAuth(private_key, "")
                
                # Read file contents for API request
                uploaded_file.seek(0)
                file_data = uploaded_file.read()
                
                files = {
                    'file': (uploaded_file.name, file_data, uploaded_file.content_type)
                }
                data = {
                    'fileName': uploaded_file.name,
                    'folder': '/products',
                    'useUniqueFileName': 'true'
                }
                
                response = requests.post(upload_url, auth=auth, files=files, data=data, timeout=30)
                if response.status_code == 200:
                    return response.json().get("url")
            except Exception:
                pass
        
        # Fallback to local storage (e.g. for development)
        public_dir = os.path.join(settings.BASE_DIR, 'frontend', 'public', 'images', 'products')
        os.makedirs(public_dir, exist_ok=True)
        
        filename = uploaded_file.name
        dest_path = os.path.join(public_dir, filename)
        
        # Reset file cursor before writing
        uploaded_file.seek(0)
        
        with open(dest_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
                
        # Also copy to build directory if it exists
        build_dir = os.path.join(settings.BASE_DIR, 'frontend', 'build', 'images', 'products')
        if os.path.exists(os.path.join(settings.BASE_DIR, 'frontend', 'build')):
            os.makedirs(build_dir, exist_ok=True)
            try:
                shutil.copy2(dest_path, os.path.join(build_dir, filename))
            except Exception:
                pass
            
        return f"/images/products/{filename}"


class WristSizeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WristSize.objects.all()
    serializer_class = WristSizeSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def featured_products(request):
    products = Product.objects.filter(is_featured=True)[:8]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "ok", "message": "Aurastone API is running"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
        "is_admin": request.user.is_staff or request.user.is_superuser,
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def contact_create(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def contact_list(request):
    """Admin-only: list all contact messages, newest first. Supports ?search= filter."""
    qs = ContactMessage.objects.all().order_by("-created_at")
    search = request.query_params.get("search", "").strip()
    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(message__icontains=search)
        )
    serializer = ContactMessageSerializer(qs, many=True)
    unread_count = ContactMessage.objects.filter(is_read=False).count()
    return Response({
        "count": qs.count(),
        "unread_count": unread_count,
        "results": serializer.data
    })


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAdminUser])
def contact_detail(request, pk):
    """Admin-only: PATCH to mark as read/unread, DELETE to delete a message."""
    try:
        msg = ContactMessage.objects.get(pk=pk)
    except ContactMessage.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == "PATCH":
        is_read = request.data.get("is_read")
        if is_read is not None:
            msg.is_read = bool(is_read)
            msg.save()
        serializer = ContactMessageSerializer(msg)
        return Response(serializer.data)
        
    elif request.method == "DELETE":
        msg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
