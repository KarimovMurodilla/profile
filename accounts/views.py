from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Comment, CustomUser
from .serializers import CommentSerializer, ProfileSerializer


# Create your views here.

#Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
        '/api/prediction/'
        'api/comments/',
        'api/comments/create/<int:pk>',
        'api/profile/',
        'api/profile/update/',
        'api/users/<int:pk>/comments/',

    ]
    return Response(routes)

#api/comments
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getComments(request):
    user_comments = request.user.comments.all().order_by('-updated')[:10]
    comments = user_comments
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


#api/comments/create/<int:pk>
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createComment(request, pk):
    profile_owner = CustomUser.objects.get(id=pk)
    user = request.user
    data = request.data
    comment = Comment.objects.create(
        user=profile_owner,
        commentator=user,
        title=data['title'],
        body=data['body'],
    )
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data)


#api/profile  and api/profile/update
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



#api/comments/user/<int:pk>/mycomments
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserComments(request, pk):
    user = CustomUser.objects.get(id=pk)
    comments = Comment.objects.filter(user=user)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

