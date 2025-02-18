from rest_framework import serializers
from categoryapp.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = "__all__"
        fields = ["name", "description", "created_at"]

        # select * from categories -> __all__
        # select name, description from categories -> ["name", "description"]
