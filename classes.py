#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2 as cv
import cvzone
from source import putTextRect
import random


class Question:
    img_pos =[[730, 50], [1005, 50], [730, 325], [1005, 325]]
    random.shuffle(img_pos)
    print(img_pos)

    def __init__(self, text, wrong_imgs_path, correct_imgs_path):
        self.text = text
        self.wrong_imgs = [DragObject(path, pos=pos, res_size=[275, 275], is_correct=False) for path, pos in
                           zip(wrong_imgs_path, self.img_pos[:-1])]
        self.correct_imgs = [DragObject(path, pos=self.img_pos[3], res_size=[275, 275]) for path in correct_imgs_path]

    def overlay_all(self, frame):
        img = frame
        DrObj = self.correct_imgs[0]
        if DrObj.type == "png":
            try:
                # img = cvzone.overlayPNG(frame, DrObj.img, DrObj.pos)
                img = DrObj.overlay(frame)
            except Exception as exc:
                # if exc == cv.error:
                print(exc)
                DrObj.make_jpg()
        elif DrObj.type == "jpg":
            img = DrObj.overlay(img)
        else:
            return TypeError("Wrong format")

        for photo in self.wrong_imgs:
            if photo.type == "png":
                try:
                    img = photo.overlay(img) #, photo.img, photo.pos
                except Exception as exc:
                    # if exc == cv.error:
                    photo.make_jpg()

            elif photo.type == "jpg":
                img = photo.overlay(img)
            else:
                TypeError("Wrong format")

        return img

    def update(self, cursor, frame):
        for dragobject in self.correct_imgs + self.wrong_imgs:
            # centerx, centery = dragobject.pos
            # if centerx - dragobject.w // 2 < cursor[0] < centerx + dragobject.w // 2 and centery - dragobject.h // 2 < cursor[
            #     1] < centery + dragobject.h // 2:
            x, y = dragobject.pos
            if x < cursor[0] < x + dragobject.w and y < cursor[1] < y + dragobject.h:
                if dragobject.is_correct:
                    putTextRect(frame, "Correct!", [500, 650], colorR=(5, 255, 5), border=25)
                    return 1, 1
                else:
                    putTextRect(frame, "Wrong!", [500, 650], colorR=(5, 5, 245), border=25, colorB=(5, 5, 245))
                    return -1, 2
        return 0, False

    def show_text(self, frame):
        putTextRect(frame, self.text, [50, 300], border=3, colorB=(10, 10 ,10))


class DragObject:
    def __init__(self, img_path, pos=[500, 500], res_size=None, is_correct=True):
        self.img = cv.imread(img_path, cv.IMREAD_UNCHANGED)
        if self.img.shape[0] > 0 or self.img.shape[1] > 300:
            if res_size:
                self.img = cv.resize(self.img, res_size, interpolation=cv.INTER_LINEAR)

            else:
                self.img = cv.resize(self.img, (self.img.shape[0] // 2, self.img.shape[1] // 2), interpolation=cv.INTER_LINEAR)

        self.pos = pos
        self.w, self.h = int(self.img.shape[0]), int(self.img.shape[1])
        self.is_correct = is_correct
        self.type = img_path[-3:]
        self.path = img_path

    def overlay(self, frame):
        if self.type == "png":
            return cvzone.overlayPNG(frame, self.img, [self.pos[0], self.pos[1]])
        elif self.type == "jpg":
            x, y = self.pos
            frame[y:(y+self.h), x:(x+self.w)] = self.img
            return frame
        else:
            return ValueError("error")

    def update(self, cursor):
        centerx, centery = self.pos
        if centerx - self.w // 2 < cursor[0] < centerx + self.w // 2 and centery - self.h // 2 < cursor[
            1] < centery + self.h // 2:
            self.pos = cursor[0], cursor[1]

    def is_clicked(self, cursor):
        centerx, centery = self.pos
        if centerx - self.w // 2 < cursor[0] < centerx + self.w // 2 and centery - self.h // 2 < cursor[
            1] < centery + self.h // 2:
            return True

    def make_jpg(self):
        path = f'{self.path[:-3]}jpg'
        cv.imwrite(f'{path}', self.img)
        self.type = 'jpg'
        self.img = cv.imread(path)
        print("I'm Here")