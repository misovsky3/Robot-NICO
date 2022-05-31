import cv2
import mediapipe as mp
import math
from nico_structure import *
import time


# calculates angle of three points,while the calculated angle is at the middle point
def calculate_angle(topX, topY, middleX, middleY, bottomX, bottomY):
    degrees = math.degrees(math.atan2(bottomY - topY, bottomX - middleX) - math.atan2(topY - middleY, topX - middleX))
    angle = int(np.abs(degrees))
    if angle > 180:
        angle = 360 - angle

    return angle


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

wCam, hCam = 1280, 960
cam = cv2.VideoCapture(0)
cam.set(3, wCam)
cam.set(4, hCam)

with mp_holistic.Holistic(
        model_complexity=0,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8
) as holistic:
    start_time = None
    while cam.isOpened():
        success, image = cam.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        handList = []

        if results.right_hand_landmarks:
            rightHand = results.right_hand_landmarks
            for id, value in enumerate(rightHand.landmark):
                h, w, c = image.shape

                cx, cy = int(value.x * w), int(value.y * h)
                handList.append([id, cx, cy])

        poseList = []
        if results.pose_landmarks:
            pose = results.pose_landmarks
            for id, value in enumerate(pose.landmark):
                h, w, c = image.shape
                cx, cy = int(value.x * w), int(value.y * h)
                poseList.append([id, cx, cy])

        if handList and poseList:
            WRIST = handList[0][1], handList[0][2]
            THUMB_CMC = handList[1][1], handList[1][2]
            THUMB_MCP = handList[2][1], handList[2][2]
            THUMB_IP = handList[3][1], handList[3][2]
            THUMB_TIP = handList[4][1], handList[4][2]
            INDEX_FINGER_MCP = handList[5][1], handList[5][2]
            INDEX_FINGER_TIP = handList[8][1], handList[8][2]
            RING_FINGER_MCP = handList[13][1], handList[13][2]
            RING_FINGER_TIP = handList[16][1], handList[16][2]
            PINKY_MCP = handList[16][1], handList[16][2]

            LEFT_SHOULDER = poseList[11][1], poseList[11][2]
            RIGHT_SHOULDER = poseList[12][1], poseList[12][2]
            RIGHT_ELBOW = poseList[14][1], poseList[14][2]
            RIGHT_WRIST = poseList[16][1], poseList[16][2]

            r_index_finger = calculate_angle(INDEX_FINGER_TIP[0], INDEX_FINGER_TIP[1], INDEX_FINGER_MCP[0],
                                             INDEX_FINGER_MCP[1], WRIST[0], WRIST[1])
            r_other_fingers = calculate_angle(RING_FINGER_TIP[0], RING_FINGER_TIP[1], RING_FINGER_MCP[0],
                                              RING_FINGER_MCP[1], WRIST[0], WRIST[1])
            r_thumb_lift = calculate_angle(THUMB_MCP[0], THUMB_MCP[1], WRIST[0],
                                           WRIST[1], PINKY_MCP[0], PINKY_MCP[1])
            r_thumb_close = calculate_angle(THUMB_TIP[0], THUMB_TIP[1], THUMB_IP[0],
                                            THUMB_IP[1], THUMB_MCP[0], THUMB_MCP[1])

            r_shoulder_fwd_bwd = None
            r_shoulder_left_right = None
            r_shoulder_lift = None
            r_elbow = None
            r_wrist_rotate = None
            r_wrist_left_right = None

            r_other_fingers_converted = convert_r_other_fingers(r_other_fingers)
            r_index_finger_converted = convert_r_index_finger(r_index_finger)
            r_thumb_lift_converted = convert_r_thumb_lift(r_thumb_lift)
            r_thumb_close_converted = convert_r_thumb_close(r_thumb_close)

            if start_time is None:
                start_time = time.time() * 1000
            print(
                f'{int(time.time() * 1000 - start_time)} 0 {r_other_fingers_converted} 0 {r_index_finger_converted} 0 '
                f'{r_thumb_lift_converted} 0 {r_thumb_close_converted} 2004 2007 2211 1521 2298 '
                f'2030 2184 1961 2650 1943 1383 2935 1990 2143')

        cv2.imshow('Position detection', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()
exit()
