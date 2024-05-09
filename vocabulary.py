from explain_group import ExplainGroup

class Vocabulary:

    def __init__(self, wd: str, lv: str, epln_group: ExplainGroup):
        """
        建立單字類別
        :param wd: 單字
        """
        self.word = wd
        self.level = lv
        self.epln_group = epln_group

    def get_data(self) -> dict:
        """
        取得單字的資料
        :return: dict
        """
        explains = []
        for eid, epln in self.epln_group.get_all_explain().items():
            explains.append({
                "eid": eid,
                "text": epln.text,
                "image_list": epln.image_list,
                "sentence_list": epln.sentence_list,
            })

        data_dict = {
            "word": self.word,
            "level": self.level,
            "explains": explains
        }

        return data_dict



