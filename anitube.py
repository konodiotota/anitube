import requests
from bs4 import BeautifulSoup
import twilio
from twilio.rest import Client
import schedule
import time
import os
from dotenv import load_dotenv

load_dotenv()

load_dotenv()

account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")
meu_whatsapp = os.getenv("MEU_WHATSAPP")

client = Client(account_sid, auth_token)


url = 'https://www.anitube.news/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

container = soup.find('div', class_='epiSubContainer')
ep_tags = container.find_all('div', class_='epiItem')

ep_list = []

for ep in ep_tags:
    title = ep.get_text(strip=True)
    link_tag = ep.find('a')
    
    if link_tag:
        link = link_tag.get('href')
        ep_list.append(f"{title}\nLink: {link}\n")

# Montando mensagem
body_text = "Hoje foram lançados os 10 primeiros episódios no AniTube:\n\n"

for item in ep_list[:10]:
    body_text += item + "\n"

body_text += "Então quando chegar em casa aproveite ❤️"

# print(body_text)


def enviar_mensagem():
    client.messages.create(
        from_=twilio_number,
        body=body_text,
        to=meu_whatsapp
    )

enviar_mensagem()
schedule.every().day.at("21:35").do(enviar_mensagem)

while True:
    schedule.run_pending()
    time.sleep(1)
