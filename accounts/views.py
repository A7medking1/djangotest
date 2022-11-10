from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.models import AuthToken 
from .serializers import *
from django.contrib.auth import login
from .models import *
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
#from rest_framework import pagination

'''class CustomPagination(pagination.PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'count'
    max_page_size = 10
    page_query_param = 'page'
'''
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user


class ListCategory(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        query = Product.objects.all()
        data = []
    
        serializers = ProductSerializer(query, many=True)
        for product in serializers.data:
            fab_query = Favorite.objects.filter(
                user=request.user).filter(product_id=product['id'])
            if fab_query:
                product['favorit'] = fab_query[0].isFavorit
            else:
                product['favorit'] = False
            data.append(product)
       
        return Response(data)


class FavoriteView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    def post(self, request):
        data = request.data['id']
        #print(data)
        try:
            product_obj = Product.objects.get(id=data)
            user = request.user
            single_favorit_product = Favorite.objects.filter(
                user=user).filter(product=product_obj).first()
            if single_favorit_product:
                isFav = single_favorit_product.isFavorit
                single_favorit_product.isFavorit = not isFav
                single_favorit_product.save()
                return Response({'status': 'product changed successfully'})
            else:
                Favorite.objects.create(
                    product=product_obj, user=user, isFavorit=True)
            response_msg = {'Status': 'product added to favorite successfully'}
        except:
            response_msg = {'error': "error when added product to favorite"}
        return Response(response_msg)
    
    def get(self , request):
        query = Favorite.objects.filter(user=request.user).filter(isFavorit=True)
        fav_obj = FavoriteSerializer(query , many=True) 
        return Response({'data':fav_obj.data})
       
        



    
