
import multiprocessing
from  multiprocessing import Event,Queue
from django.core.mail import send_mail
from django.template.loader import render_to_string
import threading
class ActorExit(Exception):
    pass

class Actor:
    def __init__(self):
        self._mailbox=Queue()

    def send(self,msg):
        self._mailbox.put(msg)
        print('put :{}'.format(msg))
        print(self._mailbox.empty())

    def recv(self):
        print('I am in recieved')
        msg=self._mailbox.get()
        print('recieved: {}'.format(msg))
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        self.send(ActorExit)

    def __call__(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._teminated.set()


    def start(self):
        self._teminated=threading.Event()
        p=multiprocessing.Process(target=self)
        p.daemon=True
        p.start()


    def join(self):
        self._teminated.wait()

    def run(self):

        while True:
            msg=self.recv()

class MailActor(Actor):
    def run(self):
        print('-----mailer is ready----')
        while True:
            print("=========In while------")
            msg=self.recv()
            send_mail("Django mail", ' ', 'ooplabflask@gmail.com', [msg.email],
                      html_message=render_to_string('emailbody.html', {'user': msg}),
                      fail_silently=False)
            print(render_to_string('emailbody.html', {'user': msg}))

django_mailer=MailActor()
django_mailer.start()