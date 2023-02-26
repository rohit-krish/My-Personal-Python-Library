import time
import cv2


class GetFPS:
    def __init__(self) -> None:
        self.prev_time = 0
        self.curr_time = 0

    def get(self):
        self.curr_time = time.time()
        fps = 1/(self.curr_time-self.prev_time)
        self.prev_time = self.curr_time
        return int(fps)

    def draw_in_img(self, img, scale=1):
        cv2.rectangle(img, (0, 0), (int(200*scale), int(50*scale)), (100, 46, 21), cv2.FILLED)
        cv2.putText(
            img, f'FPS: {self.get()}', (int(10*scale), int(40*scale)),
            cv2.FONT_HERSHEY_SIMPLEX, 1.5*scale, (255, 255, 255), int(2*scale)
        )
        return img
