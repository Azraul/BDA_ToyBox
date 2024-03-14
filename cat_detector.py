import os
import requests
import json
import cv2

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
        cat_image = cv2.imread(cat_url)
        gray_cat_image = cv2.cvtColor(cat_image, cv2.COLOR_BGR2GRAY)

        # Load the cat face Haar cascade
        cat_face_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')

        # Detect cat faces in the image
        cat_faces = cat_face_cascade.detectMultiScale(gray_cat_image, scaleFactor=1.1, minNeighbors=5, minSize=(75, 75))

        if len(cat_faces) > 0:
            print("Cat detected in the image!")
        else:
            print("No cat detected in the image.")
    except Exception as e:
        print(f"Error fetching cat image: {e}")

api_key = os.getenv("CAT_API_KEY")
if api_key:
    get_cat_image(api_key)
else:
    print("Please set your API key as an environment variable.")
