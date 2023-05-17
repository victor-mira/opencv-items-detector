![Release](https://img.shields.io/badge/Release-v1.0-blueviolet)
![Language](https://img.shields.io/badge/Language-Python-0052cf)
![Libraries](https://img.shields.io/badge/Libraries-OpenCV_Numpy_Matplotlib_Panda-20d645)

# Items detector with OpenCV
### :warning: This was a School project with a deadline, thus it is not finished at the moment :warning:

This project allow to detects obects added in a room with the same camera position but the lighting can be different.

## How to run
Run main.py in a console with the path to the room images folder. The folder should contain a reference images with no objects on the floor named "Reference.JPG".
```
>>> py main.py 'my-folder/'
```
Example with this project data:
```
>>> py main.py 'Images/Salon/'
```
The program will then ask you to draw the limit of the floor. A click allow to add a point to the polygon, when the shape is defined you can press a key to draw the mask.
| ![image](https://github.com/victor-mira/opencv-items-detector/assets/58742508/aa01bb1a-3da1-47a8-9d63-4a96de148c13) | ![image](https://github.com/victor-mira/opencv-items-detector/assets/58742508/1cf6ab23-7360-49c2-b0c9-d777e92ffc98) |
| :-------------: |:-------------:|
| *Tracing the polygon* | *The displayed mask* |

The mask will then be saved in the images folder and you won't be asked to draw it again.

## Process
The first step is to reduces the high lights that can affect the detection because of the saturation. For that we apply a threshoding on the high values of the image that we etend with closing. With use the telea algorithm to replace this zones. Then we equalize the light of the test image with the reference image histogram. We apply a Blur to reduce noise and we compare the images based on their strucural similaritty. After opening and clothing to asssure structure of the objects we highlight them with a bounding box on the test image.

| ![image](https://github.com/victor-mira/opencv-items-detector/assets/58742508/707f75df-0399-4320-a8d8-66b97bf149a8) | ![image](https://github.com/victor-mira/opencv-items-detector/assets/58742508/dd9c7c73-e8db-4d4f-9d2e-a07e534bf9e1) |
| :-------------: |:-------------:|
| *Different steps on the bedroom images* | *Different steps on the kitchen images* |

## Results
The programm work pretty well on every rooms except on the salon when the curtain is open. Despite of the light treatment, the high lightning remain a problem.

| ![image](https://github.com/victor-mira/opencv-items-detector/assets/58742508/0b871b96-2236-484c-b4ee-8b3655b19e3c) | ![image](https://github.com/victor-mira/opencv-items-detector/assets/58742508/5a63f51d-8004-4849-81f4-738f0b1efbe2) |
| :-------------: |:-------------:|
| *Salon treatment when the curtain is closed* | *Salon treatment when the curtain is open* |

