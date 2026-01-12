from django.test import TestCase
from django.urls import reverse
from .models import Task, Tag


class TodoTests(TestCase):
    def setUp(self):
        # Створюємо початкові дані для тестів
        self.tag = Tag.objects.create(name="Work")
        self.task = Task.objects.create(
            content="Test task content",
            is_done=False
        )
        self.task.tags.add(self.tag)

    # 1. Тестування моделей
    def test_tag_str(self):
        self.assertEqual(str(self.tag), "Work")

    def test_task_str(self):
        self.assertEqual(str(self.task), "Test task content")

    def test_task_ordering(self):
        # Перевірка сортування: спочатку не зроблені (is_done=False)
        Task.objects.create(content="Done task", is_done=True)
        tasks = Task.objects.all()
        self.assertEqual(tasks[0].content, "Test task content")
        self.assertFalse(tasks[0].is_done)

    # 2. Тестування доступності сторінок (Views)
    def test_index_page_status_code(self):
        response = self.client.get(reverse("todo:index"))
        self.assertEqual(response.status_code, 200)

    def test_tag_list_page_status_code(self):
        response = self.client.get(reverse("todo:tag-list"))
        self.assertEqual(response.status_code, 200)

    # 3. Тестування логіки перемикання статусу (Toggle Status)
    def test_toggle_task_status(self):
        # Викликаємо URL для зміни статусу
        toggle_url = reverse("todo:toggle-status", kwargs={"pk": self.task.id})

        # Використовуємо POST, оскільки ми переписали це на Class-based View з методом post
        response = self.client.post(toggle_url)

        # Оновлюємо дані з бази
        self.task.refresh_from_db()

        # Перевіряємо, що статус змінився на True
        self.assertTrue(self.task.is_done)
        # Перевіряємо редирект на головну сторінку
        self.assertRedirects(response, reverse("todo:index"))

    # 4. Тестування створення через форму (базово)
    def test_create_tag(self):
        tags_count = Tag.objects.count()
        response = self.client.post(reverse("todo:tag-create"), {"name": "New Tag"})
        self.assertEqual(response.status_code, 302)  # Редирект після успіху
        self.assertEqual(Tag.objects.count(), tags_count + 1)