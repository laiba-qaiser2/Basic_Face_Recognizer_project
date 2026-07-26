# Project : Basic Face Recognizer

This repository contains the source code for **Project 01: Basic Face Recognizer**, completed as part of the AI Internship at **Hex Softwares**.

## Project Description
The goal of this project is to create a real-time face detection script. Instead of building and training an AI model from scratch, this project utilizes Python and the OpenCV library with a pre-trained Haar Cascade Classifier (`haarcascade_frontalface_default.xml` / `alt2`) to accurately detect human faces through a webcam.

## Features
* Real-time face detection using the computer's webcam.
* Draws a green bounding box around the detected face.
* Optimized parameters (scaleFactor, minNeighbors) to reduce false positives and background noise.

## Requirements
To run this project, you will need to have Python installed on your system along with the OpenCV library.

Install the required library using pip:
```bash
pip install opencv-python
How to Run the Project
1.Clone this repository to your local machine.
2.Open your terminal or command prompt and navigate to the project folder.
3.Run the following command:
python face_recognizer.py
1.Your webcam will turn on, and a window will pop up showing the live video feed with face tracking.
2.To close the program, simply click on the video window and press the 'q' key on your keyboard.

##Acknowledgements


OpenCV for their open-source computer vision library and pre-trained models.
