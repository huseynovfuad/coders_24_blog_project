from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer, ActivationSerializer
from django.contrib.auth import get_user_model


User = get_user_model()



class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ActivationView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ActivationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context=kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)