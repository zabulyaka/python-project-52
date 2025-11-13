from task_manager.users.models import User
from task_manager.statuses.models import Status
from django.test import TestCase
from django.urls import reverse_lazy

class StatusTestCase(TestCase):
    fixtures = ['statuses.json']
    
    def setUp(self):
        self.test_data = {
            'name': 'status3'
        }

    def get_test_user(self, name='name3'):
        user = User.objects.get(first_name=name)
        return user

    def get_test_status(self, name='status2'):
        status = Status.objects.get(name=name)
        return status

    def test_status_create_wo_auth(self):
        new_data = self.test_data

        url = reverse_lazy('status_create')
        response = self.client.post(url, new_data)
        
        redirect_url = reverse_lazy('user_login')
        self.assertRedirects(response, redirect_url)

        self.client.login(username='nickname3', password='djangohexlet3')

        url = reverse_lazy('statuses_show')
        response = self.client.get(url)

        self.assertNotContains(response, new_data['name'])

        self.client.logout()        

    def test_status_create_with_auth(self):
        new_data = self.test_data

        self.client.login(username='nickname3', password='djangohexlet3')

        url = reverse_lazy('status_create')
        response = self.client.post(url, new_data)

        self.assertEqual(response.status_code, 302)
        created_status = self.get_test_status(name=new_data['name'])
        self.assertEqual(created_status.name, new_data['name'])

        self.client.logout()        
    
    def test_status_update_wo_auth(self):
        new_data = self.test_data
        status = self.get_test_status()

        url = reverse_lazy('status_update', kwargs={'pk': status.pk})
        response = self.client.post(url, new_data)
        status.refresh_from_db()

        redirect_url = reverse_lazy('user_login')
        self.assertRedirects(response, redirect_url)
        self.assertNotEqual(status.name, new_data['name'])

    def test_status_update_with_auth(self):
        new_data = self.test_data
        user = self.get_test_user()
        status = self.get_test_status()

        self.client.login(username='nickname3', password='djangohexlet3')

        url = reverse_lazy('status_update', kwargs={'pk': status.pk})
        response = self.client.post(url, new_data)
        status.refresh_from_db()

        redirect_url = reverse_lazy('statuses_show')
        self.assertRedirects(response, redirect_url)
        self.assertEqual(status.name, new_data['name'])

        self.client.logout()

    def test_status_delete_wo_auth(self):
        status = self.get_test_status()

        url = reverse_lazy('status_delete', kwargs={'pk': status.pk})
        response = self.client.post(url)

        redirect_url = reverse_lazy('user_login')
        self.assertRedirects(response, redirect_url)
        
        self.client.login(username='nickname3', password='djangohexlet3')

        url = reverse_lazy('statuses_show')
        response = self.client.get(url)

        self.assertContains(response, status.name)

        self.client.logout()        
        
    def test_status_delete_with_auth(self):
        user = self.get_test_user()
        status = self.get_test_status()

        self.client.login(username='nickname3', password='djangohexlet3')

        url = reverse_lazy('status_delete', kwargs={'pk': status.pk})
        response = self.client.post(url)
        
        redirect_url = reverse_lazy('statuses_show')
        self.assertRedirects(response, redirect_url)
       
        url = reverse_lazy('statuses_show')
        response = self.client.get(url)

        self.assertNotContains(response, status.name)

        self.client.logout()        
