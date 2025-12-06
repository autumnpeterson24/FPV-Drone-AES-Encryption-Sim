"""
Project: CS303_Project
Author: Autumn Peterson
File: decrypt_fpv.py
Description: Decrypts fpv_encrypted.bin (simulated encrypted fpv drone video stream)
    frame by frame using openCV and AES decryption from pycryptodome. It reads
    width, height, and fps from the original video and writes to a decrypted video file (fpv_decrypted.mp4). 
    Reads nonce length, nonce, tag length, tag, ciphertext length, and ciphertext.
"""

import os # for file path stuff
import struct # for packing and unpacking binary data
import cv2 # for video processing stuff
import numpy as np # for reconstructing frames from bytes
from Crypto.Cipher import AES # Library to use AES-GCM from pycryptodome
import time # for timing

KEY_FILE = "aes_key.bin" # binary file containing the AES key to use for decryption

def load_key()->bytes:
    """ 
    Load the AES key from aes_key.bin.
    
    Returns:
        bytes: The AES key.
    """
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()
    print(f"AES key loaded from -> {KEY_FILE}")
    return key # returns the AES key as bytes

def decrypt_fpv_stream()->float:
    """ Decrypts the FPV drone video stream frame by frame and displays it. """

    # SETTING UP ==========================================
    input_path = "encrypted_stream.bin" # path to the encrypted binary file

    key = load_key() # load the AES key from aes_key.bin (KEY_FILE)

    # Error handling if file does not exist
    if not os.path.exists(input_path):
        print(f"ERROR: Encrypted file not found -> {input_path}")
        exit(1) # exit with error code 1 if the encrypted file is not found

    with open(input_path, "rb") as file:
        # read the header that was written during encryption to figure out how to decrypt (like a recipe)
        magic = file.read(4) # read the magic number (4 bytes)
        if magic != b"FPV1": # check that the magic number for the file is correct so it can be read correctly
            print(f"ERROR: Invalid file format or corrupted file.")
            exit(1) # exit with error code 1 if the magic number is incorrect

        width_bytes = file.read(4) # read width (4 bytes)
        height_bytes = file.read(4) # read height (4 bytes)
        ch_byte = file.read(1) # read channels (1 byte)
        fps_bytes = file.read(4) # read fps (4 bytes)

        # check that all the header information is correctly read
        if len(width_bytes) < 4 or len(height_bytes) < 4 or len(ch_byte) < 1 or len(fps_bytes) < 4:
            print(f"ERROR: Incomplete header information. File may be corrupted.")
            exit(1) # exit with error code 1 if the header information is incomplete

        width = struct.unpack(">I", width_bytes)[0] # unpack width from bytes to integer
        height = struct.unpack(">I", height_bytes)[0] # unpack height from bytes to integer
        channels = struct.unpack(">B", ch_byte)[0] # unpack channels from bytes to integer
        fps = struct.unpack(">f", fps_bytes)[0] # unpack fps from bytes to float

        if fps <=0:
            fps = 30.0 # default to 30 fps if unable to get fps from video (just like in encrypt)

        print(f"Encrypted video properties (Header) - Resolution: {width} x {height}, FPS: {fps}, Channels: {channels}")

        delay_ms = int(1000.0 / 60) # calculate delay between frames in milliseconds for cv2.waitKey()


        frame_count = 0
        start = time.time()


    # CHECKING NONCE, TAG, AND CIPHERTEXT LENGTHS  ==========================
        while True:
            # read nonce length (1 byte)
            nonce_len_bytes = file.read(1) 
            if len(nonce_len_bytes) == 0:
                break # end of file reached

            nonce_len = struct.unpack("B", nonce_len_bytes)[0] # unpack nonce length
            nonce = file.read(nonce_len) # read nonce

            if len(nonce) < nonce_len:
                print(f"ERROR: Incomplete nonce data. File may be corrupted.")
                exit(1) # exit with error code 1 if nonce data is incomplete

            tag_len_bytes = file.read(1) # read tag length (1 byte)
            if not tag_len_bytes:
                print(f"ERROR: Incomplete tag length data. File may be corrupted.")
                exit(1) # exit with error code 1 if tag length data is incomplete

            tag_len = struct.unpack("B", tag_len_bytes)[0] # unpack tag length
            tag = file.read(tag_len) # read tag to ensure data integrity
            if len(tag) < tag_len:
                print(f"ERROR: Incomplete tag data. File may be corrupted.")
                exit(1) # exit with error code 1 if tag data is incomplete

            ct_len_bytes = file.read(4) # read ciphertext length (4 bytes)
            if len(ct_len_bytes) < 4:
                print(f"ERROR: Incomplete ciphertext length data. File may be corrupted.")
                exit(1) # exit with error code 1 if ciphertext length data is incomplete

            ct_len = struct.unpack(">I", ct_len_bytes)[0] # unpack ciphertext length
            ciphertext = file.read(ct_len) # read ciphertext
            if len(ciphertext) < ct_len:
                print(f"ERROR: Incomplete ciphertext data. File may be corrupted.")
                exit(1) # exit with error code 1 if ciphertext data is incomplete

            # START ACTUAL DECRYPTION PROCESSING HERE: ==================
            try:
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce) # create AES-GCM cipher object with the nonce
                plaintext = cipher.decrypt_and_verify(ciphertext, tag) # decrypt the ciphertext and verify with the tag
            
            except Exception as e:
                print(f"ERROR: Decryption failed for frame {frame_count}. Possible data corruption. {str(e)}")
                continue # skip the frame if decryption fails

            expected_size = width * height * channels
            if len(plaintext) != expected_size:
                print(f"ERROR: Decrypted frame size mismatch for frame {frame_count}. Expected {expected_size} bytes, got {len(plaintext)} bytes.")
                continue # skip the frame if size mismatch occurs

            frame = np.frombuffer(plaintext, dtype=np.uint8) # convert plaintext bytes back to numpy array
            frame = frame.reshape((height, width, channels)) # reshape to original frame dimensions

            # Show the frame!
            cv2.imshow("Decrypted FPV Video Stream: ", frame)
            frame_count += 1

            key_pressed = cv2.waitKey(1) & 0xFF # wait for the calculated delay between frames (60 frame per seconds)
            if key_pressed == ord('q'): # quit if 'q' is pressed
                print("Decryption interrupted by user.")
                break
            
        end = time.time()
        elapsed = end - start

        print(f"[Decrypted Video Processing Time]: {frame_count} frames in {elapsed:.2f} sec -> {frame_count/elapsed:.2f} FPS") # print out data for comaprison against unencrypted stream

    cv2.destroyAllWindows()

    return frame_count/elapsed # return the frames per second of the decrypted video stream

