import os
from threading import Thread
import ffmpeg
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Video
from .serializers import VideoSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES['file']
        video = Video.objects.create(file=file, filename=file.name)
        return Response({'id': video.id}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def change_resolution(self, request, pk=None):
        video = self.get_object()
        width = request.data.get('width')
        height = request.data.get('height')

        if width % 2 != 0 or height % 2 != 0 or width <= 20 or height <= 20:
            return Response({'error': 'Width and height must be even numbers greater than 20'},
                            status=status.HTTP_400_BAD_REQUEST)

        video.processing = True
        video.save()

        Thread(target=process_video, args=(video, width, height)).start()

        return Response({'success': video.processing}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        video = self.get_object()
        serializer = self.get_serializer(video)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        video = self.get_object()
        file_path = video.file.path
        video.delete()
        if os.path.exists(file_path):
            os.remove(file_path)  # Удаление файла с диска

        return Response({'success': True}, status=status.HTTP_200_OK)


def process_video(video, width, height):
    input_file = video.file.path
    output_file = os.path.splitext(input_file)[0] + f'_{width}x{height}.mp4'
    output_filename = os.path.basename(output_file)

    if not os.path.exists(input_file):
        return Response({'error': 'Requested file does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, vf=f'scale={width}:{height}')
            .run()
        )
        video.processing_success = True
        os.remove(input_file)  # Удаление оригинального файла после успешной конвертации
        video.file.name = f'videos/{output_filename}'  # Обновление имени файла в базе данных
        video.filename = output_filename

    except Exception as e:
        video.processing_success = False
        video.processing = False
        video.save()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        video.processing = False
        video.save()
