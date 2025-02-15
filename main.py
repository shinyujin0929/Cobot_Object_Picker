import cv2
import numpy as np
from ultralytics import YOLO
import time
from pymycobot.mycobot import MyCobot
import cobot_module
import camera_file


# 각도 업데이트 함수
angle = cobot_module.current_angle
camera_file.update_detected_angle(angle)

# MyCobot 연결 설정
mc = MyCobot('COM3', 115200)

red_detection_count = 0  # 초기 인식 횟수 설정

cobot_module.initialize_cobot(mc)
cobot_module.open_gripper(mc)

# yolo 실행 및 물체 탐지 후 로봇팔 동작
def run_process():
    global red_detection_count
# 서보 모터 활성화 -> 그리퍼 초기화 -> 초기 위치-> 카메라 촬영 위치
    cobot_module.move_to_camera_position(mc)

    # YOLO를 통해 물체 탐지 및 각도 계산
    # YOLO를 통해 물체 탐지 및 각도 계산
    detected_color = camera_file.yolo_run()
    print(f"Detected color: {detected_color}")  # 반환된 값 출력

    # 색상에 따른 목적지 이동

    if detected_color == 'Red':
        red_detection_count += 1  # Red 인식 시 카운트 증가

        if red_detection_count == 1:
            cobot_module.destination_red_1(mc)
        elif red_detection_count == 2:
            cobot_module.destination_red_2(mc)
        elif red_detection_count == 3:
            cobot_module.destination_red_3(mc)

        
    elif detected_color == 'Blue':
        cobot_module.destination_blue(mc)
    elif detected_color == 'Green':
        cobot_module.destination_green(mc)

        print("green")

    elif detected_color == 'Error':
        cobot_module.destination_error(mc)  # 그 외의 경우(오류 등) 목적지 4


    # 그리퍼 오픈
    cobot_module.open_gripper(mc)
    cobot_module.initialize_cobot(mc)





# if __name__ == "__main__":
#     run_process()
if __name__ == "__main__":
    for i in range(6):
        print(f"Starting process {i+1}")
        run_process()
        time.sleep(1)