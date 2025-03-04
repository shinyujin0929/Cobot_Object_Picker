import cv2
import numpy as np
from ultralytics import YOLO
import time
import cobot_module


def update_detected_angle(angle):
    # cobot_module.current_angle을 직접 업데이트
    cobot_module.current_angle = angle
    print(f"Detected angle updated to: {cobot_module.current_angle}")  # 디버깅 메시지

    
# 이전 각도를 전역 변수로 설정
previous_angle = None
# 카메라 위치로 이동
def find_contour(roi, frame, angle_file, x1, y1, x2, y2):
    global previous_angle  # 전역 변수를 사용하여 이전 각도 저장
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # 색상 범위 설정
    color_ranges = {
        'red': [(np.array([0, 50, 50]), np.array([10, 255, 255]))],
        'green': [(np.array([40, 50, 50]), np.array([80, 255, 255]))],
        'blue': [(np.array([100, 150, 0]), np.array([140, 255, 255]))]
    }

    morphed_masks = []
    for color, ranges in color_ranges.items():
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for lower, upper in ranges:
            mask |= cv2.inRange(hsv, lower, upper)
        morphed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((2, 2), np.uint8))
        morphed_masks.append(morphed_mask)

    contours = []
    for morphed_mask in morphed_masks:
        cnts, _ = cv2.findContours(morphed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours.extend(cnts)
    
    print(f"Contours detected: {len(contours)}")  # 윤곽선 개수 디버깅
    
    changed_angle = None
    if contours:
        standard_contour = max(contours, key=cv2.contourArea)
        print(f"Max contour area: {cv2.contourArea(standard_contour)}")  # 가장 큰 윤곽선의 면적
        
        if cv2.contourArea(standard_contour) > 300:
            rect = cv2.minAreaRect(standard_contour)
            box = np.int0(cv2.boxPoints(rect))
            angle = rect[2]

            # 바운딩 박스 그리기
            cv2.polylines(frame, [box + (x1, y1)], isClosed=True, color=(255, 0, 0), thickness=2)
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

            print(f"Detected angle: {angle}")  # 감지된 각도 디버깅

            # 각도 변화 감지
            if previous_angle is None or abs(angle - previous_angle) >= 20:
                changed_angle = angle  # 새로 감지된 각도를 저장
                previous_angle = angle  # 마지막 각도를 업데이트
                
                # 감지된 각도를 업데이트하는 함수 호출
                update_detected_angle(changed_angle)
                
                try:
                    with open(angle_file, 'a') as f:
                        f.write(f"{changed_angle:.2f}\n")
                except IOError as e:
                    print(f"파일에 각도를 저장하는 데 오류 발생: {e}")
                print(f"Angle changed: {changed_angle}")
            else:
                print(f"Initial Angle: {angle}")

            # 현재 각도와 이전 각도 출력
            print(f"Current Angle: {angle}, Previous Angle: {previous_angle}")
            return angle, changed_angle

    return None, None

def capture_and_display_with_angle(frame, angle):
    # 캡처된 이미지와 각도 정보를 표시하는 창 생성
    captured_image = frame.copy()
    cv2.putText(captured_image, f"Rotation Angle: {angle:.2f} degrees", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Captured Frame with Angle", captured_image)
    cv2.waitKey(0)  # 창이 닫힐 때까지 기다림
    cv2.destroyWindow("Captured Frame with Angle")

def yolo_run():
    previous_position = None
    previous_time = None
    stationary_threshold = 2.0
    detected_angle = None
    model = YOLO(r'C:/mypro/kairos_project/runs/detect/train2/weights/best.pt')
    cap = cv2.VideoCapture(1)
    angle_file = "changed_angles.txt"
    detected_color = None  # 감지된 색상 저장

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        results = model(frame)
        height, width, _ = frame.shape
        detected_objects = []
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].numpy()
            if 0 < x1 < 1 and 0 < y1 < 1 and 0 < x2 < 1 and 0 < y2 < 1:
                x1, y1, x2, y2 = x1 * width, y1 * height, x2 * width, y2 * height
            x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
 
            # ROI 영역 설정 후 윤곽선 검출
            roi = frame[y1:y2, x1:x2]
            angle, changed_angle = find_contour(roi, frame, angle_file, x1, y1, x2, y2)
            if angle is not None:
                detected_angle = changed_angle  # 새로 감지된 각도를 저장
            
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            detected_objects.append((center_x, center_y))

        if detected_objects:
            current_position = detected_objects[0]
            if previous_position:
                movement = np.linalg.norm(np.array(current_position) - np.array(previous_position))
                if movement < 10:  # 10픽셀 이하 움직이면 정지한 것으로 판단
                    if previous_time is None:
                        previous_time = time.time()
                    elif time.time() - previous_time >= stationary_threshold:
                        print("객체 정지 감지 | 캡처 및 동작 수행")
                        capture_and_display_with_angle(frame, detected_angle)
                        break  
                else:
                    previous_time = None  
            previous_position = current_position  

        cv2.imshow('Webcam', frame)


    cap.release()
    cv2.destroyAllWindows()

    return detected_color  # 감지된 색상을 반환



if __name__ == "__main__":
    yolo_run()