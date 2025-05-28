from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

@api_view(['GET'])
def api_root(request):
    return Response({
        'status': 'success',
        'message': 'Welcome to OctoFit API',
        'baseUrl': 'https://fantastic-couscous-gj9j9pxv7j7cvp5r-8000.app.github.dev'
    })
