from task_manager.users.models import User
from django.test import TestCase
from django.urls import reverse_lazy

class UserTestCase(TestCase):
    fixtures = ['users.json']
    
    def setUp(self):
        self.test_data = {
            'first_name': 'name4',
            'last_name': 'surname4',
            'username': 'nickname4',
            'password1': 'djangohexlet4',
            'password2': 'djangohexlet4'
        }

    def get_test_user(self, name='name3'):
        user = User.objects.get(first_name=name)
        return user

    def test_user_create(self):
        new_data = self.test_data

        url = reverse_lazy('user_create')
        response = self.client.post(url, new_data)

        self.assertEqual(response.status_code, 302)
        created_user = self.get_test_user(name=new_data['first_name'])
        self.assertEqual(created_user.username, new_data['username'])
    
    def test_user_update_wo_auth(self):
        new_data = self.test_data
        user = self.get_test_user()

        url = reverse_lazy('user_update', kwargs={'pk': user.pk})
        response = self.client.post(url, new_data)
        user.refresh_from_db()

        redirect_url = reverse_lazy('user_login')
        self.assertRedirects(response, redirect_url)
        self.assertNotEqual(user.username, new_data['username'])

    def test_user_update_with_auth(self):
        new_data = self.test_data
        user = self.get_test_user()
        another_user = self.get_test_user(name='name2')

        self.client.login(username='nickname3', password='djangohexlet3')

        url = reverse_lazy('user_update', kwargs={'pk': another_user.pk})
        response = self.client.post(url, new_data)
        another_user.refresh_from_db()

        redirect_url = reverse_lazy('users_show')
        self.assertRedirects(response, redirect_url)
        expected = 'nickname2'
        self.assertEqual(another_user.username, expected)
         
        url = reverse_lazy('user_update', kwargs={'pk': user.pk})
        response = self.client.post(url, new_data)
        user.refresh_from_db()
 
        redirect_url = reverse_lazy('users_show')
        self.assertRedirects(response, redirect_url)
        self.assertEqual(user.username, new_data['username'])

        self.client.logout()

    def test_user_delete_wo_auth(self):
        user = self.get_test_user()

        url = reverse_lazy('user_delete', kwargs={'pk': user.pk})
        response = self.client.post(url)

        redirect_url = reverse_lazy('user_login')
        self.assertRedirects(response, redirect_url)
        
        url = reverse_lazy('users_show')
        response = self.client.get(url)

        self.assertContains(response, user.username)
        
    def test_user_delete_with_auth(self):
        user = self.get_test_user()
        another_user = self.get_test_user(name='name2')

        self.client.login(username='nickname3', password='djangohexlet3')
        
        url = reverse_lazy('user_delete', kwargs={'pk': another_user.pk})
        response = self.client.post(url)

        redirect_url = reverse_lazy('users_show')
        self.assertRedirects(response, redirect_url)

        url = reverse_lazy('user_delete', kwargs={'pk': user.pk})
        response = self.client.post(url)

        self.assertRedirects(response, redirect_url)
        
        url = reverse_lazy('users_show')
        response = self.client.get(url)

        self.assertContains(response, another_user.username)
        self.assertNotContains(response, user.username)

        self.client.logout()        
