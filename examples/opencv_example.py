"""
An example of using LiveConfig with an OpenCV application.
Example usages:
    >>> example_instance width 800
    >>> example_instance text Goodbye, World

This changes the width of the frame without needing to restart the program.
"""

import cv2
from liveconfig import liveclass, liveinstance, start_interface, LiveConfig

LiveConfig("./examples/opencv_variables.json")

start_interface("web")

camera = cv2.VideoCapture(0)

@liveclass
class ExampleClass:
    def __init__(self, text):
        self.text = text
        self.font_scale = 1
        self.width = 600
        self.height = 600
        self.threshold = 0.5
        self.show_text = False
        self.color = (255, 255, 255)
        self.mixed_tuple = (0, "Hello", 3.14, True)
        self.mixed_list = [1, "Goodbye", 2.71, False]

example = liveinstance("example_instance")(ExampleClass("Hello, World"))


while True:
    ret, frame = camera.read()
    if not ret:
        print("Error reading frame")
        break

    frame = cv2.resize(frame, (example.width, example.height))

    height, width, _ = frame.shape
    text_position = (width // 2 - 100, height // 2)  # Adjust offset for centering
    cv2.putText(frame, example.text, text_position, cv2.FONT_HERSHEY_SIMPLEX, example.font_scale, example.color, 2)
    cv2.putText(frame, str(example.mixed_tuple), (100, 200), cv2.FONT_HERSHEY_SIMPLEX, example.font_scale, example.color, 2)
    cv2.putText(frame, str(example.mixed_list), (100, 400), cv2.FONT_HERSHEY_SIMPLEX, example.font_scale, example.color, 2)
    if example.show_text and example.threshold > 0.5:
        cv2.putText(frame, "Hidden text", (100,100), cv2.FONT_HERSHEY_SIMPLEX, example.font_scale, example.color, 2)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()