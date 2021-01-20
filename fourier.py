import cv2
import numpy as np
import math as m
import copy


def line(img, pts1, pts2, color):
    cv2.line(img, (pts1[1], pts1[0]), (pts2[1], pts2[0]), color)


def circle(img, center, radius, color):
    cv2.circle(img, (center[1], center[0]), radius, color)


def text(img, pts, text, size, color):
    cv2.putText(img, text, (pts[1], pts[0]),
                cv2.FONT_HERSHEY_SIMPLEX, size, color)


def ellipse(img, center, length, slope, start_angle, finish_angle, color, a):
    cv2.ellipse(img, (center[1], center[0]), length,
                slope, start_angle, finish_angle, color, a)


def onChange(x):
    pass


img = np.full([500, 1000, 3], 0, dtype=np.uint8)

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.createTrackbar('0.00omega', 'img', 1, 100, onChange)

circle_center, circle_radius = (250, 200), 150
origin = 550

first = True
color_main = (255, 0, 255)
color_dnm = (100, 20, 100)
y_scale = 100

#항 추가
every_terms = []
every_terms.append(["sin", 4 / m.pi, 1,  (230,200,100), "4/pi"])
every_terms.append(["sin", 4 / (3 * m.pi), 3, (200, 100, 30), "4/3pi"])
every_terms.append(["cos", 3 / (2 * m.pi), 2, (130, 200, 0), "3/2pi"])

for t in range(0, 50000):
    omega = 1 / 100
    omega_div = cv2.getTrackbarPos('0.00omega', 'img')
    omega *= omega_div
    theta = t * omega
    #좌표 생성 => pos_every_terms
    pos_every_terms = []
    temp = [circle_center[0],circle_center[1]]
    for each_term in every_terms:
        if each_term[0] == "sin":
            temp[0] += round(y_scale * each_term[1] * m.sin(-each_term[2] * theta))
            temp[1] += round(y_scale * each_term[1] * m.cos(each_term[2] * theta))
        elif each_term[0] == "cos":
            temp[0] += round(y_scale * each_term[1] * m.cos(-each_term[2] * theta))
            temp[1] += round(y_scale * each_term[1] * m.sin(each_term[2] * theta))
        pos_every_terms.append(copy.deepcopy(temp))


    #오른쪽 그래프에 점 추가
    if first:
        dots = np.array([pos_every_terms[-1][0], origin])
        first = False
    dots = np.vstack([
        dots,
        np.array([pos_every_terms[-1][0], origin])
    ])

    #점들을 잇기
    for i in range(dots.shape[0] - 1):
        line(img, dots[i], dots[i + 1], color=color_dnm)
    #오른쪽 그래프의 점들을 오른쪽으로 1픽셀씩 옮겨주기
    dots = dots + np.array([0, 1])
    #그림에서 벗어나는 점 제거
    np.delete(dots, np.where(dots[:, 1] > img.shape[1]), axis=0)

    #기본 가로 세로 축
    line(img, (0, origin), (img.shape[0], origin), color=color_main)
    line(img, (0, circle_center[1]), (img.shape[0],
                                      circle_center[1]), color=color_main)
    line(img, (circle_center[0], 0), (circle_center[0],
                                      img.shape[1]), color=color_main)

    #왼쪽 원(들)과 직선
    circle(img, circle_center, round(y_scale * every_terms[0][1]), color=every_terms[0][3])
    line(img, circle_center, pos_every_terms[0], color=every_terms[0][3])
    for i in range(len(every_terms) - 1):
        circle(img, pos_every_terms[i], round(y_scale * every_terms[i + 1][1]), color=every_terms[i + 1][3])
        line(img, pos_every_terms[i], pos_every_terms[i + 1], color=every_terms[i + 1][3])

    #각종 텍스트, 선, ..
    line(img, pos_every_terms[-1],
         (pos_every_terms[-1][0], origin), color=color_dnm)
    text(img, (circle_center), str(every_terms[0][4])+ " "+str(every_terms[0][0]) +"("+str(every_terms[0][2])+"theta)", 1, color=every_terms[0][3])
    for i in range(len(every_terms) - 1):
        text(img, (pos_every_terms[i]), str(every_terms[i + 1][4])+" "+str(every_terms[i + 1][0]) +"("+str(every_terms[i + 1][2])+"theta)", 1, color=every_terms[i + 1][3])
    text(img, (circle_center[0], origin), "Fourier", 3,  color=color_main)
    text(img, (circle_center[0] + 30, origin + 200),
         "son jh", 1,  color=color_main)
    text(img, (30, circle_center[1]),
         "y / "+str(y_scale), 1,  color=color_main)
    text(img, (30, origin) , "y / "+str(y_scale), 1, color=color_main)
    text(img, (circle_center[0], origin - 30),
         "x", 1,  color=color_main)
    text(img, (circle_center[0], img.shape[1] - 30),
         "t", 1,  color=color_main)
    cv2.imshow("img", img)
    cv2.waitKey(1)


    img = np.full([500, 1000, 3], 0, dtype=np.uint8)