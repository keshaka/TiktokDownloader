import json
from requests import *
from datetime import datetime
from tiktok_module import downloader
from dotenv import dotenv_values

token_bot = dotenv_values()['token_bot']
api = "https://api.telegram.org/bot" + token_bot
update_id = 0


def SendVideo(userid, msgid):
    tg_url = api + "/sendvideo"
    data = {
        "chat_id": userid,
        "caption": "<b>Video Downloaded from</b> @ti_down_bot!\n\n<b>EN</b> : <i>if the video is blank send url again!</i>\n<b>සිංහල</b> : <i> වැඩ කරේ නැත්තං ආය් ලින්ක් එක එවන්න</i>",
        "parse_mode": "html",
        "reply_to_message_id": msgid,
        "reply_markup": json.dumps({
            "inline_keyboard": [
                [
                    {
                        "text": "⭕️ සිංහල උපසිරසි සමග චිත්‍රපටි බලන්න මේක ඔබන්න ⭕️",
                        "url": "https://t.me/Films_l_tv_series"
                    }
                ]
            ]
        })
    }
    res = post(
        tg_url,
        data=data,
        files={
            "video": open("video.mp4", "rb")
        }
    )


def SendMsg(userid, text, msgid):
    tg_url = api + "/sendmessage"
    post(tg_url, json={"chat_id": userid, "text": text,
         "parse_mode": "html", "reply_to_message_id": msgid})


def get_time(tt):
    ttime = datetime.fromtimestamp(tt)
    return f"{ttime.hour}-{ttime.minute}-{ttime.second}-{ttime.day}-{ttime.month}-{ttime.year}"


def Bot(update):
    try:
        global last_use
        userid = update['message']['chat']['id']
        meseg = update['message']['text']
        msgid = update['message']['message_id']
        timee = update['message']['date']
        dl = downloader.tiktok_downloader()
        if update['message']['chat']['type'] != "private":
            SendMsg(userid, "Bot only work in private chat !", msgid)
            return
        first_name = update['message']['chat']['first_name']
        print(f"{get_time(timee)}-> {userid} - {first_name} -> {meseg}")
        if meseg.startswith('/start'):
            SendMsg(userid, "<b>Welcome to Tiktok Video Downlaoder Bot !</b>\n\n<b>How to use this bot </b>:\n<i>just send or paste url video tiktok on this bot </i>!!\n", msgid)
        elif "tiktok.com" in meseg and "https://" in meseg:
            getvid = dl.musicaldown(url=meseg, output_name="video.mp4")
            if getvid:
                SendVideo(userid, msgid)
                return
            if getvid == False:
                getvid = dl.ttscraper(url=meseg, output_name="video.mp4")
                if getvid:
                    SendVideo(userid, msgid)
                    return
                else:
                    text = "failed to download video.check link and try again"
                    SendMsg(userid, text, msgid)
                    return
                # SendMsg(
                #     userid, "<i>Failed to download video</i>\n\n<i>Try again later</i>", msgid)
                # return
                # elif getvid == "private/remove":
                #     SendMsg(
                #         userid, "<i>Failed to download video</i>\n\n<i>Video was private or removed</i>", msgid)
                # elif int(len(open('video.mp4', 'rb').read()) / 1024) > 51200:
                #     SendMsg(
                #         userid, "<i>Failed to download video</i>\n\n<i>Video size to large</i>", msgid)
                # elif getvid == 'url-invalid':
                #     SendMsg(userid, "<i>URL is invalid, send again !</i>", msgid)
                # else:
            else:
                text = "failed to download video.check link and try again"
                SendMsg(userid, text, msgid)
                return
            # os.remove('video.mp4')
        elif "/help" in meseg:
            SendMsg(userid, "How to use this bot :\njust send or paste url tiktok video on this bot !\n\n/donation - for donation bot\n/status - show status bot", msgid)
        elif meseg.startswith("/donation"):
            # SendMsg(userid, "Support me on\n\nko-fi (EN): https://ko-fi.com/fowawaztruffle\nsaweria (ID): https://saweria.co/fowawaztruffle\ntrakteerid (ID): https://trakteer.id/fowawaz\nQRIS (EWALLET,BANK): https://s.id/nusantara-qr", msgid)
            text = "EN : support this bot by subscribing to the developer channel and watching the video hehehehe. Thanks\n\nID : dග්ෆ්"
            SendMsg(userid, text, msgid)
            return
    except KeyError:
        return
