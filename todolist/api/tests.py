from django.test import TestCase
from rest_framework.test import APIClient
from django.test import Client
from rest_framework import status
from .models import Task
from .models import Tag
import json
import base64
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory
from .serializers import InputSerializer, OutputSerializer


class PostCreateTest(APITestCase):

    def setUp(self):

        self.username = "test"
        self.password = "Test1234"
        self.email = "test@gmail.com"
        self.user = User.objects.create_superuser(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.headers = {
           'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'test:Test1234').decode("ascii")
        }
        self.task_data = {
            'title': 'Test Task',
            'status': 'OPEN',
            'description': 'This is a test task.',
            'due_date': '2023-12-28',
            'tags': ['name1', 'name2']
        }
        self.task_data2 = {
            'title': 'Test Task2',
            'status': 'OPEN',
            'description': 'This is a test task2.',
            'due_date': '2023-12-28',
            'tags': ['name1', 'name2']
        }
        self.updatetask_data = {
            'title': 'Task20',
            'status': 'DONE',
            'description': 'This is updated task.',
            'due_date': '2023-12-29'
          
        }

        
    def test_views(self):
        
        # created task1
        post_url = reverse('add new task')
        response = self.client.post(post_url, self.task_data, format='json', **self.headers)
        print("Task 1: ",response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # created task2
        response = self.client.post(post_url, self.task_data2, format='json', **self.headers)
        print("Task 2: ",response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Retrive all tasks
        get_url = reverse('get all tasks')
        response = self.client.get(get_url, **self.headers)
        print("All Tasks: ",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Retrieve single task
        get_url = reverse('get any task', kwargs={'pk': 2})
        response = self.client.get(get_url, **self.headers)
        print("Single Task: ",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 

        # Update any task
        update_url = reverse('update task', kwargs={'pk': 2})
        response = self.client.put(update_url, self.updatetask_data, format='json', **self.headers)
        print("Update any task: ",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        get_url = reverse('get any task', kwargs={'pk': 2})
        response = self.client.get(get_url, **self.headers)
        print("Updated Task: ",response.content)
        
        
        # Delete any task
        delete_url = reverse('delete task', kwargs={'pk': 2})
        response = self.client.delete(delete_url, **self.headers)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_models(self):    
        task = Task.objects.create(
            title="mytask1",
            status="OPEN",
            description="This is a test task",
            due_date="2023-12-28",
        )

        tag1 = Tag.objects.create(value="tag1")
        task.tags.set([tag1])

        assert task.title == "mytask1"      
        assert task.status == "OPEN"
        assert task.description == "This is a test task"    
        assert task.due_date == "2023-12-28"

        assert tag1 in task.tags.all()


    def test_url(self):

        path = reverse('add new task')
        print(path)     
        assert resolve(path).view_name == "add new task"
