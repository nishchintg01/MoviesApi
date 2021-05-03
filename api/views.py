import requests
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .serializers import CollectionSerializers, SignupSerializer
from rest_framework import serializers, permissions, status, viewsets
from .models import Collections
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from requests.auth import HTTPBasicAuth
from .utils import get_tokens_for_user

class RegisterUsers(CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        serialized_user = SignupSerializer(data=request.data)
        if serialized_user.is_valid():
            data = User.objects.create_user(
                serialized_user.initial_data['username'],
            )
            data.set_password(serialized_user.initial_data['password'])
            print(data)
            data.save()
            token = get_tokens_for_user(data)
            return Response(token, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_user._errors, status=status.HTTP_400_BAD_REQUEST)


class GetMoviesList(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        url = "https://demo.credy.in/api/v1/maya/movies/"
        username = "iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0"
        password = "Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"
        response = requests.get(url ,auth = HTTPBasicAuth(username, password))
        return JsonResponse(response.json(), safe=False)

       
        
class ColectionsViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    """
    A simple ViewSet for listing, retrieving, deleting and editing collections objects.
    """
    def list(self, request):
        queryset = Collections.objects.filter(user = request.user)
        serializer = CollectionSerializers(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def retrieve(self, request, pk = None):
        try:
            data = Collections.objects.get(uuid = pk)
            serializer = CollectionSerializers(data)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"data could not be Fetched"}, status = status.HTTP_400_BAD_REQUEST)
    
    def create(self, request):
        print(request.data)
        try:
            data = Collections(
                user = request.user,
                Title = request.data['title'],
                Description = request.data['description'],
                Movies = request.data['movies']
            )
            data.save()
            return Response({"collection_uuid": data.uuid}, status = status.HTTP_201_CREATED )
        except Exception as e:
            print(e)     
            return Response({"error":"data could not be saved"}, status = status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk = None):
        try:
            data = Collections.objects.get(uuid = pk)
            data.Title = request.data['title']
            data.Description = request.data['description']
            data.Movies = request.data['movies']
            data.save()
            serializer = CollectionSerializers(data, many = False)
            return Response({"collection_uuid": serializer.data }, status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e)     
            return Response({"error":"data could not be saved"}, status = status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk = None):
        try:
            collection = Collections.objects.get(uuid = pk)
            collection.delete()
            return Response({"success":"Collection has been removed"}, status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"error":"Bad Request"}, status = status.HTTP_400_BAD_REQUEST)
        