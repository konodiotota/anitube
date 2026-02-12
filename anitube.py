import requests
from bs4 import BeautifulSoup
import twilio
from twilio.rest import Client
import schedule
import time
import os
from dotenv import load_dotenv

load_dotenv()

#Neste programa é necessário criar um arquivo .env, na mesma pasta que o programa, com as seguintes variáveis:
#TWILIO_SID=your_twilio_sid
#TWILIO_TOKEN=your_twilio_auth_token
#TWILIO_NUMBER=your_twilio_phone_number (com o código do país, ex: +5511999999999)
#MEU_WHATSAPP=your_whatsapp_number (com o código do país, ex: +5511999999999)  
#Não podendo esquecer de criar uma conta no Twilio e configurar o WhatsApp Sandbox para obter os números necessários.

account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")
meu_whatsapp = os.getenv("MEU_WHATSAPP")

#nesta parte do codigo puxara tua conta do Twilio usando as variáveis de ambiente para autenticação e envio de mensagens.

client = Client(account_sid, auth_token)

#Aqui o código faz uma requisição para o site do AniTube, utilizando a biblioteca requests para obter o conteúdo da página.
#Em seguida, a biblioteca BeautifulSoup é usada para analisar o HTML e extrair as informações dos episódios lançados.

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
body_text = "Hoje foram lançados os 12 primeiros episódios no AniTube:\n\n"

for item in ep_list[:12]:
    body_text += item + "\n"

body_text += "Então quando chegar em casa aproveite ❤️"

print(body_text)

def enviar_mensagem():
    client.messages.create(
        from_=twilio_number,
        body=body_text,
        to=meu_whatsapp
    )

if __name__ == "__main__":
    enviar_mensagem()
