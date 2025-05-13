from rest_framework import serializers
from .models import (
    Supplier, ArticleFamily, Article, Stock, EntryVoucher, ExitRequest, ExitVoucher, ReturnRequest, ReturnVoucher, Service
)

# from rest_framework.exceptions import NotAuthenticated

# class UserContextMixin:
#     def validate(self, data):
#         request = self.context.get('request')
#         if not request and not request.user:
#             raise NotAuthenticated("User is not authenticated")
        
#         print("test user authenticated")
        
#         return data

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ArticleFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleFamily
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class EntryVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryVoucher
        fields = '__all__'

class ExitRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExitRequest
        fields = '__all__'

class ExitVoucherSerializer(serializers.ModelSerializer):
    article = serializers.CharField(source='exit_request.article')
    request_code = serializers.CharField(source='exit_request.request_code')
    class Meta:
        model = ExitVoucher
        fields = ['id', 'quantity', 'reference_number', 'created_by', 'updated_by', 'exit_request', 'created_at', 'updated_at', 'employee', 'description', 'is_active', 'article', 'request_code']

class ReturnRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnRequest
        fields = '__all__'

class ReturnVoucherSerializer(serializers.ModelSerializer):
    article = serializers.CharField(source='return_request.article')
    class Meta:
        model = ReturnVoucher
        fields = ['id', 'quantity', 'reference_number', 'created_by', 'updated_by', 'return_request', 'created_at', 'updated_at', 'employee', 'description', 'is_active', 'article', 'status']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
