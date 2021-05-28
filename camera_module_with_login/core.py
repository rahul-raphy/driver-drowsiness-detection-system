from keras.preprocessing.image import img_to_array
from keras.models import load_model
import cv2
import numpy as np
from database import *
from imutils import face_utils
from scipy.spatial import distance
import dlib
import face_recognition
detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'models/_mini_XCEPTION.106-0.65.hdf5'
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

def detect_emotion(frame,face):
	EMOTIONS = ["angry","disgust","scared", "happy", "sad", "surprised","neutral"]
	(fX, fY, fW, fH) = face
	roi = frame[fY:fY + fH, fX:fX + fW]
	roi = cv2.resize(roi, (48, 48))
	roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	roi = roi.astype("float") / 255.0
	roi = img_to_array(roi)
	roi = np.expand_dims(roi, axis=0)
	preds = emotion_classifier.predict(roi)[0]
	emotion_probability = np.max(preds)

	angry = preds[0] * 100
	disgust = preds[1] * 100
	scared = preds[2] * 100
	happy = preds[3] * 100
	sad = preds[4] * 100
	surprised = preds[5] * 100
	neutral = preds[5] * 100

	if sad > 7:
		label = 'sad'
	elif scared > 4:
		label = 'scared'
	elif neutral > 65:
		label = 'neutral'

	else:
		top_ip = np.argmax(preds)
		label = EMOTIONS[preds.argmax()]


	
	cv2.putText(frame, label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
	cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH),(0, 0, 255), 2)
	return label


def get_user_id(frame,face):
	(fX, fY, fW, fH) = face
	roi = frame[fY:fY + fH, fX:fX + fW]
	roi = np.asarray(roi)
	face_locations = face_recognition.face_locations(roi)
	print(face_locations)
	return 2


def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear
def check_distraction(gray,shape):
	size = gray.shape
	
	focal_length = size[1]
	center = (size[1]/2, size[0]/2)
	camera_matrix = np.array(
							 [[focal_length, 0, center[0]],
							 [0, focal_length, center[1]],
							 [0, 0, 1]], dtype = "double"
							 )
	model_points = np.array([
							(0.0, 0.0, 0.0),             # Nose tip
							(0.0, -330.0, -65.0),        # Chin
							(-225.0, 170.0, -135.0),     # Left eye left corner
							(225.0, 170.0, -135.0),      # Right eye right corne
							(-150.0, -150.0, -125.0),    # Left Mouth corner
							(150.0, -150.0, -125.0)      # Right mouth corner
						
						])
	image_points = np.array([
							shape[33],     # Nose tip
							shape[8],     # Chinq
							shape[36],     # Left eye left corner
							shape[45],     # Right eye right corne
							shape[48],     # Left Mouth corner
							shape[54]      # Right mouth corner
						], dtype="double")
	dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
	(success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

	(nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
	p1 = ( int(image_points[1][0]), int(image_points[1][1]))
	p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
	dista = distance.euclidean(p1,p2)
	if dista < 60:
		return "normal"
	else:
		return "distraction"

def check_eye(gray,shape):
	thresh = 0.25
	leftEye = shape[lStart:lEnd]
	rightEye = shape[rStart:rEnd]

	# compute the center of mass for each eye
	leftEyeCenter = leftEye.mean(axis=0).astype("int")
	rightEyeCenter = rightEye.mean(axis=0).astype("int")


	leftEAR = eye_aspect_ratio(leftEye)
	rightEAR = eye_aspect_ratio(rightEye)
	ear = (leftEAR + rightEAR) / 2.0
	leftEyeHull = cv2.convexHull(leftEye)
	rightEyeHull = cv2.convexHull(rightEye)
	cv2.drawContours(gray, [leftEyeHull], -1, (0, 255, 0), 1)
	cv2.drawContours(gray, [rightEyeHull], -1, (0, 255, 0), 1)
	if ear < thresh:
		return "closed"
	else:
		return "open"

def process_frame(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	subjects = detect(gray, 0)
	if len(subjects) > 0:
		shape = predict(gray, subjects[0])
		shape = face_utils.shape_to_np(shape)
		eye = check_eye(gray,shape)
		distraction = check_distraction(gray,shape)
		print(eye,distraction)
		return eye,distraction
	else:
		return "open","normal"