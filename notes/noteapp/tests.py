from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Note

class NoteAPITestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.note = Note.objects.create(
            title='Test Note',
            content='Test Content',
            user=self.user
        )

        self.client = Client()

    def test_create_note(self):
        url = reverse('create-note')
        data = {'title': 'New Note', 'content': 'New Content'}

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Note.objects.count(), 2) 

    def test_update_note(self):
        url = reverse('update-note', args=[self.note.id])
        data = {'title': 'Updated Note', 'content': 'Updated Content'}

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Note')
