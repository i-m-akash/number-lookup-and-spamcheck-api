from django.core.management.base import BaseCommand
from core.models import User, Contact, SpamReport
from django.contrib.auth import get_user_model
from faker import Faker
import random
from django.db import models


UserModel = get_user_model()

class Command(BaseCommand):
    help = 'Populate sample users, contacts, and spam reports'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = []

        # Create 100 users
        for _ in range(100):
            name = fake.name()
            phone = fake.unique.phone_number()
            email = fake.email()
            user = UserModel.objects.create_user(
                phone_number=phone,
                name=name,
                password='password123',
                email=email
            )
            users.append(user)

        self.stdout.write("✅ Created 100 users.")

        # Each user gets 10 contacts
        for user in users:
            for _ in range(10):
                contact = Contact.objects.create(
                    user=user,
                    name=fake.name(),
                    phone_number=fake.phone_number()
                )
        self.stdout.write("📇 Added contacts for each user.")

        # Randomly mark 300 numbers as spam
        all_numbers = list(UserModel.objects.values_list("phone_number", flat=True))
        for _ in range(300):
            reporter = random.choice(users)
            number = random.choice(all_numbers)
            if number != reporter.phone_number and not SpamReport.objects.filter(reported_by=reporter, phone_number=number).exists():
                SpamReport.objects.create(reported_by=reporter, phone_number=number)
                # Also increment spam_count
                UserModel.objects.filter(phone_number=number).update(spam_count=models.F('spam_count') + 1)
                Contact.objects.filter(phone_number=number).update(spam_count=models.F('spam_count') + 1)

        self.stdout.write("🚨 300 random spam reports added.")
        self.stdout.write(self.style.SUCCESS("🎉 Data population complete!"))
