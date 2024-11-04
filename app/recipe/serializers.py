"""
Serializers for Recipe API
"""

from rest_framework import serializers
from core.models import Recipe, Tag

#Serializer for an specific Model
class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""
    class Meta:
        model= Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed"""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def create(self, validated_data):
        """Create a recipe"""
        #Store data in tags and delete from validated_data
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        #Create tag objects and add in recipe
        self._get_or_create_tags(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe"""
        tags = validated_data.pop('tags', None)

        #Clear and add the new tags
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        #Add the remaining data minus tags to recipe
        for attr, value in validated_data.items():
            setattr(instance,attr,value)

        instance.save()

        return instance



#RecipeDetailSerializer is an extension(subclass) of RecipeSerializer
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view"""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']