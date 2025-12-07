"""
Project: CS303_Project
Author: Autumn Peterson
File: encrypt_fpv.py
Description: encrypts fpv_vid.mp4 (simulated fpv drone video stream) frame by frame 
    using openCV and AES encryption from pycryptodome. It encrypts by reading
    width, height, and fps from the original video and writing to a binary file (.bin). 
    Converts each frame to bytes using AES-GCM encryption. Writes nonce length, nonce, 
    tag length, tag, and ciphertext length, and ciphertext
    for each frame to the binary file.
"""

import struct # for packing and unpacking binary data
import cv2 # for video processing stuff
from Crypto.Cipher import AES # Library to use AES-GCM from pycryptodome
from Crypto.Random import get_random_bytes # for generating random bytes for AES key and nonce


KEY_FILE = "aes_key.bin" # binary file containing the AES key to use for encryption

def create_aes_key()->bytes:
    """ 
    Create the key to use and saves it to aes_key.bin.
    Uses a 256-bit (32-byte) key for AES-GCM encryption.
    
    Returns:
        bytes: The 256-bit (32-byte) AES key in bytes.
    """
    key = get_random_bytes(32) # 256 bits = 32 bytes
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print(f"AES key generated and saved to -> {KEY_FILE}")
    return key # returns the 256-bit AES key as bytes

def encrypt_fpv_stream()->None:
    """ 
    Encrypts the FPV drone video stream frame by frame and writes to a binary file. 
    
    Returns: 
        None
    """
    vid_path = "media/fpv_vid.mp4" # path to the original video file
    output_path = "encrypted_stream.bin" # path to the encypted binary file

    key = create_aes_key() # create and save the AES key to aes_key.bin (KEY_FILE) and return the 256-bit key as bytes

    cap = cv2.VideoCapture(vid_path) # open the video file using openCV

    if not cap.isOpened(): # opened unsuccessfully
        print(f"ERROR: Can't open video file")
        exit(1) # exit with error code 1 it fails

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # get width of the video frames
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # get height of the video frames
    fps = cap.get(cv2.CAP_PROP_FPS) # get frames per second of the video

    if fps <= 0:
        fps = 30.0 # default to 30 fps if unable to get fps from video

    channels = 3 # using default 3 channels from cv2 (BGR) for color video (BLUE GREEN RED)
    print(f"Video properties - Resolution: {width} x {height}, FPS: {fps}, Channels: {channels}")
    print(f"Video opened successfully for ENCRYPION -> {vid_path}")

    with open(output_path, "wb") as output_file:
        # write out to the binary file the header information needed for decryption
        format_spec = b"FPVf" # The beginning of my file has this (basically the name of my format) MUST BE 4 BYTES
        output_file.write(format_spec)
        output_file.write(struct.pack(">I", width)) # write 4 bytes for width (>I is format for big-endian unsigned int)
        output_file.write(struct.pack(">I", height)) # write 4 bytes for height (>I is format for big-endian unsigned int)
        output_file.write(struct.pack("B", channels)) # write 1 byte for channels (B is format for Byte)
        output_file.write(struct.pack(">f", fps)) # write 4 bytes for fps (>f is format for big-endian float)

        # NOTE: Big endian jsut means that the most-significant byte is stored first (at the lowest memory address)

        # SETUP ===============================================
        frame_count = 0 # keep track of number of frames processed
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # get total number of frames in the video to compare to when seeing progress

        while True:
            ret, frame = cap.read() # read a frame from the video (ret = return value if frame is available, frame = next fram of the vid)
            if not ret: # no more frames to read
                print("End of video file reached.")
                break
            
            # Resize frames here if they come in wonky
            if frame.shape[0] != height or frame.shape[1] != width:
                frame = cv2.resize(frame, (width, height)) # resize frame to match original video dimensions

            # Handle channel mismatch
            if frame.shape[2] != channels:
                raise ValueError(f"Unexpected number of channels in frame: {frame.shape[2]}")
            
            # Convert frame to bytes
            frame_bytes = frame.tobytes() # convert the frame (numpy array) to bytes

            # START ACTUAL ENCRYPTION AND AUTHENTICATION PROCESSING HERE: ==================
            nonce = get_random_bytes(12) # generate a random 96-bit (12-byte) nonce for AES-GCM (what is recommended for AES-GCM)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            ciphertext, tag = cipher.encrypt_and_digest(frame_bytes) # encrypt the frame bytes and get the authentication tag to ensure data integrity

            # Write out the encrypted frame data to the binary file ==================
            # Write nonce length (1 byte), nonce, tag length (1 byte), tag, ciphertext length (4 bytes), ciphertext
            output_file.write(struct.pack("B", len(nonce))) # write 1 byte for nonce length
            output_file.write(nonce) # write the nonce
            output_file.write(struct.pack("B", len(tag))) # write 1 byte for tag length
            output_file.write(tag) # write the tag
            output_file.write(struct.pack(">I", len(ciphertext))) # write 4 bytes for ciphertext length
            output_file.write(ciphertext) # write the ciphertext
            # ========================================================

            frame_count += 1
            if frame_count % 50 == 0: # keep track of progress every 50 frames to see if things are working
                print(f"{frame_count} / {total_frames} frames encrypted and written to {output_path}")

        print(f"Encryption complete!!! Total frames encrypted: {frame_count}")

        cap.release() # release the video capture object


