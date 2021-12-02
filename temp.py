# -*- encoding=utf-8 -*-

from PIL import Image


def make_regalur_image(img, size=(256, 256)):
    """我们有必要把所有的图片都统一到特别的规格，在这里我选择是的256x256的分辨率。"""
    return img.resize(size).convert('RGB')


def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)


def calc_similar(li, ri):
    return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0


def calc_similar_by_path(lf, rf):
    li, ri = make_regalur_image(Image.open(
        lf)), make_regalur_image(Image.open(rf))
    return calc_similar(li, ri)


def split_image(img, part_size=(64, 64)):
    w, h = img.size
    pw, ph = part_size
    assert w % pw == h % ph == 0
    return [img.crop((i, j, i+pw, j+ph)).copy() for i in range(0, w, pw)
            for j in range(0, h, ph)]


if __name__ == '__main__':
    img1_path = r'a.jpg'
    img2_path = r'b.jpg'
    similary = calc_similar_by_path(img1_path, img2_path)
    print("两张图片相似度为:%s" % similary)
