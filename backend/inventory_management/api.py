from .models import Product, InventoryMovement
from rest_framework import viewsets, permissions, status, filters
from .serializers import ProductSerializer, InventoryMovementSerializer
from rest_framework.response import Response
from accounts.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from .filters import MovementFilter


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for handling products.
    Provides CRUD operations for products with filtering and searching capabilities.
    """

    queryset = Product.objects.all().order_by("name")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]

    search_fields = ["name", "description"]
    ordering_fields = ["name", "price", "quantity"]
    filterset_fields = ["is_active"]

    @action(detail=False, methods=["get"])
    def active(self, request):
        """Custom endpoint for product search suggestions"""
        queryset = self.filter_queryset(self.get_queryset())
        sugestions = queryset.values_list("name", flat=True)[:10]
        return Response(sugestions)


class InventoryMovementViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for handling inventory movements.
    Provides read-only access to inventory movements with filtering capabilities.
    """

    queryset = InventoryMovement.objects.all().order_by("-date")
    serializer_class = InventoryMovementSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    filterset_class = MovementFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED, headers=headers
                )
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
