from django.test import TestCase, RequestFactory
from allauth.socialaccount.models import SocialAccount
from account_manager.models import User
from django.urls import reverse
from allauth.account.signals import user_signed_up

class TestSignalUserSignedUp(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory
    
    def test_user_signed_up_signal_with_social_account(self):
        any_user = User.objects.create_user(
            username='any user',
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )
        SocialAccount.objects.create(user=any_user, provider='google')

        self.client.login(email='anyuser@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('home'))

        user_signed_up.send(sender=any_user.__class__, request=response.wsgi_request, user=any_user)

        any_user.refresh_from_db()

        self.assertEqual(any_user.username, any_user.email)
        self.assertTrue(any_user.is_active)

    def test_user_signed_up_signal_without_social_account(self):
        any_user = User.objects.create_user(
            username='any user',
            idade=17,
            email='anyuser@gmail.com',
            password='senhaqualquer12',
        )

        self.client.login(email='anyuser@gmail.com', password='senhaqualquer12')
        response = self.client.get(reverse('home'))

        user_signed_up.send(sender=any_user.__class__, request=response.wsgi_request, user=any_user)

        any_user.refresh_from_db()

        self.assertEqual(any_user.username, 'any user')
        self.assertFalse(any_user.is_active)
