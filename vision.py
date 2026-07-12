import cv2
import os

def capture_image(save_path="models/capture.jpg"):
    """Capture an image from the default camera"""
    # Ensure directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False
        
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(save_path, frame)
        print(f"Image saved to {save_path}")
    
    cap.release()
    cv2.destroyAllWindows()
    return ret

def detect_objects(image_path):
    """Placeholder for object detection"""
    print(f"Running object detection on {image_path}...")
    # Add YOLO or other OpenCV detection logic here
    return ["person", "laptop"]

if __name__ == "__main__":
    capture_image()
