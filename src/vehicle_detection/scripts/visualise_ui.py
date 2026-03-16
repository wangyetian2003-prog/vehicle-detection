#!/usr/bin/env python3
import rospy, json, cv2, numpy as np
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
from collections import defaultdict

class UI:
    def __init__(self):
        self.frame  = None
        self.counts = defaultdict(int)
        rospy.Subscriber('/detections/image/compressed', CompressedImage, self.cb_img)
        rospy.Subscriber('/detections/json', String, self.cb_json)

    def cb_img(self, msg):
        arr = np.frombuffer(msg.data, np.uint8)
        self.frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    def cb_json(self, msg):
        dets = json.loads(msg.data)
        self.counts = defaultdict(int)
        for d in dets:
            self.counts[d['class']] += 1

    def run(self):
        rate = rospy.Rate(30)
        while not rospy.is_shutdown():
            if self.frame is not None:
                disp = self.frame.copy()
                cv2.rectangle(disp,(5,5),(220,35+28*max(len(self.counts),1)),(0,0,0),-1)
                y = 28
                total = sum(self.counts.values())
                cv2.putText(disp,f'Total: {total}',(10,y),cv2.FONT_HERSHEY_SIMPLEX,0.65,(255,255,255),2)
                y += 28
                for cls,cnt in self.counts.items():
                    cv2.putText(disp,f'{cls}: {cnt}',(10,y),cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,255,255),2)
                    y += 28
                cv2.imshow('Vehicle Detection - AAE4011', disp)
                if cv2.waitKey(1) == 27:
                    break
            try:
                rate.sleep()
            except rospy.exceptions.ROSTimeMovedBackwardsException:
                pass
        cv2.destroyAllWindows()

if __name__ == '__main__':
    rospy.init_node('vehicle_ui')
    UI().run()
