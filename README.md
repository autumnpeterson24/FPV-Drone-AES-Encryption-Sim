# FPV Video Encryption/Decryption using AES-GCM 
## Project Description
This project demonstrates how an FPV (First-Person-View) drone video feed can be secured using AES-GCM (Advanced Encryption Standard-Galois Counter Mode), applied frame-by-frame to simulate a real encrypted video stream. The system includes:

- Offline encryption of a simulated drone video (fpv_vid.mp4)

- Real-time decryption + playback of the encrypted video stream

- Performance measurement comparing unencrypted vs. decrypted vs. encrypted throughput

- A simple test harness (main.py) to run the full pipeline

## Included Libraries / Resources
### Libraries:
 - OpenCV (https://opencv.org/)
 - PyCryptodome (https://pypi.org/project/pycryptodome/)
 - Numpy (https://numpy.org/)
 - Pixabay [for video] (https://pixabay.com/videos/flight-fpv-drone-mountain-and-forest-287291/)

 ## How to Install and Run Yourself
 ### Version Dependencies
 1. Ensure you have Python 3.13
 2. Ensure you have VSCode (for ease of use)
 ### Clone the Repository
 3. Open your terminal
 4. Clone the repo
 ```bash
git clone https://github.com/autumnpeterson24/FPV-Drone-AES-Encryption-Sim.git
```
### Activate the Virtual Environment
5. Open the repo in VS Code
6. Set up your virtual environment (Make sure you are in **FPV-Drone-AES-Encryption-Sim** directory)
    - press Ctrl + Shift + p
    - choose the Python interpreter (Python 3.13)
    - choose to use the dependencies from requirements.txt (is a checkbox)
    - build the environment
    * This will automatically install all the libraries/dependencies needed for the project
7. Activate your virtual environment:
In the terminal:
```bash
.venv/Scripts/activate
```
### Run the project
8. Press the 'Run Code' play button in the upper right corner to run the project