import sqlite3, os, pickle
from glob import glob
import cv2

def init_create_folder_database():
	# create the folder and database if not exist
	if not os.path.exists("gestures"):
		os.mkdir("gestures")
	if not os.path.exists("gesture_db.db"):
		conn = sqlite3.connect("gesture_db.db")
		create_table_cmd = "CREATE TABLE gesture ( g_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, g_name TEXT NOT NULL )"
		conn.execute(create_table_cmd)
		conn.commit()

def create_folder(folder_name):
	if not os.path.exists(folder_name):
		os.mkdir(folder_name)

def store_in_db(g_id, g_name):
	conn = sqlite3.connect("gesture_db.db")
	cmd = "INSERT INTO gesture (g_id, g_name) VALUES (%s, \'%s\')" % (g_id, g_name)
	conn.execute(cmd)
	conn.commit()

def get_hand_hist():
	with open("hist", "rb") as f:
		hist = pickle.load(f)
	return hist

def image_preprocess(i):
	images = glob(f'gestures_2/{i}/*.jpeg')
	pic_no = 0
	create_folder("gestures/" + str(i))
	for image in images:
		img = cv2.imread(image, 0)
		img = cv2.flip(img, 1)
		#imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		imgHSV = img
		hist = get_hand_hist()
		dst = cv2.calcBackProject([imgHSV], [0, 1], hist, [0, 180, 0, 256], 1)
		disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
		cv2.filter2D(dst, -1, disc, dst)
		blur = cv2.GaussianBlur(dst, (11, 11), 0)
		blur = cv2.medianBlur(blur, 15)
		thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
		thresh = cv2.merge((thresh, thresh, thresh))
		thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
		thresh = cv2.bitwise_not(thresh)
		cv2.imwrite("gestures/" + str(i) + "/" + str(pic_no) + ".jpeg", thresh)
		pic_no += 1

init_create_folder_database()
for i in range(10):
	image_preprocess(i)
	store_in_db(i, i)
for i in range(10, 36):
	image_preprocess(i)
	store_in_db(i, chr(i+87))
