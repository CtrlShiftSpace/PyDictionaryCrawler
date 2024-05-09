import pandas
from vocabulary_search import VocabularySearch
import json
from tkinter import *

# 查詢並更新未記錄過資料
def search_update_word(search_wd):
    try:
        # 讀取JSON檔
        with open("data.json", mode="r") as data:
            json_data = json.load(data)
    except FileNotFoundError:
        json_data = {}

    # 如果是未查過的單字
    if search_wd not in json_data:
        vs = VocabularySearch()
        # 執行 cambridge 查詢
        vc = vs.cambridge_search(search_wd=search_wd)

        # 更新查詢結果的dict
        json_data[vc.word] = vc.get_data()
        with open("data.json", mode="w") as file:
            json.dump(json_data, file, indent=4)

    return json_data


################ TKinter UI ################

def search_btn_click():
    wd = search_entry.get()

    json_data = search_update_word(search_wd=wd)
    result_label.config(text=json_data)


window = Tk()
window.title("字典查詢工具")
window.config(padx=40, pady=40)

dictionary_label = Label(text="英文字典查詢", font=("Arial", 30, "bold"))
dictionary_label.grid(row=0, column=0, columnspan=2)

search_entry = Entry(width=30)
search_entry.grid(row=1, column=0, pady=10)

search_button = Button(text="查詢", width=10, command=search_btn_click)
search_button.grid(row=1, column=1, pady=10)

result_label = Label(text="test", width=40, height=20, bg="azure", anchor="nw", wraplength=250)
result_label.grid(row=2, column=0, columnspan=2, pady=10)



window.mainloop()




# 要查詢的英文單字
# wd = "will"
# search_update_word(search_wd=wd)