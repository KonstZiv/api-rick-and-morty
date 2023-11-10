from django.test import TestCase, Client
from django.urls import reverse

from characters.models import Character


class TestModelCharacter(TestCase):
    def test_str(self):
        character = Character.objects.create(
            api_id=1,
            name="test",
            status="unknown",
            species="test",
            gender="unknown",
            image="https://127.0.0.1:8000/api/v1/images/1/",
        )
        self.assertEquals(
            str(character),
            character.name,
            "incorrect __str__ method for Character model",
        )


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.character_1 = Character.objects.create(
            api_id=1,
            name="test_1",
            status="unknown",
            species="test",
            gender="unknown",
            image="https://127.0.0.1:8000/api/v1/images/1/",
        )
        self.character_2 = Character.objects.create(
            api_id=2,
            name="test_2",
            status="unknown",
            species="test",
            gender="unknown",
            image="https://127.0.0.1:8000/api/v1/images/2/",
        )

    def test_param(self):
        url = reverse("characters:character-list")
        param = {"inc_in_name": "_2"}
        res = self.client.get(url, param)
        self.assertContains(
            res,
            self.character_2.name,
            msg_prefix="Search by parameter in the name does not work: ",
        )
        self.assertEqual(
            1, len(res.json()["results"]), "Response include more then one result."
        )
