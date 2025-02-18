from rest_framework import viewsets
from categoryapp.models import Category
from categoryapp.serializer import CategorySerializer

# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # CRUD metotlar, dinamik olarak gelir. override edebilirsiniz 
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)
