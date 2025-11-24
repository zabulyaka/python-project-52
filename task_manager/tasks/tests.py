from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.test import TestCase
from django.urls import reverse_lazy

class TaskTestCase(TestCase):
    fixtures = ['tasks.json']
    
    def setUp(self):
        self.test_data = {
            'name': 'task3',
            'description': 'description3',
            'executor': User.objects.get(first_name='name2').id,
            'status': Status.objects.get(name='status2').id
        }

    def get_test_user(self, name='name1'):
        user = User.objects.get(first_name=name)
        return user

    def get_test_task(self, name='task2'):
        task = Task.objects.get(name=name)
        return task

    def test_task_create_wo_auth(self):
        new_data = self.test_data

        url = reverse_lazy('task_create')
        response = self.client.post(url, new_data)
        
        redirect_url = reverse_lazy('user_login')
        self.assertRedirects(response, redirect_url)

        self.client.login(username='nickname1', password='djangohexlet1')

        url = reverse_lazy('tasks_show')
        response = self.client.get(url)

        self.assertNotContains(response, new_data['name'])

        self.client.logout()        

    def test_task_create_with_auth(self):
        new_data = self.test_data

        self.client.login(username='nickname1', password='djangohexlet1')

        url = reverse_lazy('task_create')
        response = self.client.post(url, new_data)

        self.assertEqual(response.status_code, 302)
        created_task = self.get_test_task(name=new_data['name'])
        self.assertEqual(created_task.name, new_data['name'])

        self.client.logout()        
    
    def test_task_update_wo_auth(self):
        new_data = self.test_data
        task = self.get_test_task()

        url = reverse_lazy('task_update', kwargs={'pk': task.pk})
        response = self.client.post(url, new_data)
        task.refresh_from_db()

        redirect_url = reverse_lazy('user_login')
        self.assertRedirects(response, redirect_url)
        self.assertNotEqual(task.name, new_data['name'])

    def test_task_update_with_auth(self):
        new_data = self.test_data
        user = self.get_test_user()
        task = self.get_test_task()

        self.client.login(username='nickname1', password='djangohexlet1')

        url = reverse_lazy('task_update', kwargs={'pk': task.pk})
        response = self.client.post(url, new_data)
        task.refresh_from_db()

        redirect_url = reverse_lazy('tasks_show')
        self.assertRedirects(response, redirect_url)
        self.assertEqual(task.name, new_data['name'])

        self.client.logout()

    def test_task_delete_wo_auth(self):
        task = self.get_test_task()

        url = reverse_lazy('task_delete', kwargs={'pk': task.pk})
        response = self.client.post(url)

        redirect_url = reverse_lazy('user_login')
        self.assertRedirects(response, redirect_url)
        
        self.client.login(username='nickname3', password='djangohexlet3')

        url = reverse_lazy('tasks_show')
        response = self.client.get(url)

        self.assertContains(response, task.name)

        self.client.logout()        
        
    def test_task_delete_with_auth(self):
        user = self.get_test_user()
        task = self.get_test_task()

        self.client.login(username='nickname1', password='djangohexlet1')

        url = reverse_lazy('task_delete', kwargs={'pk': task.pk})
        response = self.client.post(url)
        
        redirect_url = reverse_lazy('tasks_show')
        self.assertRedirects(response, redirect_url)
       
        url = reverse_lazy('tasks_show')
        response = self.client.get(url)

        self.assertNotContains(response, task.name)

        self.client.logout()        
