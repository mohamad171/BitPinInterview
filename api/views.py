from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Q
from asgiref.sync import async_to_sync
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .serializer import *
class Signin(APIView):
    def post(self,request):
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        user = authenticate(username=username,password=password)
        if user:
            serializer = UserSerializer(instance=user)
            data = serializer.data
            token, created = Token.objects.get_or_create(user=user)
            data["token"] = token.key if token else created.key
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"status":"faild","message":"Invalid username or password"},status=400)
class SignUp(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.instance
            data = serializer.data
            token, created = Token.objects.get_or_create(user=user)
            data["token"] = token.key if token else created.key
            return JsonResponse(data,safe=False)

class PostsView(generics.GenericAPIView,mixins.ListModelMixin):
    """
            Get List of posts
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer
    queryset = Post.objects.filter()
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

class PostsDetailsView(generics.GenericAPIView,mixins.RetrieveModelMixin):
    """
            Get details of specific post
        """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer
    queryset = Post.objects.filter()
    lookup_field = "id"
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

class SubmitRate(APIView):
    """
        Submit rate for specific post
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,id):
        rate = request.POST.get("rate",5)
        rate = int(rate)
        post = get_object_or_404(Post,id=id)
        if  rate <= 0 or rate >= 6:
            return JsonResponse({"status":"faild","message":"Rate should be in range 1-5"},status=403)

        post_rate = Rate.objects.filter(user=request.user,post=post).first()
        if post_rate:
            post_rate.rate_number = rate
            post_rate.save()
        else:
            Rate.objects.create(user=request.user,post=post,rate_number=rate)

        return JsonResponse({"status":"ok"},safe=False)

