from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import check_password
from .models import User, Contact, SpamReport
from .serializers import UserSerializer, ContactSerializer, SpamReportSerializer,SearchResultSerializer

from django.db.models import Q, Count


# Register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"error": "User already exists"}, status=400)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data}, status=201)

# Login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not phone_number or not password:
            return Response({"error": "Phone number and password required"}, status=400)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if not user.check_password(password):
            return Response({"error": "Incorrect password"}, status=401)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data})

# Protected Views
class ContactListView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

class SpamReportListView(generics.ListCreateAPIView):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    permission_classes = [IsAuthenticated]

class SpamCheckView(APIView):
    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number required'}, status=status.HTTP_400_BAD_REQUEST)

        spam_count = SpamReport.objects.filter(phone_number=phone_number).count()
        is_spam = spam_count > 0

        return Response({
            'phone_number': phone_number,
            'is_spam': is_spam,
            'spam_count': spam_count
        })

class SearchByNameView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get("query", "").strip()
        if not query:
            return Response({"error": "Query param required."}, status=400)

        # First: registered users
        registered_users_start = User.objects.filter(name__istartswith=query)
        registered_users_contains = User.objects.filter(name__icontains=query).exclude(id__in=registered_users_start)

        # Then: contacts (excluding duplicates of registered users)
        contact_users_start = Contact.objects.filter(name__istartswith=query).exclude(
            phone_number__in=User.objects.values_list('phone_number', flat=True)
        )
        contact_users_contains = Contact.objects.filter(name__icontains=query).exclude(
            Q(id__in=contact_users_start) |
            Q(phone_number__in=User.objects.values_list('phone_number', flat=True))
        )

        results = []

        # Registered Users
        for user in registered_users_start.union(registered_users_contains):
            spam_count = SpamReport.objects.filter(phone_number=user.phone_number).count()
            results.append({
                "name": user.name,
                "phone_number": user.phone_number,
                "spam_likelihood": spam_count,
            })

        # Contacts
        for contact in contact_users_start.union(contact_users_contains):
            spam_count = SpamReport.objects.filter(phone_number=contact.phone_number).count()
            results.append({
                "name": contact.name,
                "phone_number": contact.phone_number,
                "spam_likelihood": spam_count,
            })

        return Response(results)

class SearchByPhoneNumberView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        number = request.GET.get("phone", "").strip()
        if not number:
            return Response({"error": "Phone param required."}, status=400)

        result = []

        # Check if the phone number belongs to a registered user
        try:
            user = User.objects.get(phone_number=number)
            spam_count = SpamReport.objects.filter(phone_number=number).count()

            # Check if the requester is in their contacts
            is_in_contact = Contact.objects.filter(user=user, phone_number=request.user.phone_number).exists()

            result.append({
                "name": user.name,
                "phone_number": user.phone_number,
                "spam_likelihood": spam_count,
                "email": user.email if is_in_contact else None,
                "is_registered_user": True
            })

        except User.DoesNotExist:
            # Not a registered user, look in contacts
            contacts = Contact.objects.filter(phone_number=number)
            for contact in contacts:
                spam_count = SpamReport.objects.filter(phone_number=contact.phone_number).count()
                result.append({
                    "name": contact.name,
                    "phone_number": contact.phone_number,
                    "spam_likelihood": spam_count,
                    "email": None,
                    "is_registered_user": False
                })

        return Response(result)
class MarkSpamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        number = request.data.get("phone_number", "").strip()

        if not number:
            return Response({"error": "Phone number is required"}, status=400)

        # Prevent self-marking
        if request.user.phone_number == number:
            return Response({"error": "You can't mark your own number as spam"}, status=400)

        # Prevent duplicate reports
        if SpamReport.objects.filter(reporter=request.user, phone_number=number).exists():
            return Response({"error": "Already reported"}, status=400)

        SpamReport.objects.create(reporter=request.user, phone_number=number)

        # Update spam_count
        User.objects.filter(phone_number=number).update(spam_count=F('spam_count') + 1)
        Contact.objects.filter(phone_number=number).update(spam_count=F('spam_count') + 1)

        return Response({"message": "Number marked as spam successfully"})


