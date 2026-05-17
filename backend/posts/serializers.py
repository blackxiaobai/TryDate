from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_display = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_display', 'content', 'is_anonymous', 'created_at']
        read_only_fields = ['id', 'post', 'created_at']

    def get_author_display(self, obj):
        if obj.is_anonymous:
            return '匿名用户'
        return obj.author.nickname

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author_display = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author_display', 'is_anonymous', 'content', 'like_count', 'is_liked', 'is_owner', 'comment_count', 'created_at']
        read_only_fields = ['id', 'like_count', 'created_at']

    def get_author_display(self, obj):
        if obj.is_anonymous:
            return '匿名用户'
        return obj.author.nickname

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author_id == request.user.id
        return False

    def get_comment_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
