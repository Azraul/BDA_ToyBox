import urllib
import numpy as np
import requests
import json
import cv2
import subprocess

def url_to_image(url):
    try:
        with urllib.request.urlopen(url) as response:
            arr = np.asarray(bytearray(response.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # Load it as a color image
            return img
    except urllib.error.URLError as e:
        print(f"Error fetching image from URL: {e}")
        return None

def get_cat_image(api_key):
    url = "https://api.thecatapi.com/v1/images/search"
    params = {
        "api_key": api_key,
        "limit": 1
    }

    try:
        response = requests.get(url, params=params)
        cat_data = json.loads(response.content)
        cat_url = cat_data[0]["url"]
        print(f"Here's your cat image: {cat_url}")

        # Load the cat image and convert it to grayscale
        cat_image = url_to_image(cat_url)
        print(cat_image)
        if cat_image is not None:
        # Convert the image to grayscale
            gray_image = cv2.cvtColor(cat_image, cv2.COLOR_BGR2GRAY)
            print("Grayscale conversion successful!")
            # Load the cat face Haar cascade
            cat_face_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')

            # Detect cat faces in the image
            cat_faces = cat_face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(75, 75))

            if len(cat_faces) > 0:
                print("Cat detected in the image!")
                # Convert the cat image to ASCII art using img2txt
                subprocess.run(["img2txt", cat_image])
            else:
                print("No cat detected in the image.")
        else:
            print("Error loading the cat image. Check the URL or network connection.")
    except Exception as e:
        print(f"Error fetching cat image: {e}")

api_key = "live_ZbAFQMfuCAvsmAkfyxgJarl5LFLGpAFkD7Kh8HTOtekXTxXKPGODzkHmNqwpXdu3"
if api_key:
    get_cat_image(api_key)
else:
    print("Please set your API key as an environment variable.")
