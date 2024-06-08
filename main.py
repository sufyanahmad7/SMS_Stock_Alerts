import requests
import os
from twilio.rest import Client

STOCK = "CRWD"
COMPANY_NAME = "Crowdstrike"
ALPHA_VANTAGE_API = os.environ.get("ALPHA_VANTAGE_API")
NEWS_API = os.environ.get("NEWS_API")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

stock_parameters = {
    "apikey" : ALPHA_VANTAGE_API,
    "symbol" : STOCK,
    "function" : "TIME_SERIES_DAILY"
}

# STEP 1: Use https://www.alphavantage.co to get the stock prices.
response = requests.get("https://www.alphavantage.co/query", params=stock_parameters)
response.raise_for_status()
stock_data = response.json()

# Retrieve the values from the dictionary and store them in a list.
keys_list = list(stock_data["Time Series (Daily)"].keys())

# Another way to retrieve the values from the dictionary and store them in a list.
# data_list = [value for (key, value) in stock_data.items()]

# Access first and second item of the stock data.
yesterday = stock_data["Time Series (Daily)"][keys_list[0]]
two_days_ago = stock_data["Time Series (Daily)"][keys_list[1]]
print(f"Yesterday numbers : {yesterday}")
print(f"Two days ago numbers : {two_days_ago}")

# Access close price of first and second item.
# Item is in string with decimal places. Hence, the next step is to convert to float and then int.
yesterday_close = int(float(stock_data["Time Series (Daily)"][keys_list[0]]["4. close"]))
two_days_ago_close = int(float(stock_data["Time Series (Daily)"][keys_list[1]]["4. close"]))
print(f"Yesterday close : {yesterday_close}")
print(f"Two days ago close : {two_days_ago_close}")

# Calculates the percentage difference between two days.
percentage_difference = round(((yesterday_close - two_days_ago_close) / two_days_ago_close) * 100, 1)
print(f"Percentage difference : {percentage_difference}")

# STEP 2: Use https://newsapi.org to get the first 2 news pieces for the COMPANY_NAME.
news_parameters = {
        "apiKey" : NEWS_API,
        "q": COMPANY_NAME,
        "symbol": STOCK,
        "language": "en",
        "searchIn": "title",
        "sortBy" : "publishedAt",
        "pageSize" : 2,
    }

response = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
response.raise_for_status()
news_data = response.json()

for item in news_data["articles"]:

    print (item["title"])
    print(item["content"])
    print(item["url"])

    title = item["title"]
    content = item["content"]
    url = item["url"]

    # STEP 3: Use https://www.twilio.com to send SMSes of the percentage change, each article's title and description to your phone number.
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    if percentage_difference > 1:
        message = client.messages \
            .create(
            body=f"{STOCK}: ⬆ {percentage_difference}% \n\nHeadline: {title} \n\nBrief: {content} \n\nRead more: {url}",
            from_='+13253269505',
            to='+6594596619'
        )
    elif percentage_difference < -1:
        message = client.messages \
            .create(
            body=f"{STOCK}: ⬇ {percentage_difference}% \n\nHeadline: {title} \n\nBrief: {content} \n\nRead more: {url}",
            from_='+13253269505',
            to='+6594596619'
        )

    print(f"News data :{news_data}")
    print(f"Message ID : {message.sid}")
    print(f"Message status : {message.status}")

    # Optional: Format the SMS message like this:
    """
    TSLA: 🔺2%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
    or
    "TSLA: 🔻5%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
    """
