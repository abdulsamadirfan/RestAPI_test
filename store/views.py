from django.shortcuts import get_object_or_404
# from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from rest_framework import status
from django.db.models import Count




# Create your v iews here.
# @api_view()
# def product_list(request):
#     return Response('ok')
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset,many=True,context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        # method 1
        # if serializer.is_valid():
        #     serializer.validate_data
        #     return Response('ok')
        # else:
        #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        # method 2
        # serializer.is_valid(raise_exception=True)
        # serializer.validate_data
        # return Response('ok')


        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)


##############
@api_view(['GET', 'POST'])
def collections_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(
            products_count=Count('products')).all()
        serializer = CollectionSerializer(
            queryset,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED)
##############


@api_view(['GET','PUT','DELETE'])
def product_details(request, id):
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)


    product = get_object_or_404(Product,pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(
            product,context={'request': request})
        return Response(serializer.data) 
    elif request.method == 'PUT':
        serializer = ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response(
                {"error":'product cannot be deleted because it is associated with order item'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET','PUT','DELETE'])
def collections_details(request,pk):
    collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')),
            pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(
            collection,context={'request': request})
        return Response(serializer.data) 
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response(
                {"error":'collection cannot be deleted because it is associated with products'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

