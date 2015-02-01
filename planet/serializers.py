from rest_framework import serializers
from planet.models import Blog, Post, Feed,Category

class CategorySerializer(serializers.ModelSerializer):
	#posts=serializers.RelatedField(many=True)
	class Meta:
		model=Category
		fields=('title',)
		

class PostSerializer(serializers.ModelSerializer):
	category=serializers.SlugRelatedField(slug_field='title')
	feed=serializers.SlugRelatedField(slug_field='title')
	class Meta:
		model=Post
		fields=('title','url','content','feed','category','date_created','cluster_id','rank','image_url')

class FeedSerializer(serializers.ModelSerializer):
	posts=serializers.RelatedField(many=True)

	class Meta:
		model=Feed
		fields=('title','posts')
		

