import cv2
import os

def detect_and_save_faces(input_path, output_path):
    # OpenCVのカスケード分類器を初期化
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 画像を読み込む
    image = cv2.imread(input_path)

    # 画像をグレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 顔を検出
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for idx, (x, y, w, h) in enumerate(faces):
        # 顔部分を切り出す
        face_image = image[y:y+h, x:x+w]

        # 元の画像名を取得
        base_name = os.path.basename(input_path)
        file_name_without_extension = os.path.splitext(base_name)[0]

        # 顔画像の名前を決定
        save_name = f"{file_name_without_extension}_face_{idx}.jpg"
        
        # 顔画像を保存
        save_path = os.path.join(output_path, save_name)
        cv2.imwrite(save_path, face_image)

def process_all_images_in_folder(input_directory, output_directory):
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # ディレクトリ内のすべての画像ファイルを処理
    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(input_directory, filename)
            detect_and_save_faces(file_path, output_directory)

if __name__ == "__main__":
    input_dir = 'downloaded_images'  # 画像を含む入力ディレクトリへのパス
    output_dir = 'face_images' # 顔の画像を保存する出力ディレクトリへのパス
    process_all_images_in_folder(input_dir, output_dir)
