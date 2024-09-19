# socialnetwork/urls.py

from django.urls import path

from .views import CheckEmailVerificationView, CustomUserSignUpView, LoginView, VerifyEmailView

urlpatterns = [
    # Authentication endpoints
    path('login/', LoginView.as_view(), name='user_login'),
    path('signup/', CustomUserSignUpView.as_view(), name='user_signup'),

    # Email verification endpoint
    path('api/verify-email/<uuid:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('check-email-verification/', CheckEmailVerificationView.as_view(), name='check_email_verification'),

    # User-related endpoints
    # path('search/', UserSearchView.as_view(), name='user_search'),  # User search
    # path('friend-requests/', FriendRequestView.as_view(), name='friend_requests'),  # Manage friend requests
    # path('friends/', FriendListView.as_view(), name='friend_list'),  # List friends
    # path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending_friend_requests'),  # Pending friend requests
    # path('block-user/', BlockUserView.as_view(), name='block_user'),  # Block/unblock user
]
