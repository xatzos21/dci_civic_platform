from users.models import CustomUser as User

import json
import os
import io

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Upload, Location, FileBookmark
from users.models import CustomUser
from geolocation.models import Location
from .serializers import UploadSerializer, FileBookmarkSerializer


def create_user():
    user = CustomUser.objects.create_user(
        email="normal@user.com", username="Testuser", password="foo"
    )

    return user


# https://testdriven.io/blog/django-custom-user-model/
class UploadApiTests(TestCase):
    def create_user(self):
        user = CustomUser.objects.create_user(
            email="normal@user.com", username="Testuser", password="foo"
        )

        return user

    def get_test_data(self, file):
        tags = ["Summer, Sun"]

        data = {
            "location": "Bonn",
            "title": "Test",
            "zip_code": 53129,
            "file": file,
            "tags": tags,
            "link": "https://www.zeit.de/index",
            "status": "published",
        }

        return data

    def test_upload_post(self):
        file = SimpleUploadedFile("test.txt", b"Hallo Test", content_type="text/plain")
        data = self.get_test_data(file)
        test_user = self.create_user()

        self.client.login(email="normal@user.com", password="foo")
        response = self.client.post(
            "/api/archive/upload/",
            data=data,
            headers={"Content-Type": "multipart/form-data"},
        )

        uploaded_file = response.data.get("file")
        file_path = os.path.dirname(os.path.realpath(uploaded_file))
        self.assertEqual(response.status_code, 201)
        self.assertTrue(os.path.isfile(uploaded_file))

        folders_list = file_path.split("/")
        category = folders_list[-1]
        media_root = folders_list[-2]
        # was file correctly categorized?
        self.assertEqual("document", category)
        self.assertEqual("media", media_root)

        upload_instance = Upload.objects.get(pk=response.data.get("id"))
        upload_instance.delete()

    def test_wrong_file_type_upload(self):
        file = SimpleUploadedFile("test.py", b"Hallo Test", content_type="text/plain")
        data = self.get_test_data(file)
        test_user = self.create_user()

        self.client.login(email="normal@user.com", password="foo")
        response = self.client.post(
            "/api/archive/upload/",
            data=data,
            headers={"Content-Type": "multipart/form-data"},
        )

        error_code = response.data.get("file").get("error")
        expected_error_code = "File type not supported."
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_error_code, error_code)

    def test_wrong_mime_type_upload(self):
        ##########################################
        # check if wrong file extension and
        # mime type are mismatching
        ##########################################
        file = SimpleUploadedFile("test.jpg", b"Hallo Test", content_type="text/plain")
        data = self.get_test_data(file)
        test_user = self.create_user()

        self.client.login(email="normal@user.com", password="foo")
        response = self.client.post(
            "/api/archive/upload/",
            data=data,
            headers={"Content-Type": "multipart/form-data"},
        )

        error_code = response.data.get("file").get("error")
        expected_error_code = "File extension mismatching mime type of file."
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_error_code, error_code)

    def test_upload_patch(self):
        file = SimpleUploadedFile("test.txt", b"Hallo Test", content_type="text/plain")
        data = self.get_test_data(file)
        test_user = self.create_user()

        self.client.login(email="normal@user.com", password="foo")
        response = self.client.post(
            "/api/archive/upload/",
            data=data,
            headers={"Content-Type": "multipart/form-data"},
        )

        patch_data = {"title": "Alternative title"}

        self.client.login(email="normal@user.com", password="foo")
        patch_response = self.client.patch(
            f"/api/archive/upload/{response.data.get('id')}",
            data=patch_data,
            content_type="application/json",
        )

        self.assertEqual("Alternative title", patch_response.data.get("title"))

        upload_instance = Upload.objects.get(pk=patch_response.data.get("id"))
        upload_instance.delete()

    def test_upload_delete(self):
        file = SimpleUploadedFile("test.txt", b"Hallo Test", content_type="text/plain")
        data = self.get_test_data(file)
        test_user = self.create_user()

        self.client.login(email="normal@user.com", password="foo")
        response = self.client.post(
            "/api/archive/upload/",
            data=data,
            headers={"Content-Type": "multipart/form-data"},
        )

        upload_id = response.data.get("id")
        upload_file = response.data.get("file")

        self.client.login(email="normal@user.com", password="foo")
        delete_response = self.client.delete(f"/api/archive/upload/{upload_id}")

        check_if_deleted = self.client.get("/api/archive/upload/{upload_id}")
        self.assertEqual(404, check_if_deleted.status_code)
        self.assertFalse(os.path.isfile(upload_file))


class AddBookmarkTest(TestCase):
    def create_user(self):
        user = CustomUser.objects.create_user(
            email="normal@user.com", username="Testuser", password="foo"
        )

        return user

    def get_test_data(self, file):
        tags = ["Summer, Sun"]

        data = {
            "location": "Bonn",
            "title": "Test",
            "zip_code": 53129,
            "file": file,
            "tags": tags,
            "link": "https://www.zeit.de/index",
            "status": "published",
        }

        return data

    def test_create_bookmark(self):
        file = SimpleUploadedFile("test.txt", b"Hallo Test", content_type="text/plain")
        data = self.get_test_data(file)
        test_user = self.create_user()

        self.client.login(email="normal@user.com", password="foo")
        response = self.client.post(
            "/api/archive/upload/",
            data=data,
            headers={"Content-Type": "multipart/form-data"},
        )

        upload_id = response.data.get("id")
        upload_file = response.data.get("file")
        bookmark_data = {
            "upload": upload_id,
            "note": "Important",
        }
        self.client.login(email="normal@user.com", password="foo")
        response_bookmark = self.client.post(
            "/api/archive/upload/bookmark/create/",
            data=bookmark_data,
        )

        self.assertEqual(response_bookmark.status_code, 201)
        self.assertEqual(response_bookmark.data.get("note"), "Important")
        self.assertEqual(response_bookmark.data.get("upload"), upload_id)
