"""
Views for Recipe API
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication, get_user_model
from rest_framework.permissions import IsAuthenticated

from core.models import Ingredient, Recipe, Tag
from recipe import serializers

#Viewset made to work directly with models
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.RecipeDetailSerializer

    #Objects available for this
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #Filter recipes to authenticated user
    def get_queryset(self):
        """Retreive recipes as saved in queryset above for authenticated users"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    #Return detail serializer for most things but return recipe serializer for list outputs
    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    #Assign user id to new recipes
    def perform_create(self, serializer):
        """Create a new Recipe"""
        serializer.save(user=self.request.user)

#GenericViewSet allows mixins integration
#Mixins provides additional functionalities
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base Viewset for recipe attributes"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    serializer_class = serializers.TagSerializer
    queryset =  Tag.objects.all()

class IngredientViewSet(BaseRecipeAttrViewSet):
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
