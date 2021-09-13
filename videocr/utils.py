from urllib.request import urlopen
import shutil
import datetime

from . import constants


# download language data files to ~/tessdata if necessary
def download_lang_data(lang: str):
    constants.TESSDATA_DIR.mkdir(parents=True, exist_ok=True)

    for lang_name in lang.split('+'):
        filepath = constants.TESSDATA_DIR / '{}.traineddata'.format(lang_name)
        if not filepath.is_file():
            # download needed file
            if lang_name[0].isupper():
                url = constants.TESSDATA_SCRIPT_URL.format(lang_name)
            else:
                url = constants.TESSDATA_URL.format(lang_name)

            with urlopen(url) as res, open(filepath, 'w+b') as f:
                shutil.copyfileobj(res, f)


# convert time string to frame index
def get_frame_index(time_str: str, fps: float):
    t = time_str.split(':')
    t = list(map(float, t))
    if len(t) == 3:
        td = datetime.timedelta(hours=t[0], minutes=t[1], seconds=t[2])
    elif len(t) == 2:
        td = datetime.timedelta(minutes=t[0], seconds=t[1])
    else:
        raise ValueError(
            'Time data "{}" does not match format "%H:%M:%S"'.format(time_str))
    index = int(td.total_seconds() * fps)
    return index


# convert frame index into SRT timestamp
def get_srt_timestamp(frame_index: int, fps: float):
    td = datetime.timedelta(seconds=frame_index / fps)
    ms = td.microseconds // 1000
    m, s = divmod(td.seconds, 60)
    h, m = divmod(m, 60)
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(h, m, s, ms)
