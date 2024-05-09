import requests
from bs4 import BeautifulSoup
from explain import Explain
from explain_group import ExplainGroup
from vocabulary import Vocabulary
from vocabulary_file import VocabularyFile
from urllib.parse import urlparse
import os

CAMBRIDGE_URL = "https://dictionary.cambridge.org"
CAMBRIDGE_ENDPOINT = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E"
CAMBRIDGE_MEDIA_DIR = "./cambridge"

class VocabularySearch:

    def __init__(self, mode="development"):
        # 是否執行連網查詢
        self.mode = mode
        # 字典內檔案使用
        self.vf = VocabularyFile()

    def cambridge_search(self, search_wd):
        if self.mode == "production":
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                              '537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            }
            response = requests.get(f"{CAMBRIDGE_ENDPOINT}/{search_wd}", headers=headers, timeout=15)
            text = response.content
        else:
            # 測試用
            with open("test_data/cambridge_response.html", mode="r", encoding="utf-8") as file:
                text = file.read()

        soup = BeautifulSoup(text, 'html.parser')
        page = soup.find("div", class_="page")
        blocks = page.find_all("div", class_="def-block")

        # 處理多個解釋
        epln_group = ExplainGroup()

        # 讀取到的解釋內容
        sense_dict = {block["data-wl-senseid"].strip(): block for block in blocks}
        # 單字level
        lv = None
        for senseid, sense in sense_dict.items():
            level_content = sense.find("span", class_="epp-xref")
            if lv is None and level_content is not None:
                lv = level_content.string.strip()

            # 單字解釋內容
            sense_row_content = sense.find("div", class_="ddef_d")

            # 將解析出的內容轉換成純文字字串
            content_list = sense_row_content.text.split()
            content_text = " ".join(content_list)

            # 單字圖片
            sense_img_content = sense.find_all("amp-img", class_="dimg_i")
            img_list = []
            for amp_img in sense_img_content:
                download_url = f"{CAMBRIDGE_URL}/{amp_img['src']}"
                save_dir = f"{CAMBRIDGE_MEDIA_DIR}/{senseid}"
                filename = os.path.basename(urlparse(download_url).path)
                # 實際上跑才需要撈資料
                if self.mode == "production":
                    self.vf.download(url=download_url, save_dir=save_dir, save_file_name=filename)
                    img_list.append(f"{save_dir}/{filename}")


            # 例句
            sen_content = sense.find_all("span", class_="eg")
            sen_list = [" ".join(sen.text.split()) for sen in sen_content]

            # 建立單一解釋物件
            epln = Explain(text=content_text)
            epln.sentence_list = sen_list
            epln.image_list = img_list

            # 將解釋物件儲存
            epln_group.add_explain(eid=senseid, epln=epln)

        # 查詢單字
        vc = Vocabulary(wd=search_wd, lv=lv, epln_group=epln_group)
        return vc

