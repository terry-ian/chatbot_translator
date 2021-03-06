from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from googletrans import Translator
translator = Translator()

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Exp3hJTRaHaqE2JoYK7dWuHOo8QIr79dnMsH+q9fw45r3/PpxP87FjS29yoTrsRAzJuzQ8AeF3P50+jcddTKqrgeeoSTQSWvGBVan8yyzz99Wyx9y+sfEfeLxol9dMapD4fff1ei2tIFU0ETRP6b/gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('67e3b4786b262255f2fff4ac3e526b46')

def translator_line(texts):
    lan=translator.detect(texts)
    if lan.lang =='zh-CN' :
        reply=translator.translate(texts, dest='en').text
    elif lan.lang =='zh-TW' :
        reply=translator.translate(texts, dest='en').text
    elif lan.lang =='en' :
        reply=translator.translate(texts, dest='zh-TW').text
    else : reply='你輸入的不是中英文' 
    print(texts)
    return reply

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	messagetext=translator_line(event.message.text)
	message01 = TextSendMessage(text=messagetext)
	line_bot_api.reply_message(event.reply_token, message01)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
