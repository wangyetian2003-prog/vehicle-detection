#!/usr/bin/env python3
import rospy, cv2, json
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
from cv_bridge import CvBridge
from ultralytics import YOLO

VEHICLE_CLASSES = {2:'car', 3:'motorcycle', 5:'bus', 7:'truck'}

class VehicleDetector:
    def __init__(self):
        self.bridge = CvBridge()
        rospy.loginfo("Loading YOLOv8n model...")
        self.model = YOLO('yolov8n.pt')
        self.pub_img  = rospy.Publisher('/detections/image/compressed', CompressedImage, queue_size=1)
        self.pub_json = rospy.Publisher('/detections/json', String, queue_size=1)
        rospy.Subscriber('/hikcamera/image_2/compressed', CompressedImage, self.callback, queue_size=1)
        rospy.loginfo("Detector ready.")

    def callback(self, msg):
        frame = self.bridge.compressed_imgmsg_to_cv2(msg, 'bgr8')
        results = self.model(frame, conf=0.4, verbose=False)[0]
        detections = []
        for box in results.boxes:
            cls = int(box.cls[0])
            if cls not in VEHICLE_CLASSES:
                continue
            x1,y1,x2,y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            label = f"{VEHICLE_CLASSES[cls]} {conf:.2f}"
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(frame,label,(x1,y1-8),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)
            detections.append({'class':VEHICLE_CLASSES[cls],'conf':round(conf,3),'bbox':[x1,y1,x2,y2]})
        out_msg = CompressedImage()
        out_msg.header = msg.header
        out_msg.format = "jpeg"
        out_msg.data = cv2.imencode('.jpg', frame)[1].tobytes()
        self.pub_img.publish(out_msg)
        self.pub_json.publish(json.dumps(detections))

if __name__ == '__main__':
    rospy.init_node('vehicle_detector')
    VehicleDetector()
    rospy.spin()
