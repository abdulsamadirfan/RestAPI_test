from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection
from django.db.models import Count

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
#     price_with_tax = serializers.SerializerMethodField(method_name='calcualte_tex')
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset = Collection.objects.all()
#     # ) # method 1
#     # method 2
#     # collection = serializers.StringRelatedField()
#     # method 3
#     # collection = CollectionSerializer()
#     # method 4
#     collection = serializers.HyperlinkedRelatedField(
#         queryset = Collection.objects.all(),
#         view_name = 'collection-details'
#         )

    # def calcualte_tex(self, product:Product):
    #     return product.unit_price * Decimal(1.1)




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id','title','description','slug','inventory',
            'unit_price',
            'price_with_tax','collection'
        ]
    price_with_tax = serializers.SerializerMethodField(method_name='calcualte_tex')

    def calcualte_tex(self, product:Product):
        return product.unit_price * Decimal(1.1)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection 
        fields = ['id','title','products_count']

    products_count = serializers.IntegerField()
