from ultralytics import YOLO
import cv2 as cv
import numpy as np
from utils.geometry import KeyPoints
from deep_models.detector.face_detector import face_detector

# kpt_color_map = {
#    0:'Nose',
#        1:'Right Eye',
#        2:'Left Eye',
#        3:'Right Ear',
#        4:'Left Ear',
#        5:'Right Shoulder',
#        6:'Left Shoulder',
#        7:'Right Elbow',
#        8:'Left Elbow',
#        9:'Right Wrist',
#        10:'Left Wrist',
#        11:'Right Hip',
#        12:'Left Hip',
#        13:'Right Knee',
#        14:'Left Knee',
#        15:'Right Ankle',
#        16:'Left Ankle',
# }
global skeleton
skeleton = [

    [10, 8],
    [8, 6],
    [6, 5],
    [5, 7],
    [7, 9]
]


def draw_circle(frame, point_list, radius=5, color=(255, 0, 0), frame_shape=(640, 480)):

    for idx, point in enumerate(point_list):
        x, y = np.multiply(point, frame_shape).astype(int)

        cv.circle(frame, (x, y), radius, color, -1)


def draw_line(frame, kpts: np.ndarray, color=(255, 0, 0), frame_shape=(640, 480)):

    for i, sk in enumerate(skeleton):

        pt1 = (int(np.multiply(kpts[sk[0]][0], frame_shape[0])), int(
            np.multiply(kpts[sk[0]][1], frame_shape[1])))
        pt2 = (int(np.multiply(kpts[sk[1]][0], frame_shape[0])), int(
            np.multiply(kpts[sk[1]][1], frame_shape[1])))

        if pt1[0] % frame_shape[1] == 0 or pt1[1] % frame_shape[0] == 0 or pt1[0] < 0 or pt1[1] < 0:
            continue

        if pt2[0] % frame_shape[1] == 0 or pt2[1] % frame_shape[0] == 0 or pt2[0] < 0 or pt2[1] < 0:
            continue

        cv.line(frame, pt1, pt2, color, 2)


def kp(inx1, idx2, idx3):

    kp1 = key_points.point_xy(inx1)
    kp2 = key_points.point_xy(idx2)
    kp3 = key_points.point_xy(idx3)

    return kp1, kp2, kp3


def is_hostile(left_angle, right_angle):

    hostile = True

    # check if the hand is raised
    if 120 > right_angle > 60 and 120 > left_angle > 60:
        # print("Hand is raised")
        hostile = False

    return hostile


pause = False

model_pose = YOLO("./weights/yolov8n-pose.pt")


cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()

    results = model_pose(frame, show=False, verbose=False)

    if ret:

        for result in results:

            # face = result.boxes.xyxy[0].tolist()

            try:

                faces = face_detector.process(frame)[0]

                kp_array = result.keypoints.xyn[0].cpu().numpy()

                key_points = KeyPoints(kp_array)

                # angle between right shoulder, right elbow and right wrist
                right_shoulder, right_elbow, right_wrist = kp(5, 7, 9)

                # angle between left shoulder, left elbow and left wrist
                left_shoulder, left_elbow, left_wrist = kp(6, 8, 10)

                # calculate the angle
                right_elbow_angle = key_points.calc_angle(right_shoulder,
                                                        right_elbow,
                                                        right_wrist)

                left_elbow_angle = key_points.calc_angle(left_shoulder,
                                                        left_elbow,
                                                        left_wrist)

                draw_circle(frame, [right_shoulder, right_elbow, right_wrist,
                                    left_shoulder, left_elbow, left_wrist])

                draw_line(frame, kp_array)
                # draw_line(frame, np.array(([right_wrist, right_elbow, right_shoulder,
                #                             left_shoulder, left_elbow, left_wrist])))

                if is_hostile(left_elbow_angle, right_elbow_angle):
                    cv.rectangle(
                        frame, (int(faces[0]), int(faces[1])), (int(faces[2]), int(faces[3])), (0, 0, 255), 2)

                    cv.putText(
                        frame, "Hostile", (faces[0], faces[1]-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv.LINE_AA)
                    print("Hostile Detected! Engage!")

                else:
                    cv.rectangle(
                        frame, (int(faces[0]), int(faces[1])), (int(faces[2]), int(faces[3])), (0, 255, 0), 2)
                    cv.putText(frame, "Friendly", (faces[0], faces[1]-5),
                            cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv.LINE_AA)
                    print("Not Hostile")

            except:
               pass

        if pause:
            key = cv.waitKey(0)

        else:
            key = cv.waitKey(1)

        cv.imshow("deneme", frame)

        if key == ord("q"):
            break

        if key == ord("p"):
            if pause:
                pause = False
            else:
                pause = True


cap.release()
cv.destroyAllWindows()


# changing coordinate system

# right_shoulder = (right_shoulder[0], 1-right_shoulder[1])
# right_elbow = (right_elbow[0],  1-right_elbow[1])
# right_wrist = (right_wrist[0],  1-right_wrist[1])
