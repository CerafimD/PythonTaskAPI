import os

import ffmpeg

input_file = r'D:/new PycharmProjects/djangoProjecthttpapi/videos/WIN_20240729_16_49_16_Pro.mp4'

output_file = os.path.splitext(input_file)[0] + f'_120x120.mp4'
try:
    stream = ffmpeg.input(input_file)
    ffmpeg.output(stream, output_file, vf=f'scale={120}:{120}').run()
    print('Video conversion successful')
except Exception as e:
    print(f' {e}')
