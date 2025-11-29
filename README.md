# SMS_Stock_Alerts

## :book: Introduction
Like any other investor, there are some companies which I follow closely; and Crowdstrike is one of them. I have created a script that triggers email alerts when the closing prices between the recent 2 days are higher than 1% (this number be adjusted plus I don't recommend anyone to obsess over a stock's price)


## :computer: Tech Stack
1. Script = Python
2. Trigger SMS alerts = Twilio
3. Stock API = AlphaVantage
4. Stock news API = News API


## :white_check_mark: Key Features (App Ready)

1. Crowdstrike stock price checker (checks the closing yesterday and closing 2 days ago).
2. Price difference checker (triggers SMS alerts if price difference > $1).
3. Fetch latest Crowdstrike news (included in the SMS alerts)

  
## :x: Limitations

1. Code structure can be in modules for readability and maintainability. Perhaps, the SMS trigger part can be in a function in a different class.
2. Can be hosted in PythonAnywhere to run it everyday.


## :bowtie: Reflections
This was one of the hardest projects to work on. The most challenging part was storing the dictionary keys into lists and using the same list items to retrive the respective values. Google and StackOverflow were my best friends during the hardship. It didn't help that AlphaVantage limited me to 25 calls from an IP address in a day.


Difficulty Level: 8️⃣
