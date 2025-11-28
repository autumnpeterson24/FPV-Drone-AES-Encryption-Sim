"""
Main for CS 303 Project - FPV Drone Video Encryption and Decryption
Author: Autumn Peterson
Description: This is the main file to run the encryption and decryption of a simulated FPV drone video stream and compare them.

"""
import encrypt_fpv as e_fpv
import decrypt_fpv as d_fpv
import cv2
import time

def play_unecrypted_video(video_path: str)->None:
    """ Play the unencrypted video for comparison. """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"ERROR: Can't open video file {video_path}")
        return

    delay_ms = int(1000.0 / 60) # calculate delay between frames in milliseconds for cv2.waitKey()
    frame_count = 0 # keep track of number of frames processed
    start = time.time() # time how long it takes to see if there is latency
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        cv2.imshow('Unencrypted Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): # press q to quit the video
            break
    end = time.time()

    elapsed = end - start
    
    print(f"[Original Unencrypted Video Processing Time]: {frame_count} frames in {elapsed:.2f} sec -> {frame_count/elapsed:.2f} FPS")

    cap.release()
    cv2.destroyAllWindows()

    return frame_count/elapsed # return the frames per second of the unencrypted video stream

if __name__ == "__main__":
    print("Starting FPV Drone Video Encryption...")
    e_fpv.encrypt_fpv_stream() # functions made in encrypt_fpv.py
    print("Encryption complete.\n")

    print("Starting FPV Drone Video Decryption...")
    fps_decrypted = d_fpv.decrypt_fpv_stream() # funtions made in encrypt_fpv.py

    print("Playing unencrypted video for comparison...")
    fps_unecrypted = play_unecrypted_video("media/fpv_vid.mp4")

    overhead = (1 - (fps_decrypted / fps_unecrypted)) * 100.0

    print(f"Overhead introduced by encryption/decryption: {overhead:.2f}%")