from rest_framework import serializers
from .models import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    profile = ProfileSerializer()
    class Meta:
        model = Post
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = "__all__"

class SubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub
        fields = "__all__"

class SectionSerializer(serializers.ModelSerializer):
    blogpost = PostSerializer()
    class Meta:
        model = Section
        fields = "__all__"

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)