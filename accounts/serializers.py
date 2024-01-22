from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.conf import settings

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }


    def get_user(self, data):
        email = data.get("email")
        password = data.get("password")
        return authenticate(email=email, password=password)


    def validate(self, attrs):
        user = self.get_user(attrs)

        if not user:
            raise serializers.ValidationError({"error": "Email or password is wrong"})

        if not user.is_active:
            raise serializers.ValidationError({"error": "This account is not activated"})

        return attrs


    def create(self, validated_data):
        return self.get_user(validated_data)


    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            'refresh': str(token),
            'access': str(token.access_token),
        }
        return repr_



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email", "name", "surname", "mobile",
            "password", "password_confirm"
        )


    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Account with this email already exists"})

        if len(password) < 6:
            raise serializers.ValidationError({"error": "Password should contain 6 symbols at least"})

        if password_confirm != password:
            raise serializers.ValidationError({"error": "Passwords should match"})
        
        return super().validate(attrs)


    def create(self, validated_data):
        request = self.context.get("request")
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User(**validated_data, is_active=False)
        user.set_password(password)
        user.save()

        # sending verification mail
        uuid = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        # example front link
        # link = azxeber.com/verify/?uuid=<uuid>&token=<token>
        link = request.build_absolute_uri(reverse_lazy("accounts:activation", kwargs={"uuid": uuid, "token": token}))
        html_content = render_to_string("mail/activation.html", {"link": link})
        msg = EmailMultiAlternatives(
            "Activition mail | AzXeber.com",
            html_content,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return user



class ActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "surname", "mobile")
        extra_kwargs = {
            "email": {"read_only": True},
            "name": {"read_only": True},
            "surname": {"read_only": True},
            "mobile": {"read_only": True}
        }


    def create(self, validated_data):
        uuid = self.context.get("uuid")
        token = self.context.get("token")

        id = smart_str(urlsafe_base64_decode(uuid))
        user = User.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({"error": "Wrong credentials"})

        user.is_active = True
        user.save()
        return user


    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            'refresh': str(token),
            'access': str(token.access_token),
        }
        return repr_



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "surname", "email", "mobile")