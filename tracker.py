import cv2
import math

class EuclideanDistTracker:
    def __init__(self):
        self.center_points = {} # centerPoints{(id,c),.....}
        self.id_count = 0

    def update(self, objects_rect):
        objects_bbs_ids = []
        for rect in objects_rect:
            x, y, w, h = rect  # unpack data
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            print(cx, cy)
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                if dist < 50:
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break
            if not same_object_detected:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1  # id will be incremented for the next detected object id
                print(self.center_points)
        return objects_bbs_ids

tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("C:\\Users\\HADITH\\Desktop\\timeDoor\\comp vision\\meeting6\\highway.mp4")
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        break  # Exit loop if frame not read correctly

    roi = frame[340:720, 500:800]
    mask = object_detector.apply(roi)  # Apply on ROI
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # return ->(contours, hierarchy)
    detections = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            cv2.drawContours(roi, [cnt], -1, (0,255,0), 2)
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])

    boxes_ids = tracker.update(detections)
    
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y - 15),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print(detections)

    cv2.imshow("Frame", roi)
    key = cv2.waitKey(30)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()