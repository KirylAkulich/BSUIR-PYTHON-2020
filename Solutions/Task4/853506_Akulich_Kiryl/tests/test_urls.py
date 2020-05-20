from django.test import TestCase,RequestFactory
import pytest
from django.urls import reverse,resolve
from blog.models import Account
from blog.views import user_profile
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
'''
@pytest.fixture(autouse=True)
def file_urlu( view_name, mode,admin_client,client):
    url = reverse(view_name)
    if mode == 'client':
        return client.get(url)
    else:
        return admin_client.get(url)


@pytest.mark.parametrize('self.file_urlu', ['blog:post_lists', 'client'])
def test_main_url(self):
    url = self.file_urlu
    response = self.client.get(url)
    assert response.status_code == 200


class TestUrls(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestUrls,cls).setUpClass()

    @pytest.mark.django_db
    def test_main_url(self):
        path=reverse('blog:post_list')
        assert resolve(path).view_name == 'blog:post_list'

    @pytest.mark.django_db
    def test_user(self):
        user=Account.objects.create_user(email='oopflasklab@gmail.com',username='test',
                                         password='password')
        assert user.email=='oopflasklab@gmail.com'

    def test_user_auth(self):
        path=reverse('blog:profile')
        request=RequestFactory().get(path)
        request.user=Account.objects.create_user(email='oopflasklab@gmail.com',username='test',
                                         password='password')
        response=user_profile(request)
        assert response.status_code==200
        request.user=AnonymousUser()
        response = user_profile(request)
        assert response.status_code !=200

    @pytest.fixture(autouse=True)
    def file_ulru(self, view_name, mode):
        url = reverse(view_name)
        if mode == 'client':
            return self.client.get(url)
        else:
            return self.admin_client.get(url)

    @pytest.mark.parametrize('self.file_ulru', ['blog:post_lists', 'client'])
    def test_main_url(self):
        url = self.file_ulru
        response = self.client.get(url)
        assert response.status_code == 200
'''
@pytest.mark.django_db
class TestModels:

  def test_user(self):
    acc=mixer.blend('blog.Account',quantity=1)
    assert 1==1




