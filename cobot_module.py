from pymycobot.mycobot import MyCobot
import time
import keyboard
import cv2
import os

current_angle = 0.0 

def update_detected_angle(angle):
    global current_angle
    current_angle = angle

#서보 해제 / 활성화
def unservoing(mc):
    mc.realease_all_servos()
    print("모든 서보 해제")
    time.sleep(1)
def activate_servos(mc):
    mc.power_on()
    print("모든 서보를 활성화합니다.")

#기본 위치 이동 ( 초기 위치 / 카메라 촬영 위치 )
def initialize_cobot(mc):
    mc.set_gripper_mode(0)
    mc.init_eletric_gripper()
    mc.send_angles([0, 0, 0, 0, 0, 0],50)
    time.sleep(2)

def move_to_camera_position(mc):
    mc.send_angles([3.6, -13.53, -13.27, -58.18, 92.72, 1.93], 50)
    time.sleep(2)

#물체 잡는 위치로 이동
def move_to_grip(mc):
  
    mc.send_angles([2.37, -27.59, -41.66, -21.62, 90.61, -0.17],50)
    time.sleep(2)
    gripper_angle = -0.17 + current_angle
    print("회전 ***")
    mc.send_angles([2.37, -27.59, -41.66, -21.62, 90.61, gripper_angle], 50)
    # 적용된 그리퍼 회전값 출력
    time.sleep(2)
    print(f"Applied gripper rotation angle: {gripper_angle}")


def upside_block(mc):
    mc.send_angles([7.11,-33.48,0.08,-51.06,86.48,3.42],50)
    time.sleep(2)
# def move_to_grip(mc):
#     # 기본 위치로 이동
#     mc.send_angles([2.37, -27.59, -41.66, -21.62, 90.61, -0.17], 50)
#     time.sleep(4)
    
#     # current_angle이 90도일 때는 회전하지 않도록 조건 추가
#     if current_angle == 90:
#         gripper_angle = -0.17  # 90도일 경우 추가 회전 없이 기본값 유지
#     else:
#         gripper_angle = -0.17 + current_angle

#     print("회전 ***")
#     mc.send_angles([2.37, -27.59, -41.66, -21.62, 90.61, gripper_angle], 20)
#     time.sleep(4)
    
#     # 적용된 그리퍼 회전값 출력
#     print(f"Applied gripper rotation angle: {gripper_angle}")


#그리퍼 열기 / 닫기
def open_gripper(mc):
    print("그리퍼 오픈.")
    mc.set_eletric_gripper(0)
    mc.set_gripper_value(60, 40)
    time.sleep(1)

#그리퍼 닫기
def close_gripper(mc):
    print("그리퍼 닫기")
    mc.set_eletric_gripper(1)
    mc.set_gripper_value(20, 40)
    time.sleep(1)



#그리퍼 올림(90도회전)
def gripper_up(mc):
    mc.send_angles([3.51, -22.5, -42.09, -17.13, 2.63, -0.96],50)#그리퍼 올림
    time.sleep(2)

#하역 동작
def landing(mc):
    mc.send_angles([-49.65, -50.71, -59.23, 22.06, 87.11, 88.76],50) #하역
    time.sleep(3)
    #그리퍼 위치조절
def tune_gripper(mc):
    mc.send_angles([-52.2, -39.72, -12.56, -22.93, 87.97, 90],50) #그리퍼돌림
    time.sleep(2)


##################하역 이전 동작########################################
#그린
def before_landing_green(mc):
    mc.send_angles([-52.2, -39.72, -12.56, -22.93, 87.97, 1.84],50) # 하역장소 위로 이동
    time.sleep(1)
#블루
def before_landing_blue(mc):
    mc.send_angles([-36.91,-34.27,-30.05,-13.09,95.27,0],50) # 하역장소 위로 이동
    time.sleep(1)

#레드
def before_landing_red(mc):
    mc.send_angles([-74.5, -39.72, -12.56, -22.93, 87.97, 1.84],50) # 하역장소 위로 이동
    time.sleep(1)

##################하역 동작######################################
#그린
def landing_green(mc):
    mc.send_angles([-49.65, -50.71, -59.23, 22.06, 87.11, 88.76],30) #하역
    time.sleep(2)

def landing_green_fix(mc):
    mc.send_angles([-45.79, -82.96, 65.65, -67.58, 88.15, 95.71],30) #하역
    time.sleep(2)

