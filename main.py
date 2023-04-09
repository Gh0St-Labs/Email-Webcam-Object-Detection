import os
import cv2
import time
from emailing import send_email
import glob
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

status_list = []
first_frame = None
count = 1

def clean_folder():
    print("clean_folder() FUNCTION STATUS: Started")
    images = glob.glob('images\\*.png')
    for image in images:
        os.remove(image)
    print("clean_folder() FUNCTION STATUS: Ended \n")

while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (25, 25), 0)
    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]
    # REMOVE NOISES
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    # THE HIGHER THE 'ITERATIONS', THE HIGHER THE PROCESSING

    # Create Contours / Outlines in the Object Detected
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 7000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)

        if rectangle.any():
            status = 1
            cv2.imwrite(f'images\\{count}.png', frame)
            count = count + 1
            cv2.imshow('Video', frame)
            all_images = glob.glob('images\\*.png')
            index = int(len(all_images) / 2)
            perfect_image = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        all_images = glob.glob('images\\*.png')
        index = int(len(all_images) / 2)
        perfect_image = all_images[index]
        email_thread = Thread(target=send_email, args=(perfect_image, ))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()

    print(status_list)




    # The .threshold() function takes in 4 values, first is the any frame value, second is the threshold
    # 'white' (color) value. If this value is 30, any white pixels in the frame with a value of over 30 will
    # be counted. THAT'S WHAT THE SECOND VALUE DOES. The Third Value is the value which is going to replace the
    # value entered in the second value. HOW IT WORKS:
    # SECOND VALUE / ARGUMENT = 30
    # THIRD VALUE / ARGUMENT = 255
    # WE ARE REPLACING ALL THE VALUES ABOVE 30 WITH THE VALUE 255.
    # FOURTH VALUE IS AN ALGORITHM >> cv2.THRESH_BINARY >> THIS CONVERTS THE PIXELS TO BINARY AND THEN SHOWN
    # THROUGH THE .imshow() FUNCTION.
    # MAKE SURE TO GET THE SECOND INDEX VALUE FROM THE THRESHOLD FUNCTION, WHICH IS [1]. (according to Binary)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
clean_thread.start()