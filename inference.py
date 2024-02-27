import cv2
from ultralytics import YOLO
import pyOptris as optris
from PIL import Image
import numpy as np
import time
model = YOLO('./best.pt')

optris.load_DLL()

# USB connection initialisation 
optris.usb_init("config_file.xml")

result = optris.set_palette(optris.ColouringPalette.IRON)

w, h = optris.get_palette_image_size()
print("{} x {}".format(w, h))
f = 0
fps_time = 0
while True:
    f += 1
    frame = optris.get_palette_image(w, h)
    result = model.predict(frame, save=False, show_conf=True)
    frame = cv2.putText(frame, '%d, FPS: %.2f' % (f, 1.0 / (time.time() - fps_time)),
                            (w-150, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    fps_time = time.time()
    # cv2.imshow("IR streaming", frame)
    for res in result:
        res_img = res.plot()
        im = res_img[..., ::-1]
        # out.write(im)
        if res.probs.top1:
            frame = cv2.putText(frame, 'Water: %.2f' % (res.probs.top1conf.float()),
                                (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        else:
            frame = cv2.putText(frame, 'Normal: %.2f' % (res.probs.top1conf.float()),
                                (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Detect", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

optris.terminate()
cv2.destroyAllWindows()

