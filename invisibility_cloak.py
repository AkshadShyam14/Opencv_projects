import numpy as np 
import cv2
import time

def background(cap,num_frames=30):
    print("Capturing frames.")
    bg = []
    for i in range(num_frames):
        ret,frame = cap.read()
        if ret: 
            bg.append(frame)
        else:
            print(f"Could not read frame {i+1}/{num_frames}")
        time.sleep(0.1)
        if bg:
            return np.median(bg,axis=0).astype(np.uint8)
        else:
            raise ValueError("Could not capture any frames for background")

def create_mask(frame,lower_color,upper_color):
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower_color,upper_color)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8),iterations=2)

    return mask

def apply_cloak_effect(frame,mask,backg):
    mask_inv = cv2.bitwise_not(mask)
    fg = cv2.bitwise_and(frame,frame,mask=mask_inv)
    bg = cv2.bitwise_and(backg,backg,mask=mask)
    return cv2.add(fg,bg)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error, could not open camera")
        return
    try:
        bg = background(cap)
    except ValueError as e:
        print(f"Error: {e}")
        cap.release()
        return

    lower_blue = np.array([90,50,50])
    upper_blue = np.array([130,150,150])

    print("Starting main loop. Press q to quit")
    
    while True:
        ret,frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            time.sleep(1)
            continue
        mask = create_mask(frame,lower_blue,upper_blue)
        cloak = apply_cloak_effect(frame,mask,bg)

        cv2.imshow('Invisible cloak',cloak)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()