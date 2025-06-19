# MediaPipe 기반 스틱맨 자세 추적기

이 프로젝트는 [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose.html)와 OpenCV를 활용하여 사람의 자세를 스틱맨 형태로 시각화하는 도구입니다. 영상 파일을 프레임 단위로 처리하여 관절을 인식하고, 스틱맨 스타일로 출력하며 떨림 보정을 적용합니다.

## 만들게 된 계기
@stickclimbs의 영상을 보고 "이걸 프로그램으로 만들어 자신이 등반하는 영상을 스틱맨, 더 나아가 다양한 캐릭터가 등반하는 영상을 만들면 재밌겠다 생각했습니다

-제작을 허락해준 stickclimbs의 인스타

https://www.instagram.com/stickclimbs/
## 📽️ 데모
https://www.youtube.com/shorts/c4w6Rznt5s4


## 🚀 주요 기능

- MediaPipe를 이용한 사람 자세 인식
- 관절 간 선과 원으로 이루어진 스틱맨 형태 시각화
- 실시간 화면 출력 및 결과 영상 저장 (MP4)
- 관절 좌표 스무딩 처리로 떨림 최소화
- 시각화 색상:
  - 흰색: 몸통
  - 초록색: 팔
  - 빨간색: 다리
  - 노란색: 손과 발
  - 하늘색 원: 머리 (양쪽 귀 기준)

## 🛠️ 설치 환경

- Python 3.8 이상
- OpenCV
- MediaPipe

설치 명령어:

```bash
pip install opencv-python mediapipe
```

## 사용 방법
파일 내 video_path 변수에 본인의 영상 경로를 입력 후 실행
```
video_path = "C:/Users/Chaeun/.vscode/toyProject_climbing/video.MOV"
```

## 작동 방식

-Human tracking

1.MediaPipe의 Pose 모델을 통해 각 프레임에서 33개의 주요 관절을 탐지합니다.

2.관절 위치를 이미지 크기에 맞게 2D 좌표로 변환합니다.

3.이전 프레임과의 좌표를 혼합해 스무딩하여 떨림을 줄입니다.

4.관절 간 연결을 선과 원으로 시각화합니다.

5.결과는 화면에 출력되며 동시에 영상으로 저장됩니다.

## 추후 개발/개선될 사항
1.트래킹 정교하게

2.사람 없는 배경 추출 후 트래킹 영상 합성

3.앱/웹으로 제작 후 배포

4.스틱맨 외 다른 캐릭터로 커스텀 가능하게
