# Cobot_Object_Picker
An automated system using MyCobot and YOLO to detect, pick up, and place objects based on color and angle recognition.
![Image](https://github.com/user-attachments/assets/407b0578-cdab-4887-bea2-33b7561d84fa)
## Cobot Object Picker

This project is an automated system that utilizes **MyCobot** and **YOLO** to detect, recognize, and pick up objects based on their color and rotation angle.  
The robotic arm analyzes objects via a camera, determines the correct grip angle, and moves them to a designated location.


## 🚀 Features
- Object detection using YOLO
- Color-based object classification (Red, Blue, Green)
- Automated gripping and placement with MyCobot
- Rotation angle adjustment for precise grasping

## 📷 How It Works
1. The camera captures objects and detects their color.
2. YOLO determines the object's rotation angle.
3. MyCobot moves to the object, adjusts the grip angle, and picks it up.
4. The object is placed at a predefined location based on its color.
   ![Image](https://github.com/user-attachments/assets/c5d1c07b-12bc-4a48-ac68-47879e7fb2f4)

![Image](https://github.com/user-attachments/assets/a7bde7c6-7237-42ff-9fbb-de91b99f5149)

## 💻 Installation
```bash
pip install -r requirements.txt
python src/main.py
