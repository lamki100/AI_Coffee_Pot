import cv2
from picamera import PiCamera
import time
from twilio.rest import TwilioRestClient
import numpy as np
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import smtplib
import RPi.GPIO as GPIO

print("Image Processing")

camera = PiCamera()

camera.start_preview()
camera.capture('currentState.jpg')
time.sleep(4)
camera.stop_preview()

camera.close()

sender = 'madtok2@gmail.com'
receivers = ['madtok2@gmail.com']

message = """Fill up the damn coffee pot
all the things.
"""

template = cv2.imread("empty_pot.jpg")
image2 = cv2.imread("currentState.jpg")

template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

w, h = template.shape[::-1]

res = cv2.matchTemplate(image2, template, cv2.TM_CCOEFF_NORMED)
threshhold = 0.3
loc = np.where(res >= threshhold)

found = False
for pt in zip(*loc[::-1]):
	found = True
	print "similar!!"


try:
	if found:
        	smtpObj = smtplib.SMTP('smtp.gmail.com:587')
        	smtpObj.ehlo()
        	smtpObj.starttls()
        	smtpObj.ehlo()
        	smtpObj.login(sender, 'scstmadtok2')
        	smtpObj.sendmail(sender, receivers, message)
        	print "Successfully sent email"
        	smtpObj.quit()
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(17, GPIO.OUT)
		GPIO.output(17,True)
		GPIO.output(17,False)
	else:
		print "Not similar"
except smtplib.SMTPException as E:
        print "Error: unable to send email"
        print E


