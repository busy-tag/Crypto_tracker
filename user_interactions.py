from API_operations import fetch_tickers, filter_tickers

def get_wifi_status():
    wifi_status = input("Is the busy tag connected to wifi? (y/n): ").strip().lower()
    if wifi_status not in ['y', 'n']:
        print("Invalid input. Please enter 'y' or 'n'.")
        return get_wifi_status()
    return wifi_status

def get_ticker_query():
    ticker_query = input("Enter cryptocurrency ticker (e.g., BTC) or press enter to see all tickers: ").strip().upper()
    return ticker_query

def get_currency_preference():
    currency = input("Enter currency - USD or EUR (or press enter to see all pairs): ").strip().upper()
    if currency in ['USD', 'EUR'] or currency == '':
        return currency
    else:
        print("Invalid input. Please enter 'USD' or 'EUR', or press enter to see all pairs.")
        return get_currency_preference()

def select_ticker_currency_pair(filtered_tickers):
    try:
        choice = int(input("Choose pair - enter number (e.g. 1):\n "))
        if 1 <= choice <= len(filtered_tickers):
            return filtered_tickers[choice - 1]
        else:
            print("Invalid choice. Please select a number from the list.")
            return select_ticker_currency_pair(filtered_tickers)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return select_ticker_currency_pair(filtered_tickers)

def get_drive_letter():
    while True:
        drive_letter = input("Please enter the drive letter assigned to Busy Tag device (e.g., D): ").strip().upper()
        if len(drive_letter) == 1 and drive_letter.isalpha():
            return drive_letter
        else:
            print("Invalid drive letter. Please enter a single letter (e.g., D).")

def display_tickers(tickers):
    for ticker in tickers:
        print(ticker)

def fetch_and_filter_tickers(api_url, query):
    tickers = fetch_tickers(api_url)
    return filter_tickers(tickers, query)

def display_filtered_tickers(filtered_tickers):
    for index, ticker in enumerate(filtered_tickers, start=1):
        print(f"{index}. {ticker['instId']}: {ticker['last']}")

def select_ticker(tickers):
    while True:
        ticker_query = get_ticker_query()

        if not ticker_query:
            for ticker in tickers:
                print(ticker)
            break

        filtered_tickers = filter_tickers(tickers, ticker_query)

        if filtered_tickers:
            break
        else:
            print(f"No tickers found for '{ticker_query}'. Please try again.")

    currency = get_currency_preference()

    if ticker_query and currency != '':
        filtered_tickers = filter_tickers(tickers, f"{ticker_query}-{currency}")
    else:
        filtered_tickers = filter_tickers(tickers, ticker_query)

    for index, ticker in enumerate(filtered_tickers, start=1):
        print(f"{index}. {ticker['instId']}: {ticker['last']}")

    if filtered_tickers:
        selected_pair = select_ticker_currency_pair(filtered_tickers)
    
    print(f"You have selected {selected_pair['instId']} pair")

    return selected_pair