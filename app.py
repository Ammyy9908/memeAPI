import random
import requests
from bs4 import BeautifulSoup
from flask import Flask,send_file
from PIL import Image
from io import BytesIO

from werkzeug.wrappers import response

app = Flask(__name__)

def getMemes():
    url = "https://www.memedroid.com/memes/tag/programming"
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'lxml')
    divs = soup.find_all('div',class_='item-aux-container')
    imgs = []
    for div in divs:
        img = div.find('img')['src'];
        if img.startswith('http') and img.endswith('jpeg'):
            imgs.append(img)
    return imgs

def serveImage(image):
    img_io = BytesIO()
    image.save(img_io,'JPEG',quality=70)
    img_io.seek(0)
    return send_file(img_io,mimetype='image/jpeg')


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/",methods=['GET'])
def return_meme():
    img_url = random.choice(getMemes())
    res = requests.get(img_url,stream=True)
    res.raw.decode_content = True
    img = Image.open(res.raw)
    return serveImage(img)
