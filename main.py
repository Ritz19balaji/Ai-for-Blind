import pyttsx3
from picamera import PiCamera
from time import sleep
import pytesseract
from PIL import Image
from io import BytesIO

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to detect text in an image using Tesseract OCR
def detect_text(image):
    # Open the image using PIL (Python Imaging Library)
    img = Image.open(BytesIO(image))
    
    # Convert the image to grayscale
    img_gray = img.convert('L')

    # Perform thresholding to improve contrast
    threshold = 100  # Adjust this value as needed
    img_threshold = img_gray.point(lambda p: p > threshold and 255)

    # Save intermediate results for debugging
    img.save('captured_image.jpg')
    img_gray.save('gray_image.jpg')
    img_threshold.save('threshold_image.jpg')

    # Perform text detection using Tesseract OCR
    # Replace the language parameter 'eng' with the language of your text if needed
    text = pytesseract.image_to_string(img_threshold, lang='eng')
    return text

# Function to capture image from the camera, detect text, and play it as audio
def capture_detect_and_play_audio():
    # Initialize the camera
    camera = PiCamera()
    camera.resolution = (640, 480)

    # Allow the camera to warm up
    sleep(2)

    while True:
        # Capture image from the camera
        img_stream = BytesIO()
        camera.capture(img_stream, format='jpeg')
        img_stream.seek(0)
        
        # Detect text in the captured image
        detected_text = detect_text(img_stream.getvalue())

        # If text is detected, play it as audio
        if detected_text:
            print("Detected Text:", detected_text)
            speak(detected_text)

# Call the function to capture image from the camera, detect text, and play it as audio
capture_detect_and_play_audio()
