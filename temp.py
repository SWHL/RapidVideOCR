# -*- encoding=utf-8 -*-
import cv2


def compute_similar(img_a, img_b, size=(256, 40)):
    if img_a.ndim == 3:
        img_a = cv2.cvtColor(img_a, cv2.COLOR_RGB2GRAY)
        img_a = cv2.resize(img_a, size)

    if img_b.ndim == 3:
        img_b = cv2.cvtColor(img_b, cv2.COLOR_RGB2GRAY)
        img_b = cv2.resize(img_b, size)

    hist_a = cv2.calcHist(images=[img_a],
                          channels=[0], mask=None,
                          histSize=[img_a.shape[0]],
                          ranges=[0.0, 256.0])

    hist_b = cv2.calcHist(images=[img_b],
                          channels=[0], mask=None,
                          histSize=[img_b.shape[0]],
                          ranges=[0.0, 256.0])

    return 1 - cv2.compareHist(hist_a, hist_b, 1)


if __name__ == '__main__':
    img1_path = r'a.jpg'
    img2_path = r'b.jpg'
    # similary = calc_similar_by_path(img1_path, img2_path)
    # print("两张图片相似度为:%s" % similary)

    img_a = cv2.imread(img1_path)
    img_b = cv2.imread(img2_path)
    res = compute_similar(img_a, img_b)
    print(res)

    # grey_img_a = cv2.cvtColor(img_a, cv2.COLOR_RGB2GRAY)
    # grey_img_b = cv2.cvtColor(img_b, cv2.COLOR_RGB2GRAY)

    # hist_a = cv2.calcHist(images=[grey_img_a],
    #                       channels=[0], mask=None,
    #                       histSize=[grey_img_a.shape[0]],
    #                       range=[0.0, 256.0])

    # hist_b = cv2.calcHist(images=[grey_img_b],
    #                       channels=[0], mask=None,
    #                       histSize=[grey_img_b.shape[0]],
    #                       range=[0.0, 256.0])

    # res = 1 - cv2.compareHist(hist_a, hist_b, 1)
    # print(res)
