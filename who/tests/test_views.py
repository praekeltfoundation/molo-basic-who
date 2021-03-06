import json
import requests
from mock import Mock, patch
from datetime import datetime

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client, override_settings

from rest_framework import status

from molo.core.models import Main, Languages, SiteLanguageRelation
from molo.core.tests.base import MoloTestCaseMixin


class ViewsTestCase(MoloTestCaseMixin, TestCase):

    def setUp(self):
        self.mk_main()
        main = Main.objects.all().first()
        self.english = SiteLanguageRelation.objects.create(
            language_setting=Languages.for_site(main.get_site()),
            locale='en',
            is_active=True)

        self.user = User.objects.create_user(
            'test', 'test@example.org', 'test')
        self.content_type = ContentType.objects.get_for_model(self.user)
        self.client = Client()


    def test_health_no_interface_set(self):
        """
        When there is no management interface configured it should not try and
        get the status of the queues
        """

        response = self.client.get(reverse('health'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(RABBITMQ_MANAGEMENT_INTERFACE='rabbitmq.com:15672')
    def test_health_good(self):
        """
        If there is a management interface configured it should check the
        queues, if there are messages and the rate is above 0 the status should
        be OK.
        """

        details = json.dumps(
            {'messages': 1243, 'messages_details': {'rate': 1.2}})

        with patch('httplib2.Http.request') as req:
            resp = requests.Response()
            resp.status = status.HTTP_200_OK
            req.return_value = resp, details.encode()
            response = self.client.get(reverse('health'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(RABBITMQ_MANAGEMENT_INTERFACE='rabbitmq.com:15672')
    def test_health_stuck(self):
        """
        If there is a management interface configured it should check the
        queues, if there are messages and the rate is 0 the status should be
        500.
        """

        details = json.dumps(
            {'messages': 2562, 'messages_details': {'rate': 0.0}})

        with patch('httplib2.Http.request') as req:
            resp = requests.Response()
            resp.status = status.HTTP_200_OK
            req.return_value = resp, details.encode()
            response = self.client.get(reverse('health'))

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)

    @override_settings(MAINTENANCE_MODE=True)
    def test_maintenance_mode(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'maintenance.html')

    @override_settings(MICROSOFT_AUTH_LOGIN_ENABLED=True)
    @patch('microsoft_auth.client.reverse')
    def test_microsoft_login(self, reverse_mock):
        # It's really hard to get Django to load a new url namespace after the
        # config has been loaded so I just patch reverse() where it is used instead
        reverse_mock.return_value="/microsoft/auth-callback/"

        templates_setting = settings.TEMPLATES
        templates_setting[0]['OPTIONS']['context_processors'].append(
            'microsoft_auth.context_processors.microsoft')
        with self.settings(TEMPLATES=templates_setting):
            response = self.client.get('/admin', follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, '</span><em>Microsoft</em></a>')
        self.assertContains(response, '<script type="text/javascript" src="/static/js/wagtail_login.js">')
