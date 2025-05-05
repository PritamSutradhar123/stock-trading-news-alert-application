import requests
from datetime import timedelta, datetime
import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText

STOCK = "TSLA"
COMPANY_NAME = "tesla"
STOCK_API_KEY = "<>"
NEWS_API_KEY = "<>"
MY_EMAIL = "<>"
PASSWORD = "<>"  # Replace with your App Password
TO_EMAIL = "<>"



params1 = {
    "function":"TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey":STOCK_API_KEY,
}


response = requests.get(url="https://www.alphavantage.co/query",params=params1)
response.raise_for_status()
TMS_data = response.json()['Time Series (Daily)']
TMS_data = response1['Time Series (Daily)']



def difference(ts_y, ts_db_y):
    percentage = ((ts_y - ts_db_y)/ts_db_y)*100
    print(percentage)
    if percentage >= 5:
        subject = "Tesla stock🔺5%"
        get_news(subject)
    elif percentage <= -5:
        subject = "Tesla stock🔻5%"
        get_news(subject)
    else:
        pass


now = datetime.now()
yesterday = now - timedelta(days=3)
day_before_yesterday = now - timedelta(days=4)

params2 = {
    'q':COMPANY_NAME,
    'from':yesterday,
    'sortBy':'publishedAt',
    'language':'en',
    'apiKey':NEWS_API_KEY,
}
def get_news(subject):

    response2 = requests.get(url="https://newsapi.org/v2/everything",params=params2).json()
    article_list = []
    for i in range(3):
        news_company = response2['articles'][i]['source']['name']
        url = response2['articles'][i]['url']
        headline = response2['articles'][i]['title']
        brief = response2['articles'][i]['description']

        article_list.append(f"{' '*50}\n"
              f"From : {news_company}\n"
              f"Headline : {headline}\n"
              f"Brief : {brief}\n"
              f"Article URL : {url}")
    cleaned_message = "\n".join(article_list)
    message = MIMEMultipart()
    message['From'] = MY_EMAIL
    message['To'] = TO_EMAIL
    message['Subject'] = subject
    message.attach(MIMEText(cleaned_message, 'plain'))

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=TO_EMAIL,
                            msg=message.as_string())


if now.weekday() in [0,1,6] and "one"=="t":
    print("hellp")
    pass
else:
    TMS_data_yesterday = TMS_data[str(yesterday.date())]
    TMS_data_day_before_yesterday = TMS_data[str(day_before_yesterday.date())]
    difference(float(TMS_data_yesterday['4. close'])+8,float(TMS_data_day_before_yesterday['4. close']))



