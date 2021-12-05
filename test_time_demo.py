from decord import VideoReader
from decord import cpu, gpu
from tqdm import tqdm
from videocr.utils import Capture
import time
import cv2

video_path = 'assets/4.mp4'
start = time.time()
with open(video_path, 'rb') as f:
    vr = VideoReader(f, ctx=cpu(0))
print('video frames:', len(vr))
for i in tqdm(range(len(vr)), desc='Decord'):
    frame = vr[i]

middle_time = time.time()
decord_elapse = middle_time- start

with Capture(video_path) as v:
    num_frames = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in tqdm(range(num_frames), desc='OpenCV'):
        v.set(cv2.CAP_PROP_POS_FRAMES, i)
        frame = v.read()[1]

cv_elapse = time.time() - middle_time
print(f'Decord cost: {decord_elapse}')
print(f'OpenCV cost: {cv_elapse}')