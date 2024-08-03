from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from videoapi.models import Video
from django.conf import settings
import os
import shutil


class VideoAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.video_file_path = 'C:/Users/danil/OneDrive/Изображения/Пленка/WIN_20240729_16_49_16_Pro.mp4'
        self.saved_video_path = 'D:/new PycharmProjects/djangoProjecthttpapi/videos/WIN_20240729_16_49_16_Pro.mp4'
        self.processed_video_path = 'D:/new PycharmProjects/djangoProjecthttpapi/videos/WIN_20240729_16_49_16_Pro_640x480.mp4'
        self.video = Video.objects.create(file=self.saved_video_path, filename='WIN_20240729_16_49_16_Pro.mp4')

        # Ensure the media directory exists
        if not os.path.exists(os.path.dirname(self.saved_video_path)):
            os.makedirs(os.path.dirname(self.saved_video_path))

        # Copy the test video to the media directory
        shutil.copy(self.video_file_path, self.saved_video_path)

    def tearDown(self):
        # Clean up any created files
        self.video.delete()
        if os.path.exists(self.saved_video_path):
            os.remove(self.saved_video_path)
        if os.path.exists(self.processed_video_path):
            os.remove(self.processed_video_path)

    def test_create_video(self):
        with open(self.video_file_path, 'rb') as video_file:
            response = self.client.post(reverse('video-list'), {'file': video_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        video = Video.objects.get(id=response.data['id'])
        self.assertTrue(os.path.exists(video.file.path))

    def test_change_resolution(self):
        video_id = self.video.id
        response = self.client.patch(
            reverse('video-change-resolution', args=[video_id]),
            {'width': 640, 'height': 480},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.video.refresh_from_db()
        output_file = os.path.splitext(self.video.file.path)[0] + f'_640x480.mp4'
        self.assertTrue(os.path.exists(self.video.file.path))

    def test_retrieve_video(self):
        video_id = self.video.id
        response = self.client.get(reverse('video-detail', args=[video_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(video_id))

    def test_delete_video(self):
        video_id = self.video.id
        response = self.client.delete(reverse('video-detail', args=[video_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertFalse(Video.objects.filter(id=video_id).exists())
        self.assertFalse(os.path.exists(self.saved_video_path))
        self.assertFalse(os.path.exists(self.processed_video_path))
