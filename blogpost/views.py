from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAdminOrReadOnly
from rest_framework.pagination import PageNumberPagination

import bleach
from rest_framework.authtoken.models import Token




from .models import *

class PostPagination(PageNumberPagination):
    page_size = 10  # Set the number of items per page


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Authentication successful
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'TagList': '/tag-list/',
        'ProfileList': '/profile-list/',
        'TagCreate': '/tag-create/',
        'TagDetail': '/tag-detail/<str:pk>/',
        'TagUpdate': '/tag-update/<str:pk>/',
        'TagDelete': '/tag-delete/<str:pk>/',
        'PostList': '/post-list/',
        'PostCreate': '/post-create/',
        'PostDetail': '/post-detail/<str:pk>/',
        'PostUpdate': '/post-update/<str:pk>/',
        'PostDelete': '/post-delete/<str:pk>/',
        'CommentList': '/comment-list/',
        'CommentCreate': '/comment-create/',
        'CommentDetail': '/comment-detail/<str:pk>/',
        'CommentDelete': '/comment-delete/<str:pk>/',
        'SectionList': '/section-list/<str:pk>/',
        'SectionCreate': '/section-create/',
        'SectionDelete': '/section-delete/<str:pk>/',
        'replyList': '/reply-list/<str:pk>/',
        'replyCreate': '/reply-create/',
        'replyDelete': '/reply-delete/<str:pk>/',
    }
    return Response(api_urls)


@api_view(['GET'])
def postPagList(request):
    post = Post.objects.filter(isPublished = True).order_by('-timestamp')
    paginator = PostPagination()
    result_page = paginator.paginate_queryset(post, request)

    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)



@api_view(['GET'])
def sectionPhoto(request, pk):
    section = Section.objects.get(id=pk)
    image_path = section.secimg.path

    with open(image_path, 'rb') as image_file:
        return HttpResponse(image_file.read(), content_type='image/jpeg')

@api_view(['GET'])
def postPhoto(request, pk):
    post = Post.objects.get(id=pk)
    image_path = post.headimg.path

    with open(image_path, 'rb') as image_file:
        return HttpResponse(image_file.read(), content_type='image/jpeg')
    
@api_view(['GET'])
def profilePhoto(request, pk):
    dp = Profile.objects.get(id=pk)
    image_path = dp.displaypic.path

    with open(image_path, 'rb') as image_file:
        return HttpResponse(image_file.read(), content_type='image/jpeg')


@api_view(['GET'])
def sectionList(request, pk):
    post = Post.objects.get(id=pk)
    section = Section.objects.filter(blogpost = post)
    serializer = SectionSerializer(section, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated | IsAdminOrReadOnly])
def sectionCreate(request):
    serializer = SectionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated | IsAdminOrReadOnly])
def sectionDelete(request, pk):
    section = Section.objects.get(id=pk)
    section.delete()

    return Response('Deleted')


@api_view(['GET'])
def replyList(request, pk):
    comment = Comment.objects.get(id=pk)
    reply = Reply.objects.filter(comment = comment)
    serializer = ReplySerializer(reply, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def profileList(request):
    profile = Profile.objects.all()
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def replyCreate(request):
    serializer = ReplySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated | IsAdminOrReadOnly])
def replyDelete(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.delete()

    return Response('Deleted')


@api_view(['GET'])
def commentList(request, pk):
    post = Post.objects.get(id=pk)
    comment = Comment.objects.filter(post = post).order_by('-date')
    serializer = CommentSerializer(comment, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def commentDetail(request, pk):
    comment = Comment.objects.get(id=pk)
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def commentCreate(request):
    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated | IsAdminOrReadOnly])
def commentDelete(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()

    return Response('Deleted')

@api_view(['GET'])
def postList(request):
    post = Post.objects.filter(isPublished = True).order_by('-timestamp')
    
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def styleList(request):
    styles = Tag.objects.get(tag = "Style")
    post = Post.objects.filter(isPublished = True, tag = styles).order_by('-timestamp')
    paginator = PostPagination()
    result_page = paginator.paginate_queryset(post, request)
    
    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def designList(request):
    design = Tag.objects.get(tag = "Design")
    post = Post.objects.filter(isPublished = True, tag = design).order_by('-timestamp')
    paginator = PostPagination()
    result_page = paginator.paginate_queryset(post, request)
    
    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def foodList(request):
    food = Tag.objects.get(tag = "Food")
    post = Post.objects.filter(isPublished = True, tag = food).order_by('-timestamp')
    paginator = PostPagination()
    result_page = paginator.paginate_queryset(post, request)
    
    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def relationshipList(request):
    relationship = Tag.objects.get(tag = "Relationship")
    post = Post.objects.filter(isPublished = True, tag = relationship).order_by('-timestamp')
    paginator = PostPagination()
    result_page = paginator.paginate_queryset(post, request)
    
    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def wellbeingList(request):
    wellbeing = Tag.objects.get(tag = "Wellbeing")
    post = Post.objects.filter(isPublished = True, tag = wellbeing).order_by('-timestamp')
    paginator = PostPagination()
    result_page = paginator.paginate_queryset(post, request)
    
    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def postListTrend(request):
    post = Post.objects.filter(isPublished = True).order_by('-views')
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def postListRand(request):
    post = Post.objects.filter(isPublished = True).order_by('?')[:9]
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def postListComment(request):
    post = Post.objects.filter(isPublished = True).order_by('-totalcount')[:10]
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def postDetail(request, pk):
    post = Post.objects.get(slug=pk, isPublished=True)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated | IsAdminOrReadOnly])
def postCreate(request):
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated | IsAdminOrReadOnly])
def postUpdate(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(instance=post, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated | IsAdminOrReadOnly])
def postDelete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()

    return Response('Deleted')



@api_view(['GET'])
def tagList(request):
    tag = Tag.objects.all()
    serializer = TagSerializer(tag, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def tagDetail(request, pk):
    tag = Tag.objects.get(id=pk)
    serializer = TagSerializer(tag, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated | IsAdminOrReadOnly])
def tagCreate(request):
    serializer = TagSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated | IsAdminOrReadOnly])
def tagUpdate(request, pk):
    tag = Tag.objects.get(id=pk)
    serializer = TagSerializer(instance=tag, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated | IsAdminOrReadOnly])
def tagDelete(request, pk):
    tag = Tag.objects.get(id=pk)
    tag.delete()

    return Response('Deleted')