#블루
def landing_blue(mc):
    mc.send_angles([-36.56,-63.98,-24.69,-0.7,94.74,87.18],30) #하역 4번 모터 수정해야함
    time.sleep(2)
def landing_blue_after(mc):
    mc.send_angles([-36.91,-34.27,-30.05,-13.09,95.27,0],30)
    time.sleep(2)

#레드
def landing_red(mc):
    mc.send_angles([-64.68, -64.95, -16.78, -7.47, 87.01, 88.24],30) #하역
    #mc.send_angles([-64.42, -63.19, -31.2, 6.67, 86.92, 88.5 ],30) #하역
    time.sleep(3)
def landing_red_2(mc):
    mc.send_angles([-67.41, -53.08, -27.86, -3.42, 89.64, 87.71],30) #하역
    time.sleep(2)
def landing_red_3(mc):
    mc.send_angles([-64.2, -63.0, 0.79, -23.0, 87.09, 90.83],30) #하역
    
    
    time.sleep(2)
def landing_red_fix(mc):
    mc.send_angles([ -64.68, -64.95, -16.78, -7.47, 87.01, 0],30) #하역
    time.sleep(2)
######################그리퍼 위치조정###################
def tune_gripper_green(mc):
    mc.send_angles([-52.2, -39.72, -12.56, -22.93, 87.97, 90],50) #그리퍼돌림
    time.sleep(1)
def tune_gripper_blue(mc):
    mc.send_angles([-36.91,-34.27,-30.05,-13.09,95.27,90],50) #그리퍼돌림
    time.sleep(1)
def tune_gripper_red(mc):
    mc.send_angles([-77.0, -39.72, -12.56, -22.93, 87.97, 90],50) #그리퍼돌림
    time.sleep(1)
########################################################







#그리퍼1

def destination_green(mc):
    open_gripper(mc)
    move_to_camera_position(mc)
    upside_block(mc)
    move_to_grip(mc)
    close_gripper(mc)
    gripper_up(mc)
    initialize_cobot(mc)
    before_landing_green(mc)
    tune_gripper_green(mc)
    landing_green(mc)
    open_gripper(mc)
    landing_green_fix(mc)
    #landing_green(mc)
    initialize_cobot(mc)

def destination_blue(mc):
    open_gripper(mc)
    move_to_camera_position(mc)
    upside_block(mc)
    move_to_grip(mc)
    close_gripper(mc)
    gripper_up(mc)
    initialize_cobot(mc)
    before_landing_blue(mc)
    tune_gripper_blue(mc)
    landing_blue(mc)
    open_gripper(mc)

    before_landing_blue(mc)
    initialize_cobot(mc)
    initialize_cobot(mc)


def destination_red_1(mc):
    open_gripper(mc)
    move_to_camera_position(mc)
    upside_block(mc)
    move_to_grip(mc)
    close_gripper(mc)
    gripper_up(mc)
    initialize_cobot(mc)
    before_landing_red(mc)
    tune_gripper_red(mc)
    landing_red(mc)
    open_gripper(mc)
    initialize_cobot(mc)

def destination_red_2(mc):
    open_gripper(mc)
    move_to_camera_position(mc)
    upside_block(mc)
    move_to_grip(mc)
    close_gripper(mc)
    gripper_up(mc)
    initialize_cobot(mc)
    before_landing_red(mc)
    tune_gripper_red(mc)
    landing_red_2(mc)
    open_gripper(mc)
    landing_red(mc)
    close_gripper(mc)
    open_gripper(mc)
    landing_red_fix(mc)
    close_gripper(mc)
    open_gripper(mc)
    before_landing_red(mc)
    initialize_cobot(mc)

def destination_red_3(mc):
    open_gripper(mc)
    move_to_camera_position(mc)
    upside_block(mc)
    move_to_grip(mc)
    close_gripper(mc)
    gripper_up(mc)
    initialize_cobot(mc)
    before_landing_red(mc)
    tune_gripper_red(mc)
    landing_red_3(mc)
    open_gripper(mc)
    initialize_cobot(mc)

def destination_error(mc):
    open_gripper(mc)
    move_to_camera_position(mc)
    upside_block(mc)
    move_to_grip(mc)
    close_gripper(mc)
    gripper_up(mc)
    initialize_cobot(mc)
    mc.send_angles([-90,0,0,0,0,0],50) #하역
    
    time.sleep(2)
    open_gripper(mc)

