from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    USER_TYPES = (
        ('MENTOR', 'Mentor'),
        ('MENTEE', 'Mentee'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    user_type = models.CharField(
        max_length=6,
        choices=USER_TYPES,
        default='MENTEE'  # Set a default value
    )

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        return self.displayname if self.displayname else self.user.username

    @property
    def avatar(self):
        return self.image.url if self.image else f"{settings.STATIC_URL}images/avatar.svg"