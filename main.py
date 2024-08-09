import requests
import time
import json
import os
from API_operations import fetch_tickers, filter_tickers, upload_file, upload_json, delete_file, get_file, check_connection_status, wait_for_reconnection
from image_operations import create_text_to_image
from user_interactions import get_wifi_status, get_ticker_query, get_currency_preference, select_ticker_currency_pair, get_drive_letter, select_ticker
import serial_operations as serial_ops
from price_tracking_operations import track_price_updates
from exception_handlers import handle_connection_error, handle_timeout_error, handle_unexpected_error

api_url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"

def wifi_mode():
    host = input("Enter the host address (e.g., http://busytag-XXXXXX.local): ").strip()
    file_number = 1
    tickers = fetch_tickers(api_url)
    
    selected_pair = select_ticker(tickers)
    
    print("Price tracking has started.")

    background_color = (0, 0, 0)
    text_color = (255, 255, 255)
    font = "MontserratBlack-3zOvZ.ttf"
    text = f"{selected_pair['instId'].split('-')[0]}=\n{selected_pair['last']}"
    create_text_to_image(240, 280, text, font, 35, text_color, background_color, "latest_price.png")
    upload_file(host, "latest_price.png")

    while True:
        if not check_connection_status(host):
            if not wait_for_reconnection(host):
                print("Failed to reconnect after maximum retries. Exiting.")
                break

        try:
            tickers = fetch_tickers(api_url)
            updated_ticker_info = filter_tickers(tickers, selected_pair['instId'])
            selected_pair = updated_ticker_info[0]

            text = f"{selected_pair['instId'].split('-')[0]}=\n{selected_pair['last']}"
            output_file = f"latest_price_{file_number}.png"
            create_text_to_image(240, 280, text, font, 35, text_color, background_color, output_file)

            upload_file(host, output_file)
            print("Price update sent to Busy Tag")

            json_data = get_file(host, "config.json")

            if isinstance(json_data, str):
                try:
                    json_data = json.loads(json_data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    continue
            
            json_data['image'] = output_file
            json_data['show_after_drop'] = False

            json_string = json.dumps(json_data, separators=(',', ':'))

            upload_json(host, "config.json", json_string)

            if file_number == 1:
                delete_file(host, "latest_price.png")
                os.remove("latest_price.png") 
            else:
                delete_file(host, output_file)
                os.remove(output_file)  
            print("Next update after 10 seconds")
            time.sleep(10)
            file_number += 1

        except requests.ConnectionError as e:
            handle_connection_error(e)
        except requests.Timeout as e:
            handle_timeout_error(e)
        except Exception as e:
            handle_unexpected_error(e)

def usb_mode():
    drive_letter = get_drive_letter()
    tickers = fetch_tickers(api_url)
    baudrate = 115200
    device_connected = False

    selected_pair = select_ticker(tickers)

    print(f"Price tracking has started and is displayed on Busy Tag")

    try:
        while True:
            port = serial_ops.find_busy_tag_device()
            if port:
                if not device_connected:
                    print("Busy Tag device is connected. Resuming price tracking...")
                    device_connected = True

                try:
                    track_price_updates(api_url, selected_pair, drive_letter)
                except FileNotFoundError as e:
                    print(f"An unexpected error occurred: {e}")
                    print("Try to reconnect the Busy Tag device.")
                except requests.ConnectionError as e:
                    handle_connection_error(e)
                except requests.Timeout as e:
                    handle_timeout_error(e)
                except Exception as e:
                    handle_unexpected_error(e)
            else:
                if device_connected:
                    print("The Busy Tag device has been disconnected. Please reconnect the device.")
                device_connected = False
                print("Next update after 10 seconds")
                time.sleep(10)

    except KeyboardInterrupt:
        print("Price tracking stopped.")


def main():
    connection_type = input("Is the busy tag connected via Wi-Fi or USB? (wifi/usb): ").strip().lower()
    if connection_type == 'wifi':
        wifi_mode()
    elif connection_type == 'usb':
        usb_mode()
    else:
        print("Invalid choice. Please enter 'wifi' or 'usb'.")
        main()

if __name__ == "__main__":
    main()