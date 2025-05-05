from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, FarmerProfile


@receiver(post_save, sender=CustomUser)
def create_farmer_profile(sender, instance, created, **kwargs):
    if created:
        FarmerProfile.objects.create(
            user=instance,
            farm_name=f"{instance.first_name}'s Farm",
            farm_size_acres=10.0,
            farm_location="Your Location"
        )


@receiver(post_save, sender=CustomUser)
def save_farmer_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()