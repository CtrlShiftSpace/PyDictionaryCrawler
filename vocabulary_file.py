import requests
import os

class VocabularyFile:

    def __init__(self):
        pass

    def download(self, url, save_dir, save_file_name):
        if not os.path.exists(path=save_dir):
            # 目錄不存在時建立
            os.mkdir(save_dir, 0o0755)
        # 撈取url的圖片
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                          '537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        # 本地儲存的檔案路徑
        filepath = f"{save_dir}/{save_file_name}"
        with open(filepath, 'wb') as handle:
            handle.write(response.content)