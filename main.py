import requests
import re
import os
from datetime import datetime
import schedule
import time

def clean_text(text):
    """HTMLタグやその他不要な文字列を除去する"""
    if text:
        cleaned_text = re.sub(r'<.*?>', '', text)
        return cleaned_text
    return text

def extract_name_message(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        now = datetime.now()
        file_name = now.strftime("%Y-%m-%d_%H-%M-%S.txt")
        directory = "bbs"
        file_path = os.path.join(directory, file_name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        lines = []

        if 'contents' in data:
            for item in data['contents']:
                name = item.get('name')
                message = item.get('message')

                cleaned_name = clean_text(name)
                cleaned_message = clean_text(message)

                new_content = f"Name: {cleaned_name}\nMessage: {cleaned_message}\n\n"
                lines.append(new_content)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
        print(f"{file_name}に保存しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

def job():
    url = "https://yukibbs-server.onrender.com/dev/bbs/api?start=100"
    extract_name_message(url)

# 10分ごとにjob関数を実行するようスケジュール
schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
