import requests
import json
import time

def fetch_tickers(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        tickers = [
            {"instId": ticker["instId"], "last": ticker["last"]}
            for ticker in data.get("data", [])
        ]
        return tickers
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def filter_tickers(tickers, query):
    filtered_tickers = [
        ticker for ticker in tickers if ticker["instId"].startswith(query)
    ]
    return filtered_tickers

def get_file(host, filename):
    url = f"{host}/{filename}"
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.headers.get('Content-Type') == 'application/json':
            return response.json()
        else:
            return response.content.decode()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def upload_file(host, filename):
    url = f"{host}/upload/{filename}"
    try:
        with open(filename, 'rb') as file:
            response = requests.post(url, data=file, headers={"Content-Type": "application/octet-stream"})
            response.raise_for_status()
            
            if response.headers.get('Content-Type') == 'application/json':
                return response.json()
            else:
                return response.content.decode()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except FileNotFoundError:
        print("The specified file was not found.")
        return None

def upload_json(host, filename, json_data):
    url = f"{host}/upload/{filename}"
    try:
        response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        if response.headers.get('Content-Type') == 'application/json':
            return response.json()
        else:
            return response.content.decode()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def delete_file(host, filename):
    url = f"{host}/delete/{filename}"
    try:
        response = requests.post(url)
        response.raise_for_status()

        if response.headers.get('Content-Type') == 'application/json':
            return response.json()
        else:
            return response.content.decode()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def check_connection_status(host, timeout=10):
    try:
        response = requests.get(host, timeout=timeout)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
    return False

def wait_for_reconnection(host, retry_interval=10, max_retries=10):
    retries = 0
    while retries < max_retries:
        if check_connection_status(host):
            
            return True
        print("BusyTag is not connected to the Wifi, please re-connect.")
        retries += 1
        print(f"Retrying... ({retries}/{max_retries})")
        time.sleep(retry_interval)