from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('xkBUXC5l2JbTiNvkTO5h+K/WSEpa2TFWpZVY5pCzE3uCbFuD32+GH0NFVg1XG5kivN5vCYKVwqxZ+U6Wj1wtSLL+bKlN+7J5EvcBResdyu6CmCX+14/m4xe7vvEr3QCcRjVmqRt6Y3AhOQqh6ZdHYgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('77c8c45210b487b41c067303a7c89660')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，你說什麼'

    if '給我貼圖' in msg :
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return


    if msg in['hi', 'Hi'] :
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '定位' in msg :
        r = '你想定位，是嗎?'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()