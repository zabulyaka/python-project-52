from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.users.models import User


class LabelTestCase(TestCase):
    fixtures = ['labels.json']
    
    def setUp(self):
        self.test_data = {
            'name': 'label3'
        }

    def get_test_user(self, name='name3'):
        user = User.objects.get(first_name=name)
        return user

    def get_test_label(self, name='label2'):
        label = Label.objects.get(name=name)
        return label

    def test_label_create_wo_auth(self):
        new_data = self.test_data

        url = reverse_lazy('label_create')
        response = self.client.post(url, new_data)
        
        redirect_url = reverse_lazy('user_login')
        self.assertRedirects(response, redirect_url)

        self.client.login(username='nickname3', password='djangohexlet3')

        url = reverse_lazy('labels_show')
        response = self.client.get(url)

        self.assertNotContains(response, new_data['name'])

        self.client.logout()        

    def test_label_create_with_auth(self):
        new_data = self.test_data

        self.client.login(username='nickname3', password='djangohexlet3')

        url = reverse_lazy('label_create')
        response = self.client.post(url, new_data)

        self.assertEqual(response.status_code, 302)
        created_label = self.get_test_label(name=new_data['name'])
        self.assertEqual(created_label.name, new_data['name'])

        self.client.logout()        
    
    def test_label_update_wo_auth(self):
        new_data = self.test_data
        label = self.get_test_label()

        url = reverse_lazy('label_update', kwargs={'pk': label.pk})
        response = self.client.post(url, new_data)
        label.refresh_from_db()

        redirect_url = reverse_lazy('user_login')
        self.assertRedirects(response, redirect_url)
        self.assertNotEqual(label.name, new_data['name'])

    def test_label_update_with_auth(self):
        new_data = self.test_data
        label = self.get_test_label()

        self.client.login(username='nickname3', password='djangohexlet3')

        url = reverse_lazy('label_update', kwargs={'pk': label.pk})
        response = self.client.post(url, new_data)
        label.refresh_from_db()

        redirect_url = reverse_lazy('labels_show')
        self.assertRedirects(response, redirect_url)
        self.assertEqual(label.name, new_data['name'])

        self.client.logout()

    def test_label_delete_wo_auth(self):
        label = self.get_test_label()

        url = reverse_lazy('label_delete', kwargs={'pk': label.pk})
        response = self.client.post(url)

        redirect_url = reverse_lazy('user_login')
        self.assertRedirects(response, redirect_url)
        
        self.client.login(username='nickname3', password='djangohexlet3')

        url = reverse_lazy('labels_show')
        response = self.client.get(url)

        self.assertContains(response, label.name)

        self.client.logout()        
        
    def test_label_delete_with_auth(self):
        label = self.get_test_label()

        self.client.login(username='nickname3', password='djangohexlet3')

        url = reverse_lazy('label_delete', kwargs={'pk': label.pk})
        response = self.client.post(url)
        
        redirect_url = reverse_lazy('labels_show')
        self.assertRedirects(response, redirect_url)
       
        url = reverse_lazy('labels_show')
        response = self.client.get(url)

        self.assertNotContains(response, label.name)

        self.client.logout()        
