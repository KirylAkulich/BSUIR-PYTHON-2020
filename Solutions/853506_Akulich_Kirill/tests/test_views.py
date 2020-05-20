from django.test import TestCase,RequestFactory,Client
import pytest
from django.urls import reverse,resolve
from mixer.backend.django import mixer
from blog.views import post_list,post_detail,temp_confirm,edit,verified
from blog.models import Post
import blog.Q


@pytest.fixture
def temp(request,db):
    mixer.blend('blog.Post', title='TESTING')
    view=request.param['view']
    view_name=request.param['view_name']
    mode=request.param['mode']
    path = reverse(view_name,args=request.param['args'])
    req = RequestFactory().get(path)
    if mode=='client':
        req.user=mixer.blend('blog.Account')
    return  view(req,*request.param['args'])


@pytest.mark.parametrize('temp', [{'view':post_list,'view_name':'blog:post_list' ,'mode':'client','args':[]}],indirect=True)
def test_main_url(temp):
    response = temp
    assert response.status_code == 200

@pytest.mark.parametrize('temp', [{'view':post_detail,'view_name':'blog:detail' ,'mode':'client','args':['TESTING']}],indirect=True)
def test_detiail(temp,db):
    req=temp
    assert req.status_code==200

@pytest.fixture
def user_relation(request,db):
    #mixer.blend('blog.Account',{'password': '123','username': 'TESTING', 'email': 'testing@gmail.com'})
    path = reverse(request.param['name'])
    c = Client({'password': '123','username': 'TESTING', 'email': 'oopflasklab@gmail.com'})
    r=c.post(request.param['name'], {'password1': '123', 'password2': '123',
                         'username': 'TESTING', 'email': 'oopflasklab@gmail.com'})
    print(r)
    return r

#@pytest.mark.parametrize('user_relation',[{'name':'blog:register'}])
def test_register(db):
    c = Client()
    path=reverse('blog:register')
    r = c.post(path, {'password1': '123', 'password2': '123',
                                       'username': 'TESTING', 'email': 'oopflasklab@gmail.com'})
    assert r.status_code==302


def test_login(db):
    model=mixer.blend('blog.Account')
    model.password='123'
    model.username="TESTING"
    model.email='oopflasklab@gmail.com'
    model.save()
    c = Client()
    path = reverse('blog:login')
    r = c.post(path, {'password1': '123', 'password2': '123',
                      'username': 'TESTING', 'email': 'oopflasklab@gmail.com'})
    assert r.status_code==302


def test_auth(db):
    model = mixer.blend('blog.Account')
    model.password = '123'
    model.username = "TESTING"
    model.email = 'oopflasklab@gmail.com'
    model.save()
    path = reverse('blog:temp_confirm',args=[model.id,])
    req=RequestFactory().get(path)
    req.user=model
    resp=temp_confirm(req,u_id=model.id)
    assert resp.status_code==302

def test_composer_creation(db):
    comp=mixer.blend('blog.Composer')
    comp.filepath='weights1.hdf5'
    post=mixer.blend('blog.Post')
    post.title='TEST'
    post.save()
    comp.post=post
    comp.save()
    path=reverse('blog:detail',args=[post.title,])
    req=RequestFactory().get(path)
    req.user=mixer.blend('blog.Account')
    req.GET=['submit_network']
    resp=post_detail(req,title=post.title)
    assert resp.status_code==200


def test_comment_edit(db):
    commnet=mixer.blend('blog.Comment')
    post = mixer.blend('blog.Post')
    post.title = 'TEST'
    post.save()
    commnet.post=post
    path = reverse('blog:edit', args=[commnet.id,post.title, ])
    req = RequestFactory().get(path)
    req.GET={'commentbody':"Test"}
    res=edit(req,c_id=commnet.id,title=post.title)
    assert res.status_code==302



def test_veryfied(db):
    model = mixer.blend('blog.Account')
    model.password = '123'
    model.username = "TESTING"
    model.email = 'oopflasklab@gmail.com'
    model.save()
    #from blog.Q import django_mailer
    #django_mailer.run()
    path = reverse('blog:veryfied',args=[model.id,])
    req=RequestFactory().get(path)
    req.user=model
    resp=verified(req,u_id=model.id)
    assert resp.status_code==200

