from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.models import AuthToken 
from .serializers import *
from django.contrib.auth import login
from .models import *
from rest_framework.filters import SearchFilter 
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import pagination

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'count'
    max_page_size = 10
    page_query_param = 'page'

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


class ListCategory(APIView):
    #permission_classes = [permissions.IsAuthenticated, ]
    
    def get(self,request):
        queryset = Category.objects.all()
        serializer_class = CategorySerializer(queryset,many=True)
        return Response(serializer_class.data)
        


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
                product['favorite'] = fab_query[0].isFavorite
            else:
                product['favorite'] = False
            data.append(product)
       
        return  Response(data)



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
                isFav = single_favorit_product.isFavorite
                single_favorit_product.isFavorite = not isFav
                single_favorit_product.save()
                if isFav: 
                    return Response({'status': 'remove from favorite'}) 
                return Response({'status': 'product added to favorite'})
            else:
                Favorite.objects.create(
                    product=product_obj, user=user, isFavorite=True)
            response_msg = {'status': 'product added to favorite'}
        except:
            response_msg = {'error': "error when added product to favorite"}
        return Response(response_msg)
    
    def get(self , request):
        query = Favorite.objects.filter(user=request.user).filter(isFavorite=True)
        fav_obj = FavoriteSerializer(query , many=True) 
        return Response(fav_obj.data)
       
        

class ProductByCategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get(self,request):

        #category_id = request.data['category_id']
    
        category_id = request.query_params.get('category_id')

        query = Product.objects.filter(category=category_id)
        serializers = ProductSerializer(query,many=True)

        data = []
        for product in serializers.data:
            fab_query = Favorite.objects.filter(
                user=request.user).filter(product_id=product['id'])
            if fab_query:
                product['favorite'] = fab_query[0].isFavorite
            else:
                product['favorite'] = False
            data.append(product)
       
        return Response(data)



class SearchView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class=None
    filter_backends = [DjangoFilterBackend,SearchFilter] 
    search_fields = ['title']


class PoductViewPagination(APIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request):
        queryset = Product.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            for product in serializer.data:
                fab_query = Favorite.objects.filter(
                user=request.user).filter(product_id=product['id'])
                if fab_query:
                    product['favorite'] = fab_query[0].isFavorite
                else:
                    product['favorite'] = False
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CartView(APIView):

    def get(self, request):
        query = CartItem.objects.filter(user=request.user)
        serializers = CartItemSerializer(query,many=True)

        total_price = 0.0
        total_price_old = 0.0
        for product in serializers.data:
            total_price += product['total_price']
            total_price_old += product['total_price_old']
            
        return Response({'total_price':total_price ,'total_price_old':total_price_old, 'data' : serializers.data})


class AddToCart(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    def post(self, request):
        prod_id = request.data['product_id']
        quantity = request.data['quantity']
        try:
            prod_obj = Product.objects.get(id=prod_id)
            check_in_cart = CartItem.objects.filter(
                user=request.user).filter(product=prod_obj).first()

            if check_in_cart:
                return  Response({'status':'already in cart'})

            total_price  = float(prod_obj.new_price) * float(quantity)
            total_price_old = float(prod_obj.old_price) * float(quantity)
            CartItem.objects.create(
                product=prod_obj,
                user=request.user,
                quantity= quantity,
                total_price = total_price,
                total_price_old = total_price_old,
            )
            return Response({'status':'added to cart successfully'})
        except:
            print("is here")
            response_msg ='error when added to cart'
        return Response({'status':response_msg})

        
'''class CartItemAddView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemAddSerializer
    pagination_class=None
    #permission_classes = (permissions.IsAuthenticated, )'''


'''class CartItemView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    #permission_classes = (permissions.IsAuthenticated, )
    filter_backends = [SearchFilter]
    pagination_class=None
    search_fields = [
        'product__name', 'product__description', 'product__category__name']

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)
'''


class CartItemAddOneView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    pagination_class=None

    def get(self, request, pk, format=None):
        user = request.user
        cart_item = CartItem.objects.filter(user=user)
        target_product = cart_item.get(pk=pk)

        target_product.quantity = target_product.quantity + 1
        target_product.total_price += target_product.product.new_price
        target_product.total_price_old += target_product.product.old_price
        target_product.save()
        return Response(
            data={"detail": 'added one quantity',})



class CartItemReduceOneView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    pagination_class=None
    def get(self, request, pk, format=None):
        user = request.user
        cart_item = CartItem.objects.filter(user=user)
        target_product = cart_item.get(pk=pk)


        if target_product.quantity <= 1 :
            return Response(data={"detail":"no quantity to reduce"})

        target_product.quantity = target_product.quantity - 1

        target_product.total_price -= target_product.product.new_price
        target_product.total_price_old -= target_product.product.old_price
    
        target_product.save()
        return Response(
            data={
                "detail": 'one object deleted',
            })


class CartItemDelView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = CartItem.objects.all()
    pagination_class=None
    def get(self, request, pk, format=None):
        user = request.user
        cart_item = CartItem.objects.filter(user=user)
        target_product = get_object_or_404(cart_item, pk=pk)
        target_product.delete()
        return Response(data={"detail": "deleted"})


