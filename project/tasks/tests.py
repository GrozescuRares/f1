from parameterized import parameterized
from rest_framework.test import APITestCase
from rest_framework import status
from tasks.models import Task


class TaskViewSetTestCase(APITestCase):
    def test_create_task_happy(self) -> None:
        response = self.client.post(
            "/tasks/",
            {
                "operation": "1+1",
                "priority": 5,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Task.objects.count(), 1)

        task = Task.objects.first()
        self.assertEqual(task.operation, "1+1")
        self.assertEqual(task.priority, 5)

    def test_create_task_without_priority(self) -> None:
        response = self.client.post(
            "/tasks/",
            {
                "operation": "1+1",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Task.objects.count(), 1)

        task = Task.objects.first()
        self.assertEqual(task.operation, "1+1")
        self.assertTrue(0 <= task.priority <= 9)

    @parameterized.expand(
        [
            ({"operation": 1}, status.HTTP_400_BAD_REQUEST),
            ({"operation": "1+1", "priority": "high"}, status.HTTP_400_BAD_REQUEST),
        ]
    )
    def test_create_task_with_invalid_data(
        self, payload: dict, expected_status: int
    ) -> None:
        response = self.client.post("/tasks/", payload)
        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(Task.objects.count(), 0)
