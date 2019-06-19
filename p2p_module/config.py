from dotenv import load_dotenv
import os
load_dotenv()


dest_server_host = os.getenv(
    "DESTINATION_SERVER_ADDRESS")

dest_server_port = int(os.getenv(
    "DESTINATION_SERVER_PORT"))

dest_client_host = os.getenv(
    "DESTINATION_CLIENT_ADDRESS")

dest_client_port = int(os.getenv(
    "DESTINATION_CLIENT_PORT"))

self_server_host = os.getenv(
    "SELF_SERVER_ADDRESS")

self_server_port = int(os.getenv(
    "SELF_SERVER_PORT"))

self_client_host = os.getenv(
    "SELF_CLIENT_ADDRESS")

self_client_port = int(os.getenv(
    "SELF_CLIENT_PORT"))

owner_key_file_name = os.getenv(
    "OWNER_KEY_FILE_NAME")

receiver_key_file_name = os.getenv(
    "RECEIVER_KEY_FILE_NAME")

encryption_file_name = os.getenv(
    "ENCRYPTION_FILE_NAME")

decryption_file_name = os.getenv(
    "DECRYPTION_FILE_NAME")

buffer_size = 16384