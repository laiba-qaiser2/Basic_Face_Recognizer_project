import cv2

# Load Haar Cascade Classifier
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Open Camera
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Camera Settings
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
video_capture.set(cv2.CAP_PROP_FPS, 30)
video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not video_capture.isOpened():
    print("Error: Camera open nahi ho saka.")
    exit()

print("Camera ON... Press 'Q' to Quit")

while True:
    ret, frame = video_capture.read()

    if not ret:
        print("Frame read nahi hua.")
        break

    # Mirror effect
    frame = cv2.flip(frame, 1)

    # Gray image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize for faster detection
    small_gray = cv2.resize(gray, (320, 240))

    # Face Detection
    faces = face_cascade.detectMultiScale(
        small_gray,
        scaleFactor=1.2,
        minNeighbors=6,
        minSize=(30, 30)
    )

    # Draw rectangles on original frame
    for (x, y, w, h) in faces:
        x = x * 2
        y = y * 2
        w = w * 2
        h = h * 2

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    cv2.imshow("Basic Face Recognizer - Hex Softwares", frame)

    # Exit on Q key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()