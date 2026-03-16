#!/usr/bin/env python3
import rosbag, cv2, os, numpy as np
from cv_bridge import CvBridge

def extract(bag_path, topic, out_dir):
    bridge = CvBridge()
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    img = None
    with rosbag.Bag(bag_path) as bag:
        for _, msg, _ in bag.read_messages(topics=[topic]):
            img = bridge.compressed_imgmsg_to_cv2(msg, 'bgr8')
            cv2.imwrite(os.path.join(out_dir, f'frame_{count:06d}.jpg'), img)
            count += 1
    if img is not None:
        print(f"Extracted {count} frames. Resolution: {img.shape[1]}x{img.shape[0]}")

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--bag',   default='/home/brocolli/catkin_ws/src/vehicle_detection/data/2026-02-02-17-57-27.bag')
    p.add_argument('--topic', default='/hikcamera/image_2/compressed')
    p.add_argument('--out',   default='/home/brocolli/catkin_ws/src/vehicle_detection/data/frames/')
    args = p.parse_args()
    extract(args.bag, args.topic, args.out)
