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

def has_same_filename(filepath):
    """指定されたパスにファイルが存在するかどうかをチェックする"""
    return os.path.exists(filepath)

def create_unique_filename(folder_name, original_filename, timestamp):
    """ユニークなファイル名を生成する"""
    counter = 1
    while True:
        if counter > 1:
            # カウンターが1より大きい場合、ファイル名にカウンターを追加する
            save_filename = f"{timestamp}_{counter}_{original_filename}"
        else:
            # 最初はカウンターを追加しない
            save_filename = f"{timestamp}_{original_filename}"

        # ファイル名が重複していないかチェック
        if not has_same_filename(os.path.join(folder_name, save_filename)):
            return save_filename

        # ファイル名が重複している場合、カウンターを増やしてループを続ける
        counter += 1

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
    counter = 1
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
        save_filename = create_unique_filename(folder_name, original_filename, timestamp)

        # URLから画像を取得
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            image_data = response.content
            # 画像に顔が含まれているか確認
            if contains_face(image_data):
                with open(os.path.join(folder_name, save_filename), 'wb') as f:
                    f.write(image_data)
                    print(save_filename)
                downloaded += 1
                if downloaded >= limit:
                    break
            else:
                print("No face detected.")

    print(f"{downloaded} images downloaded!")

if __name__ == "__main__":
    #target_url = "https://www.shinchosha.co.jp/special/kakiharuka1st/"
    #target_url = "https://www.google.com/search?q=%E4%B9%83%E6%9C%A8%E5%9D%82&sca_esv=578407962&rlz=1C5CHFA_enJP959JP960&tbm=isch&sxsrf=AM9HkKm5GnfX78nsRDxDBdCoE9Duh-BV6Q:1698829934012&source=lnms&sa=X&ved=2ahUKEwiCnIDWuqKCAxWVa_UHHULuDKEQ0pQJegQIAhAI&biw=1114&bih=802&dpr=1.6"
    #target_url = "https://sp.nogizaka46.com/p/members"  # 画像を収集したいウェブページのURLを指定
    target_url = "https://sakurazaka46.com/s/s46/search/artist?ima=0000&link=ROBO004"
    download_images_from_url(target_url, "downloaded_images")
