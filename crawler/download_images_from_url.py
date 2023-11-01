import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import cv2
import numpy as np
import datetime

def contains_face(image_data):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 画像が正常にデコードされているか確認
    if image is None:
        print("Failed to decode the image.")
        return False

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return len(faces) > 0

def download_images_from_url(url, folder_name, limit=100):
    """
    指定されたURLから画像をダウンロードします。

    :param url: 画像を収集するウェブページのURL
    :param folder_name: 画像を保存するフォルダの名前
    :param limit: ダウンロードする画像の最大数
    """

    # フォルダを作成
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # HTMLを取得
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 画像タグを検索
    imgs = soup.find_all('img')
    
    downloaded = 0
    for img in imgs:
        img_url = img['src']
        # 相対URLを絶対URLに変換
        img_url = urljoin(url, img_url)

         # 元のファイル名を取得
        original_filename = img_url.split('/')[-1].split('?')[0]  # URLの最後の部分を取得して、クエリパラメータを除外

        # 現在の日時を取得
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y%m%d%H%M%S')

        # 保存する画像名を作成
        save_filename = f"{timestamp}_{original_filename}"

        # URLから画像を取得
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            image_data = response.content
            # 画像に顔が含まれているか確認
            if contains_face(image_data):
                with open(os.path.join(folder_name, save_filename), 'wb') as f:
                    f.write(image_data)
                downloaded += 1
                if downloaded >= limit:
                    break

    print(f"{downloaded} images downloaded!")

if __name__ == "__main__":
    target_url = "https://www.shinchosha.co.jp/special/kakiharuka1st/"
    #target_url = "https://www.google.com/search?q=%E4%B9%83%E6%9C%A8%E5%9D%82&sca_esv=578407962&rlz=1C5CHFA_enJP959JP960&tbm=isch&sxsrf=AM9HkKm5GnfX78nsRDxDBdCoE9Duh-BV6Q:1698829934012&source=lnms&sa=X&ved=2ahUKEwiCnIDWuqKCAxWVa_UHHULuDKEQ0pQJegQIAhAI&biw=1114&bih=802&dpr=1.6"
    #target_url = "https://sp.nogizaka46.com/p/members"  # 画像を収集したいウェブページのURLを指定
    download_images_from_url(target_url, "downloaded_images")
