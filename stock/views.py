from requests import delete
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .utils import generate_unique_num_ref

from .models import (
    Supplier, ArticleFamily, Article, Stock, EntryVoucher, ExitRequest, ExitVoucher, ReturnRequest, ReturnVoucher, Service
)

from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination  

from .serializers import (
    SupplierSerializer, ArticleFamilySerializer, ArticleSerializer, StockSerializer,
    EntryVoucherSerializer, ExitRequestSerializer, ExitVoucherSerializer,
    ReturnRequestSerializer, ReturnVoucherSerializer, ServiceSerializer
)

from api_gestion_stock.constants import INTITY_API_URL

from rest_framework import viewsets, status
from rest_framework.response import Response

class SizePagination(PageNumberPagination):
    page_size = 100  # default page size
    page_size_query_param = 'page_size'
    max_page_size = 1000

class BaseViewSet(viewsets.ModelViewSet):
    """
    Custom ModelViewSet that ensures only authenticated users can create or update objects.
    It automatically checks if the user is authenticated before performing actions.
    """

    # permission_classes = [IsAuthenticated]
    pagination_class = SizePagination

    def check_authentication(self):
        if self.request.user.is_anonymous:
            print("user anonyme ? :", self.request.user.is_anonymous)
            return Response({"Success": False, "detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        return None
    
    def paginate_queryset_response(self, queryset, request, serializer_class):
        """
        Paginate the queryset and return a paginated response.
        This method can be used in any child class.
        """
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # if paginated_queryset is not None:
        serializer = serializer_class(paginated_queryset, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data)
        return Response(
            {
                "success": True,
                "data": paginated_response.data,
            },
            status=status.HTTP_200_OK
        )

        # serializer = serializer_class(queryset, many=True)
        # return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        auth_error = self.check_authentication()
        if auth_error:
            return auth_error
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        auth_error = self.check_authentication()
        if auth_error:
            return auth_error
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        auth_error = self.check_authentication()
        if auth_error:
            return auth_error
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        auth_error = self.check_authentication()
        if auth_error:
            return auth_error
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        auth_error = self.check_authentication()
        if auth_error:
            return auth_error
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        auth_error = self.check_authentication()
        if auth_error:
            return auth_error
        return super().destroy(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     extra_kwargs = {}
    #     if hasattr(serializer.Meta.model, 'created_by'):
    #         extra_kwargs['created_by'] = self.request.user
    #     if hasattr(serializer.Meta.model, 'updated_by'):
    #         extra_kwargs['updated_by'] = self.request.user
    #     serializer.save(**extra_kwargs)

    # def perform_update(self, serializer):
    #     extra_kwargs = {}
    #     if hasattr(serializer.Meta.model, 'updated_by'):
    #         extra_kwargs['updated_by'] = self.request.user
    #     serializer.save(**extra_kwargs)


class SupplierViewSet(BaseViewSet):
    queryset = Supplier.objects.all().order_by("id")
    serializer_class = SupplierSerializer

    def list(self, request, *args, **kwargs):

        # print("request.user.id_employee", request.user.id_employee)

        auth_error = self.check_authentication()
        if auth_error:
            return auth_error

        queryset = self.get_queryset()
        return self.paginate_queryset_response(queryset, request, self.serializer_class)
    
        
        


class ArticleFamilyViewSet(BaseViewSet):
    queryset = ArticleFamily.objects.all().order_by("id")
    serializer_class = ArticleFamilySerializer

    def list(self, request, *args, **kwargs):

        auth_error = self.check_authentication()
        if auth_error:
            return auth_error

        queryset = self.get_queryset()
        return self.paginate_queryset_response(queryset, request, self.serializer_class)
    
    def delete(self, request, *args, **kwargs):
        auth_error = self.check_authentication()
        if auth_error:
            return auth_error
        
        instance = self.get_object()

        # Mettre à jour le statut de l'instance (soft delete)
        instance.is_active = False
        instance.save()

        # Retourner une réponse indiquant que l'opération a réussi
        return Response(
            {"detail": "L'article a été supprimé avec succès (soft delete)."},
            status=status.HTTP_204_NO_CONTENT
        )


class ArticleViewSet(BaseViewSet):
    queryset = Article.objects.all().order_by("id")
    serializer_class = ArticleSerializer

    def list(self, request, *args, **kwargs):

        auth_error = self.check_authentication()
        if auth_error:
            return auth_error

        queryset = self.get_queryset()
        return self.paginate_queryset_response(queryset, request, self.serializer_class)
    
    def create(self, request, *args, **kwargs):
        auth_error = self.check_authentication()
        if auth_error:
            return auth_error
        
        # Serialize article data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            article = serializer.save()
            quantity = int(request.data.get('initial_stock', 0))

            # Create an initial stock for the article
            stock_data = {
                'article': article,
                'initial_stock': quantity,
                'final_stock': quantity
            }
            Stock.objects.create(**stock_data)

            return Response(
                {
                    "success": True,
                    "message": "Article created and stock initialized.",
                    "article": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class StockViewSet(BaseViewSet):
    queryset = Stock.objects.all().order_by("id")
    serializer_class = StockSerializer


class EntryVoucherViewSet(BaseViewSet):
    queryset = EntryVoucher.objects.all().order_by("id")
    serializer_class = EntryVoucherSerializer

    def perform_create(self, serializer):
        # Génération du numéro de référence automatique
        reference_number = generate_unique_num_ref(EntryVoucher)
        
        # Création de l'objet EntryVoucher avec l'utilisateur actuel
        entry_voucher = serializer.save(
            reference_number=reference_number,
            created_by=self.request.user.id_employee,
            updated_by=self.request.user.id_employee
        )

        # Mise à jour du stock
        stock_article = Stock.objects.filter(article=entry_voucher.article).first()
        if stock_article:
            stock_article.stock_variation = entry_voucher.quantity
            stock_article.final_stock += entry_voucher.quantity
            stock_article.save()
        
        # print("stock_article" , stock_article.final_stock)

        return Response(serializer.data)
    
    def perform_update(self, serializer):
        # Mise à jour de l'utilisateur
        entry_voucher = serializer.save(updated_by=self.request.user.id_employee)
        return Response(serializer.data)


class ExitRequestViewSet(BaseViewSet):
    queryset = ExitRequest.objects.all().order_by("id")
    serializer_class = ExitRequestSerializer

    def perform_create(self, serializer):
        article = serializer.validated_data['article']
        quantity = serializer.validated_data['quantity']
        description = serializer.validated_data['description']

        # Vérification de l'existence du stock
        stock_article = Stock.objects.filter(article=article).first()
        if not stock_article:
            return ValidationError({
                "success": False,
                "detail": "Stock record not found for this article!",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Vérification de la quantité en stock
        if stock_article.final_stock < quantity:
            raise ValidationError({
                "success": False,
                "detail": "Quantity requested exceeds quantity in stock!",
            })

        # Mise à jour du stock
        stock_article.stock_variation = -quantity
        stock_article.final_stock -= quantity
        stock_article.save()

        # Enregistrement de la demande de sortie
        exit_request = serializer.save()

        # Génération du numéro de référence
        reference_number = generate_unique_num_ref(ExitVoucher)

        # Création du bon de sortie
        exit_voucher = ExitVoucher.objects.create(
            quantity=quantity,
            reference_number=reference_number,
            created_by=self.request.user.id_employee,
            updated_by=self.request.user.id_employee,
            description=description,
            exit_request=exit_request,
            employee=self.request.user.id_employee
        )

        # Retourner les données mises à jour
        # return Response({
        #     "success": True,
        #     "exit_request": serializer.data,
        #     "exit_voucher": {
        #         "id": exit_voucher.id,
        #         "reference_number": exit_voucher.reference_number,
        #         "quantity": exit_voucher.quantity,
        #         "description": exit_voucher.description
        #     }
        # }, status=status.HTTP_201_CREATED)


class ExitVoucherViewSet(BaseViewSet):
    queryset = ExitVoucher.objects.all().order_by("id")
    serializer_class = ExitVoucherSerializer


class ReturnRequestViewSet(BaseViewSet):
    queryset = ReturnRequest.objects.all().order_by("id")
    serializer_class = ReturnRequestSerializer

    def perform_create(self, serializer):
        article = serializer.validated_data['article']
        quantity = serializer.validated_data['quantity']
        description = serializer.validated_data['description']
        status = serializer.validated_data['status']

        # Vérification de l'existence du stock
        stock_article = Stock.objects.filter(article=article).first()

        if not stock_article:
            return ValidationError({
                "success": False,
                "detail": "Stock record not found for this article!",
            })

        # Mise à jour du stock
        stock_article.stock_variation = quantity
        stock_article.final_stock += quantity
        stock_article.save()

        # Enregistrement de la demande de sortie
        return_request = serializer.save(employee=self.request.user.id_employee)

        # Génération du numéro de référence
        reference_number = generate_unique_num_ref(ReturnVoucher)

        # Création du bon de sortie
        return_voucher = ReturnVoucher.objects.create(
            quantity=quantity,
            reference_number=reference_number,
            created_by=self.request.user.id_employee,
            updated_by=self.request.user.id_employee,
            description=description,
            return_request=return_request,
            employee=self.request.user.id_employee,
            status=status
        )


class ReturnVoucherViewSet(BaseViewSet):
    queryset = ReturnVoucher.objects.all().order_by("id")
    serializer_class = ReturnVoucherSerializer


# class ServiceViewSet(BaseViewSet):
#     queryset = Service.objects.all().order_by("id")
#     serializer_class = ServiceSerializer
