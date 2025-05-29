# Codespace Django REST API endpoint: https://example-codespace-name-8000.app.github.dev/api/
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination