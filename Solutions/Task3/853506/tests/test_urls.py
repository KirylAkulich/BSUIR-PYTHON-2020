from django.test import TestCase,RequestFactory
import pytest
from django.urls import reverse,resolve
from blog.models import Account
from blog.views import user_profile
from django.contrib.auth.models import AnonymousUser

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
