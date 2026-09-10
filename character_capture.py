"""
这个项目是有借助AI的。主要在以下几个地方:
1.利用掩码抠图时AI帮我调了一下阈值
2.画出矩形轮廓这里，我本来想用遍历每一个轮廓，用len判断点的个数，
找出点最多的轮廓，然后再遍历其中点，找到最左上和右下的点，但写出
来后太繁琐了，AI教了我比较最大面积的函数。
3.视频是豆包生成的
"""
import cv2 as cv
import numpy as np
def chara_cap_demo():
    cap = cv.VideoCapture("E:/3.mp4")
    if not cap.isOpened():
        print("视频打开失败")
        return
    w = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv.CAP_PROP_FRAME_HEIGHT)#视频读取
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cap_copy = frame.copy()
        hsv = cv.cvtColor(cap_copy, cv.COLOR_BGR2HSV)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        lower_green = np.array([25, 15, 20])
        upper_green = np.array([88, 255, 255])
        mask_green = cv.inRange(hsv, lower_green, upper_green)
        mask = cv.bitwise_not(mask_green)
        kernel = np.ones((7, 7), np.uint8)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=2)#利用掩码抠图
        contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        max_area = 0
        max_cnt = None
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > max_area:
                max_area = area
                max_cnt = cnt#找到最大轮廓
        if max_cnt is not None:
            x, y, w_rect, h_rect = cv.boundingRect(max_cnt)
            cv.rectangle(cap_copy, (x, y), (x + w_rect, y + h_rect), (0, 0, 255), 2)#画出跟踪矩形
        cv.imshow("dst",cap_copy)
        #cv.imshow("mask",mask)
        #cv.imshow("mask_green", mask_green)
        c = cv.waitKey(10)
        if c == 27:
            break
    cap.release()
    cv.destroyAllWindows()
if __name__ == "__main__":
    chara_cap_demo()