from django.test import TestCase, Client
from django.urls import reverse
from .models import Task



class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Test Task")

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertFalse(self.task.completed)

# todo_app/tests.py

class TaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(title="Test Task")

    def test_task_list(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_add_task(self):
        response = self.client.post(reverse('add_task'), {'title': 'New Task'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_edit_task(self):
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {'title': 'Updated Task'})
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_delete_task(self):
        response = self.client.get(reverse('delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_complete_task(self):
        response = self.client.get(reverse('complete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)
