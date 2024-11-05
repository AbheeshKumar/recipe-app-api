"""
Views for Recipe API
"""

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
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
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    #Assign user id to new recipes
    def perform_create(self, serializer):
        """Create a new Recipe"""
        serializer.save(user=self.request.user)

    #Custom action for uploading image API that only accepts POST request
    @action(methods=['POST'], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload image to recipe"""
        #Get recipe obj through pk
        recipe = self.get_object()
        #Get RecipeImageSerializer
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
