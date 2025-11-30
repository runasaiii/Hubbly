#Django modules
'''from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

import random
from faker import Faker

#Project modules
from apps.users.models import User,Profile
from apps.communities.models import Community,CommunityMembership
from apps.events.models import Event,EventApplication
from apps.posts.models import Post,Tag,Comment

class Command(BaseCommand):
    help = 'fill the database with simple data for testing'

    @transaction.atomic
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action = 'store_true',
            help = 'Clear the database before seeding',
        )

    def handle(self, *args, **options):
        fake = Faker()
        clear = options,get('clear')

        if clear:
            self.stdout.write('Clearing data')
            Comment.objects.all().delete()
            Post.objects.all().delete()
            Tag.objects.all().delete()
            EventApplications.objectsc.all().delete()
            Event.objects.all().delete()
            CommunityMembership.objects.all().delete()
            Community.objects.all().delete()
            Profile.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()
    
        self.stdout.write('Creating users')
        users = []
        for i in range(25):
            email = f'user{i}@example.com'
            username = f'user{i}'
            user, _ = User.objects.get_or_create(
                email = email,defaults = {
                    'username': username,
                    'is_active': True,
                }
            )
            user.set_password('password')
            user.save()
            Profile.objects.get_or_create( user = user, defaults = {
                'display_name': fake.name(),
                'bio': fake.sentence(nb_words = 100),
                'location': fake.city(),
                'interests': [fake.word() for _ in range(5)],
                'is_verified': random.choice([True, False]),
                'avatar': fake.image_url(),
            })
            users.append(user)

        self.stdout.write('Creating communities and memberships')
        communities = []
        for i in range(20):
            name = f'{fake.word().capitalize()}Community {i}'
            slug = f'community-{i}-{random.randint(1000,9999)}'
            owner = random.choice(users)
            community, _ = Community.objects.get_or_create(slug = slug, defaults = {
                'name': name,
                'description': fake.paragraph(nb_sentence= 50),
                'visibility': random.choice(['public', 'private','secret']),
                'owner': owner,

            })
            communities.append(community)

            # Create memberships
            member_sample = random.sample(users, k =min(15, len(users)))
            for idx, member in enumerate(member_sample):
                CommunityMembership.objects.get_or_create(user = member, community = community, defaults = {
                    'role': 'organizer' if member == owner else random.choice(['member','moderator]),
                    'status': random.choice(['active','pending','banned']),'''
            



        


