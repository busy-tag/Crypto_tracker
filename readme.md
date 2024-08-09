# Crypto Tracker Script
## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Example](#example)

## Introduction

Crypto Tracker is a Python-based application that tracks the price of a selected cryptocurrency pair and displays the current price on a Busy Tag device. The price is updated regularly and is shown as an image on the Busy Tag display.

## Project Purpose

The main goal of this project is to:
	
- To monitor real-time cryptocurrency prices.

- To display the latest price on a Busy Tag device.

- To handle both Wi-Fi and USB connection modes for updating the Busy Tag.

## Prerequisites

To run this script, ensure you have the following installed:

- Python 3.6 or higher
- `Pillow` (PIL Fork) - Python Imaging Library
- `requests` for API calls
- A Busy Tag device.
- An internet connection for fetching cryptocurrency prices.

## Installation
 
  To get started with this Python script, follow these steps:

1. **Clone the repository:**
   First, clone the repository from GitHub to your local machine.
   ```
   git clone https://github.com/busy-tag/Crypto_tracker.git
2. Navigate to the cloned repository:

	```
	cd cd Crypto_tracker
	```
3. Install the required dependencies:
	Use `pip` to install the necessary packages.
	
	```
	pip install Pillow requests
	```

4. Ensure the default font file `MontserratBlack-3zOvZ.ttf` is in the project directory.

## Configuration

The script provides several customizable parameters:
 
• **Drive Letter:** Prompted input for the drive letter where the Busy Tag device is located (e.g., `D`).

• **Host Address:** When in Wi-Fi mode, input the Busy Tag's network address (e.g., `http://busytag-XXXXXX.local`).

• **Cryptocurrency Pair:** Select the cryptocurrency pair you wish to track (e.g., `BTC-USDT`).

• **Image Processing:** Parameters for cropping, overlaying, and adding text are set in image_operations.py.

## Configuration JSON

The application automatically updates the Busy Tag's config.json file with the following values:
```
{
    "show_after_drop": false,
    "image": "latest_price.png",
    "activate_pattern": true,
    "pattern_repeat": 2,
    "custom_pattern_arr": [
        {"led_bits": 127, "color": "000000", "speed": 10, "delay": 10},
        {"led_bits": 136, "color": "00FF00", "speed": 10, "delay": 5}
    ]
}
```

## Usage
1. **Execute the script:**
You can run the script from the command line:
```
python main.py
```
2. **Select the Connection Mode:**

	Choose between Wi-Fi or USB mode to connect to the Busy Tag device.
	
3. **Select Cryptocurrency Pair:**

	Enter the ticker symbol (e.g., BTC) and choose the desired currency pair to track.
	
4. **Price Tracking:**

The application will fetch and display the latest price on the Busy Tag device at regular intervals.

	
### Example

After running the script, you should see output similar to this in your terminal:
```
Is the busy tag connected via Wi-Fi or USB? (wifi/usb): wifi
Enter the Busy Tag network address (e.g., http://busytag-XXXXXX.local): http://busytag-6120F4.local
Enter cryptocurrency ticker (e.g., BTC) or press enter to see all tickers: BTC
Enter currency - USD or EUR (or press enter to see all pairs): USD
1. BTC-USDC: 59702
2. BTC-USDT: 59658.2
Choose pair - enter number (e.g. 1): 1
You have selected BTC-USDC pair
Price tracking has started and is displayed on Busy Tag
Next update after 10 seconds
```

An image (e.g., latest_price.png) will be saved in the specified directory (e.g., D:), displaying the latest price for the selected pair.
Sample:

<img src="/latest_price_sample.png" alt="Sample Latest Price Image" width="330" height="400"/>

### Troubleshooting ###

If you encounter any issues, ensure:

All Python packages are installed correctly.

The font file (`MontserratBlack-3zOvZ.ttf`) is present in the project directory.

The correct drive letter or host address is provided.

The Busy Tag device is connected and functioning correctly.

For any additional help, please open an issue in the repository or contact the maintainer.
