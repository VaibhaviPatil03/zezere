from . import TestCase

from django.core.exceptions import ValidationError

from zezere.models import RunRequest


class ModelsRunReqTest(TestCase):
    fixtures = [
        'fedora_installed.json',
        'fedora_iot_runreqs.json',
    ]

    def test_validation_auto(self):
        with self.assertRaises(ValidationError) as ex:
            RunRequest.objects.get(
                auto_generated_id=self.RUNREQ_INSTALLED
            ).full_clean()
        self.assertEqual(len(ex.exception.messages), 1)

    def test_validation_nonauto_require_owner(self):
        with self.assertRaises(ValidationError) as ex:
            RunRequest(
                auto_generated_id=None,
                owner=None,
                type=RunRequest.TYPE_EFI,
                efi_application='/somewhere.efi',
            ).full_clean()
        self.assertEqual(len(ex.exception.messages), 1)

    def test_validation_nonauto_ok_require_kernel_url(self):
        with self.assertRaises(ValidationError) as ex:
            RunRequest(
                auto_generated_id=None,
                owner=self.get_user(self.USER_1),
                type=RunRequest.TYPE_ONLINE_KERNEL,
                kernel_url=None,
                initrd_url='http://nowhere.world/',
            ).full_clean()
        self.assertEqual(len(ex.exception.messages), 1)

    def test_validation_nonauto_ok_require_initrd_url(self):
        with self.assertRaises(ValidationError) as ex:
            RunRequest(
                auto_generated_id=None,
                owner=self.get_user(self.USER_1),
                type=RunRequest.TYPE_ONLINE_KERNEL,
                kernel_url='http://nowhere.world/',
                initrd_url=None,
            ).full_clean()
        self.assertEqual(len(ex.exception.messages), 1)

    def test_validation_nonauto_ok(self):
        RunRequest(
            auto_generated_id=None,
            owner=self.get_user(self.USER_1),
            type=RunRequest.TYPE_ONLINE_KERNEL,
            kernel_url='http://nowhere.world/',
            initrd_url='http://nowhere.world/',
        ).full_clean()

    def test_validation_nonauto_ef_require_app(self):
        with self.assertRaises(ValidationError) as ex:
            RunRequest(
                auto_generated_id=None,
                owner=self.get_user(self.USER_1),
                type=RunRequest.TYPE_EFI,
                efi_application=None,
            ).full_clean()
        self.assertEqual(len(ex.exception.messages), 1)

    def test_validation_nonauto_ef(self):
        RunRequest(
            auto_generated_id=None,
            owner=self.get_user(self.USER_1),
            type=RunRequest.TYPE_EFI,
            efi_application='/somewhere.efi',
        ).full_clean()
