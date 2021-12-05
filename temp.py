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
for i in tqdm(range(len(vr))):
    frame = vr[i]
    # Gray = R*0.299 + G*0.587 + B*0.114 
    print('ok')
    # print(frame.shape)


# # To get multiple frames at once, use get_batch
# # this is the efficient way to obtain a long list of frames
# frames = vr.get_batch([1, 3, 5, 7, 9])
# print(frames.shape)
# # (5, 240, 320, 3)
# # duplicate frame indices will be accepted and handled internally to avoid duplicate decoding
# frames2 = vr.get_batch([1, 2, 3, 2, 3, 4, 3, 4, 5]).asnumpy()
# print(frames2.shape)
# # (9, 240, 320, 3)

# # 2. you can do cv2 style reading as well
# # skip 100 frames
# vr.skip_frames(100)
# # seek to start
# vr.seek(0)
# batch = vr.next()
# print('frame shape:', batch.shape)
# print('numpy frames:', batch.asnumpy())
