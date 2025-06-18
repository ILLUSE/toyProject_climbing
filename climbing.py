import cv2
import mediapipe as mp

# MediaPipe 초기화
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 영상 경로
video_path = "C:/Users/Chaeun/.vscode/toyProject_climbing/video.MOV"
cap = cv2.VideoCapture(video_path)

# 출력 저장 설정
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_stickman.mp4', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

# 좌표 스무딩 설정
prev_joints = {}
smooth_factor = 0.7  # 떨림 보정: 이전 좌표 비율

# Pose 모델 시작
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 전처리
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            h, w, _ = image.shape
            lm = results.pose_landmarks.landmark

            # 좌표 추출 + 스무딩
            def pt(name):
                part = mp_pose.PoseLandmark[name].value
                x, y = int(lm[part].x * w), int(lm[part].y * h)
                if name in prev_joints:
                    px, py = prev_joints[name]
                    x = int(smooth_factor * px + (1 - smooth_factor) * x)
                    y = int(smooth_factor * py + (1 - smooth_factor) * y)
                prev_joints[name] = (x, y)
                return x, y

            # 관절들
            joints = {
                "head": pt("NOSE"),
                "left_shoulder": pt("LEFT_SHOULDER"),
                "right_shoulder": pt("RIGHT_SHOULDER"),
                "left_elbow": pt("LEFT_ELBOW"),
                "right_elbow": pt("RIGHT_ELBOW"),
                "left_wrist": pt("LEFT_WRIST"),
                "right_wrist": pt("RIGHT_WRIST"),
                "left_hip": pt("LEFT_HIP"),
                "right_hip": pt("RIGHT_HIP"),
                "left_knee": pt("LEFT_KNEE"),
                "right_knee": pt("RIGHT_KNEE"),
                "left_ankle": pt("LEFT_ANKLE"),
                "right_ankle": pt("RIGHT_ANKLE"),
                "left_ear": pt("LEFT_EAR"),
                "right_ear": pt("RIGHT_EAR"),
            }

            # 머리: 귀 사이 원
            try:
                head_center = (
                    int((joints["left_ear"][0] + joints["right_ear"][0]) / 2),
                    int((joints["left_ear"][1] + joints["right_ear"][1]) / 2)
                )
                head_radius = int(abs(joints["left_ear"][0] - joints["right_ear"][0]) / 2.2)
                cv2.circle(image, head_center, head_radius, (255, 255, 0), 2)
            except:
                pass  # 귀가 안 잡히면 생략

            # 몸통: 중심 간 선
            shoulder_center = (
                int((joints["left_shoulder"][0] + joints["right_shoulder"][0]) / 2),
                int((joints["left_shoulder"][1] + joints["right_shoulder"][1]) / 2)
            )
            hip_center = (
                int((joints["left_hip"][0] + joints["right_hip"][0]) / 2),
                int((joints["left_hip"][1] + joints["right_hip"][1]) / 2)
            )
            cv2.line(image, shoulder_center, hip_center, (255, 255, 255), 2)

            # 팔
            cv2.line(image, joints["left_shoulder"], joints["left_elbow"], (0, 255, 0), 2)
            cv2.line(image, joints["left_elbow"], joints["left_wrist"], (0, 255, 0), 2)
            cv2.line(image, joints["right_shoulder"], joints["right_elbow"], (0, 255, 0), 2)
            cv2.line(image, joints["right_elbow"], joints["right_wrist"], (0, 255, 0), 2)

            # 다리
            cv2.line(image, joints["left_hip"], joints["left_knee"], (0, 0, 255), 2)
            cv2.line(image, joints["left_knee"], joints["left_ankle"], (0, 0, 255), 2)
            cv2.line(image, joints["right_hip"], joints["right_knee"], (0, 0, 255), 2)
            cv2.line(image, joints["right_knee"], joints["right_ankle"], (0, 0, 255), 2)

            # 손/발 강조
            for name in ["left_wrist", "right_wrist", "left_ankle", "right_ankle"]:
                cv2.circle(image, joints[name], 6, (0, 255, 255), -1)

        # 실시간 출력 + 저장
        cv2.imshow('Stickman Climber', image)
        out.write(image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 마무리
cap.release()
out.release()
cv2.destroyAllWindows()
