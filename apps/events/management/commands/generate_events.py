# Python modules
from typing import Any
from random import choice, randint
from datetime import datetime, timedelta

# Django modules
from django.core.management.base import BaseCommand
from django.utils import timezone

# Project modules
from apps.events.models import Event, EventApplication
from apps.users.models import CustomUser
from apps.communities.models import Community


class Command(BaseCommand):
    help = "Generate events and event applications for testing"

    EVENT_TITLES = [
        "Tech Meetup", "Art Exhibition", "Music Concert", "Sports Tournament",
        "Travel Workshop", "Food Festival", "Photography Contest", "Design Conference",
        "Code Hackathon", "Science Symposium", "Book Reading", "Gaming Tournament",
        "Fitness Challenge", "Business Summit", "Creative Workshop", "Startup Pitch",
        "Developer Conference", "Data Science Meetup", "AI Workshop", "Web Design Bootcamp"
    ]

    DESCRIPTIONS = [
        "Join us for an exciting event where we'll explore new ideas and connect.",
        "A great opportunity to learn, network, and have fun with like-minded people.",
        "Don't miss this amazing event featuring speakers and activities.",
        "Come together to celebrate and share our passion for this topic.",
        "An engaging event with workshops, discussions, and networking opportunities.",
    ]

    QUESTIONS = [
        ["What is your experience level?", "Why are you interested in this event?"],
        ["How did you hear about this event?", "What do you hope to gain?"],
        ["Any dietary restrictions?", "Will you need accommodation?"],
    ]

    def __generate_events(self, event_count: int = 200) -> list[Event]:
        users = list(CustomUser.objects.all())
        communities = list(Community.objects.all())
        
        if not users or not communities:
            self.stdout.write(self.style.ERROR("No users or communities found. Create them first"))
            return []
        
        events_before = Event.objects.count()
        created_events = []
        
        for i in range(event_count):
            organizer = choice(users)
            community = choice(communities)
            title = choice(self.EVENT_TITLES) + f" {i+1}"
            description = choice(self.DESCRIPTIONS)
            
            start_at = timezone.now() + timedelta(days=randint(1, 90))
            end_at = start_at + timedelta(hours=randint(2, 8))
            
            capacity = randint(10, 500) if randint(0, 100) < 80 else None
            status = choice(['draft', 'published', 'cancelled'])
            requires_approval = randint(0, 100) < 40
            questions = choice(self.QUESTIONS) if requires_approval else []
            
            event = Event.objects.create(
                title=title,
                description=description,
                start_at=start_at,
                end_at=end_at,
                capacity=capacity,
                status=status,
                organizer=organizer,
                community=community,
                requires_approval=requires_approval,
                questions=questions
            )
            created_events.append(event)
        
        events_after = Event.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Created {events_after - events_before} events.")
        )
        return created_events

    def __generate_applications(self, application_count: int = 500) -> None:
        events = list(Event.objects.filter(status='published'))
        users = list(CustomUser.objects.all())
        
        if not events or not users:
            return
        
        applications_before = EventApplication.objects.count()
        created_applications = []
        
        for i in range(application_count):
            event = choice(events)
            user = choice(users)
            
            if user == event.organizer:
                continue
            
            if not EventApplication.objects.filter(event=event, user=user).exists():
                status = choice(['applied', 'pending', 'approved', 'declined', 'cancelled'])
                answers = {}
                
                if event.questions:
                    for question in event.questions:
                        answers[question] = f"Answer to {question}"
                
                reviewed_at = None
                reviewed_by = None
                if status in ['approved', 'declined']:
                    reviewed_at = timezone.now()
                    reviewed_by = event.organizer
                
                application = EventApplication(
                    event=event,
                    user=user,
                    status=status,
                    answers=answers,
                    reviewed_at=reviewed_at,
                    reviewed_by=reviewed_by
                )
                created_applications.append(application)
        
        EventApplication.objects.bulk_create(created_applications, ignore_conflicts=True)
        applications_after = EventApplication.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Created {applications_after - applications_before} applications.")
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        start_time = datetime.now()
        
        events = self.__generate_events(event_count=200)
        if events:
            self.__generate_applications(application_count=500)
          
