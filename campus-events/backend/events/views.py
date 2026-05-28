from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Activity, Comment, Favorite, Registration
from .serializers import ActivitySerializer, CommentSerializer, UserSerializer

class ActivityList(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def list(self, request):
        queryset = self.get_queryset()
        search = request.query_params.get('search', '')
        category = request.query_params.get('category', '')
        
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(description__icontains=search)
        if category and category != 'all':
            queryset = queryset.filter(category=category)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        activity = get_object_or_404(Activity, pk=self.kwargs['pk'])
        return activity.comments.all()
    
    def perform_create(self, serializer):
        activity = get_object_or_404(Activity, pk=self.kwargs['pk'])
        serializer.save(activity=activity)

class FavoriteView(generics.GenericAPIView):
    def post(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        user_id = request.data.get('user_id')
        
        if Favorite.objects.filter(activity=activity, user_id=user_id).exists():
            return Response({'status': 'already favorited'}, status=status.HTTP_400_BAD_REQUEST)
        
        Favorite.objects.create(activity=activity, user_id=user_id)
        return Response({'status': 'success'})
    
    def delete(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        user_id = request.data.get('user_id')
        
        favorite = Favorite.objects.filter(activity=activity, user_id=user_id).first()
        if not favorite:
            return Response({'status': 'not favorited'}, status=status.HTTP_400_BAD_REQUEST)
        
        favorite.delete()
        return Response({'status': 'success'})

class RegistrationView(generics.GenericAPIView):
    def post(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        user_id = request.data.get('user_id')
        
        if Registration.objects.filter(activity=activity, user_id=user_id).exists():
            return Response({'status': 'already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        Registration.objects.create(activity=activity, user_id=user_id)
        return Response({'status': 'success'})
    
    def delete(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        user_id = request.data.get('user_id')
        
        registration = Registration.objects.filter(activity=activity, user_id=user_id).first()
        if not registration:
            return Response({'status': 'not registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        registration.delete()
        return Response({'status': 'success'})

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'status': 'success'
        })
    else:
        return Response({'status': 'failed', 'message': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({'status': 'failed', 'message': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({'status': 'failed', 'message': '邮箱已被注册'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'status': 'success'
    })
