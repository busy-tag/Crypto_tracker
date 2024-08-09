import requests

def handle_connection_error(e):
    print(f"Connection error occurred: {e}")
    print("Re-checking host connectivity...")

def handle_timeout_error(e):
    print(f"Timeout error occurred: {e}")
    print("Re-checking host connectivity...")

def handle_unexpected_error(e):
    print(f"An unexpected error occurred: {e}")
    print("Re-checking host connectivity...")