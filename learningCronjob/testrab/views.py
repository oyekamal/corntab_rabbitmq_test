from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView

from .serializer import Product1Serializer, ProductSerializer
from .models import Product1, Product
from rest_framework.response import Response
from .producer import publish
from learningCronjob.client import RpcClient
import json
class Product1Viewset(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Product1.objects.all()
    serializer_class = Product1Serializer
    
# class ProductViewset(viewsets.ModelViewSet):

#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class ProductView(APIView):
    def get(self, request):
        pro = Product.objects.all()
        serializer = ProductSerializer(pro, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.datsa)
        if serializer.is_valid():
            serializer.save()
            publish('product_created', serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors)

class GetProductone(APIView):
    def get(self, request, id):
        print('id', id)
        
        client = RpcClient()
        data = client.call(id)
        print(type(data.decode()))
        data=data.decode()
        return Response(json.loads(data))