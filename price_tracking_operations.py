import time
import serial_operations as serial_ops
from API_operations import fetch_tickers, filter_tickers
from image_operations import create_text_to_image

def start_price_tracking(port, baudrate, drive_letter, selected_pair):
    ser = serial_ops.setup_serial_connection(port, baudrate)
    if ser:
        try:
            text = f"{selected_pair['instId'].split('-')[0]}=\n${selected_pair['last']}"
            output_file = f"{drive_letter}:\\latest_price.png"
            create_text_to_image(240, 280, (0, 0, 0), text, "MontserratBlack-3zOvZ.ttf", 35, (255, 255, 255), output_file)
            serial_ops.send_command(ser, f"AT+SP=latest_price.png")
            time.sleep(5)
        finally:
            serial_ops.close_serial_connection(ser)

def track_price_updates(api_url, selected_pair, drive_letter):
    while True:
        tickers = fetch_tickers(api_url)
        updated_ticker_info = filter_tickers(tickers, selected_pair['instId'])
        selected_pair = updated_ticker_info[0]

        background_color = (0, 0, 0)
        text_color = (255, 255, 255)
        font = "MontserratBlack-3zOvZ.ttf"
        text = f"{selected_pair['instId'].split('-')[0]}=\n{selected_pair['last']}"
        output_file = f"{drive_letter}:/latest_price.png"

        create_text_to_image(240, 280, text, font, 35, text_color, background_color, output_file)

        print("Price update sent to Busy Tag")

        time.sleep(10)