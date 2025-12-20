# Python modules
from typing import Any
from random import choice, randint, sample
from datetime import datetime

# Django modules
from django.core.management.base import BaseCommand

# Project modules
from apps.communities.models import Community, CommunityMembership
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Generate communities and memberships for testing"

    COMMUNITY_NAMES = [
        "Tech Enthusiasts", "Art Lovers", "Music Fans", "Sports Club",
        "Travel Adventures", "Food Critics", "Photography Hub", "Design Studio",
        "Code Masters", "Science Forum", "Book Club", "Gaming Community",
        "Fitness Group", "Business Network", "Creative Minds", "Startup Hub",
        "Developer Community", "Data Science", "AI Research", "Web Designers"
    ]

    DESCRIPTIONS = [
        "A community for passionate enthusiasts to share ideas and connect.",
        "Join us to discuss and explore our shared interests together.",
        "A welcoming space for members to learn and grow together.",
        "Connect with like-minded people and build meaningful relationships.",
        "Share your experiences and learn from others in this community.",
    ]

    def __generate_communities(self, community_count: int = 100) -> list[Community]:
        users = list(CustomUser.objects.all())
        
        if not users:
            self.stdout.write(self.style.ERROR("No users r found. Create users first"))
            return []
        
        communities_before = Community.objects.count()
        created_communities = []
        
        for i in range(community_count):
            owner = choice(users)
            name = choice(self.COMMUNITY_NAMES) + f" {i+1}"
            description = choice(self.DESCRIPTIONS)
            visibility = choice(['public', 'private', 'secret'])
            
            community = Community.objects.create(
                name=name,
                description=description,
                visibility=visibility,
                owner=owner
            )
            created_communities.append(community)
        
        communities_after = Community.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Created {communities_after - communities_before} communities.")
        )
        return created_communities

    def __generate_memberships(self, membership_count: int = 500) -> None:
        communities = list(Community.objects.all())
        users = list(CustomUser.objects.all())
        
        if not communities or not users:
            return
        
        memberships_before = CommunityMembership.objects.count()
        created_memberships = []
        
        for i in range(membership_count):
            community = choice(communities)
            user = choice(users)
            
            if user == community.owner:
                role = 'organizer'
                status = 'active'
            else:
                role = choice(['member', 'moderator', 'organizer'])
                status = choice(['pending', 'active', 'banned'])
            
            if not CommunityMembership.objects.filter(user=user, community=community).exists():
                membership = CommunityMembership(
                    user=user,
                    community=community,
                    role=role,
                    status=status
                )
                created_memberships.append(membership)
        
        CommunityMembership.objects.bulk_create(created_memberships, ignore_conflicts=True)
        memberships_after = CommunityMembership.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Created {memberships_after - memberships_before} memberships.")
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        start_time = datetime.now()
        
        communities = self.__generate_communities(community_count=100)
        if communities:
            self.__generate_memberships(membership_count=500)
    
