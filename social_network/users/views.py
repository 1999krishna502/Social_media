from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings

from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER



class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Check if the login is successful
        if response.status_code == status.HTTP_200_OK:
            # Get user object based on the provided email
            user = CustomUser.objects.get(email=request.data['email'])

            # Check and update the verification status
            if not user.is_verified:
                user.is_verified = True
                user.save()

                print(f"User {user.email} is now verified after login.")

        return response

class CustomUserSignUpView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        # Send verification email
        self.send_verification_email(user)

    def send_verification_email(self, user):
        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        verification_link = f'http://{current_site.domain}/api/verify-email/{user.verification_token}/'

        message = f'Hi {user.email},\n\nPlease click the following link to activate your account:\n\n{verification_link}'

        send_mail(
            subject,
            message,
            'akkunni222@gmail.com',  # Replace with your sender email
            [user.email],
            fail_silently=False,
        )

        user.email_user(subject, message)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            user = CustomUser.objects.get(verification_token=token)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.verification_token = None
        user.save()

        print(f"User {user.email} is now verified.")

        return Response({'message': 'Email verification successful'}, status=status.HTTP_200_OK)





class CheckEmailVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Assuming the user is authenticated
        try:
            # Assuming the user is a CustomUser model
            user = CustomUser.objects.get(id=user.id)
            is_verified = user.is_verified

            if is_verified:
                return Response({'message': 'Email is verified'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Email is not verified'}, status=status.HTTP_403_FORBIDDEN)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# class UserSearchView(generics.ListAPIView):
#     serializer_class = CustomUserSerializer

#     def get_queryset(self):
#         query = self.request.query_params.get('q', '')
#         return CustomUser.objects.filter(
#             Q(email__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
#         )


# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import action

# class FriendRequestViewSet(viewsets.ViewSet):
    
#     @action(detail=False, methods=['post'])
#     def send_request(self, request):
#         # Logic to send friend request
#         pass
    
#     @action(detail=False, methods=['post'])
#     def accept_request(self, request):
#         # Logic to accept friend request
#         pass
    
#     @action(detail=False, methods=['post'])
#     def reject_request(self, request):
#         # Logic to reject friend request
#         pass

# # users/views.py

# class FriendsListView(generics.ListAPIView):
#     serializer_class = CustomUserSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return user.friends.all()

# class PendingRequestsView(generics.ListAPIView):
#     serializer_class = CustomUserSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return user.pending_requests.all()
