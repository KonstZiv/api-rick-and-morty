from django.db import models


class Character(models.Model):
    class StatusChoices(models.TextChoices):
        ALIVE = "Alive"
        DEAD = "Dead"
        UNKNOWN = "unknown"

    class GenderChoices(models.TextChoices):
        FEMALE = "Female"
        MALE = "Male"
        GENDERLESS = "Genderless"
        UNKNOWN = "unknown"

    api_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=16, choices=StatusChoices.choices)
    species = models.CharField(max_length=255)
    gender = models.CharField(max_length=16, choices=GenderChoices.choices)
    image = models.URLField(unique=True, max_length=255)

    def __str__(self) -> str:
        return self.name

    def _key(self):
        return (
            self.api_id,
            self.name,
            self.status,
            self.species,
            self.gender,
            self.image,
        )

    def __eq__(self, other):
        if not isinstance(other, Character):
            raise NotImplemented
        return self._key() == other._key()

    def __hash__(self):
        return hash(self._key())
