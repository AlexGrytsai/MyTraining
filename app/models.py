import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    pass


class BodyPart(models.TextChoices):
    UPPER_BODY = "Upper Body", "Upper Body"
    LOWER_BODY = "Lower Body", "Lower Body"
    FULL_BODY = "Full Body", "Full Body"


def create_custom_path_for_image(
    instance: ["Exercise", "Muscles"],
    filename: str
) -> str:
    _, extension = os.path.splitext(filename)
    if isinstance(instance, Exercise):
        return os.path.join(
            f"uploads-images/exercises/"
            f"{slugify(instance.body_part)}/{slugify(instance.name)}/",
            f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
        )
    elif isinstance(instance, Muscles):
        return os.path.join(
            f"uploads-images/muscles/",
            f"{slugify(instance.body_part)}/{slugify(instance.name)}/",
            f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
        )


class Muscles(models.Model):
    name = models.CharField(max_length=100, unique=True)
    body_part = models.CharField(max_length=100, choices=BodyPart.choices)
    description = models.TextField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to=create_custom_path_for_image, blank=True, null=True
    )


class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    body_part = models.CharField(max_length=100, choices=BodyPart.choices)
    core_muscles = models.ForeignKey(
        Muscles, on_delete=models.CASCADE, related_name="core_muscles"
    )
    additional_muscles = models.ManyToManyField(
        Muscles, blank=True, related_name="additional_muscles"
    )
    description = models.TextField(max_length=100, blank=True, null=True)
    execution_description = models.TextField(
        max_length=100, blank=True, null=True
    )
    use_of_add_weight = models.BooleanField(default=False)
    double_weight = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to=create_custom_path_for_image, blank=True, null=True
    )

    def clean(self):
        if self.image:
            max_image_size = 2097152
            if self.image.size > max_image_size:
                raise ValidationError(
                    f"Photo size is too large "
                    f"(max. {max_image_size / 1024 / 1024}MB)"
                )

    def __str__(self):
        return f"{self.name} ({self.body_part}-{self.core_muscles})"
