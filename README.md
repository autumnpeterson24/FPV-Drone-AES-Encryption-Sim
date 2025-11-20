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
