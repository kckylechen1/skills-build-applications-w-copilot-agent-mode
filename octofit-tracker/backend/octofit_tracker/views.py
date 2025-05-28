import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

@api_view(['GET'])
def api_root(request):
    # Dynamically determine base URL
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f'https://{codespace_name}-8000.app.github.dev'
    else:
        base_url = 'http://localhost:8000'
    
    return Response({
        'status': 'success',
        'message': 'Welcome to OctoFit API',
        'baseUrl': base_url
    })

@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'healthy',
        'message': 'OctoFit API is running'
    })
