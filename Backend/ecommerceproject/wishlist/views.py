from django.shortcuts import render
from .models import wishlist
from .serializers import wishlistSerializer,wishlistListSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import DestroyAPIView,ListAPIView
from product.models import Product
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND


class wishlistAddView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,*args,**kwargs):
        serializer=wishlistSerializer(data=request.data)
        id=kwargs.get("id")
        product=Product.objects.get(id=id)
        user=request.user
        serializer.is_valid(raise_exception=True)  
        try:
             wishlist=wishlist.objects.get(product=product,user=user)
             wishlist.quantity+=1
             wishlist.save()
             data={"message":"success"}
             return Response(data)

        except:
            serializer.save(user=user,product=product)
            return Response(serializer.data)


class wishlistListView(ListAPIView):

    serializer_class=wishlistListSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        user=self.request.user
        wishlist=user.wishlist_set.all()
        return wishlist

class wishlistRemoveView(DestroyAPIView):
    serializer_class=wishlistSerializer
    permission_classes=[IsAuthenticated]
    lookup_url_kwarg="id"
    
    def delete(self, request, *args, **kwargs):
        id=kwargs.get("id")
        try:
            user=request.user
            wishlistitem=user.wishlist_set.get(id=id)
            wishlistitem.delete()
            return Response({"message":"item removed successfully"})
        except:
            return Response({
                "message":"no such item"
            },status=HTTP_404_NOT_FOUND)