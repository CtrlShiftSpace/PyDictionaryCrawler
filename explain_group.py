from explain import Explain

class ExplainGroup:

    def __init__(self):
        self.explain_list = {}

    def add_explain(self, eid: str, epln: Explain) -> bool:
        """
        新增單字解釋
        :param eid: 單字解釋物件id
        :param epln: 單字解釋物件
        :return: True / False
        """
        # 此解釋ID已存在在dict中，無法新增
        if eid in self.explain_list:
            return False

        self.explain_list[eid] = epln
        return True

    def get_explain(self, eid: str):
        """
        取得單字解釋
        :param eid: 單字解釋物件id
        :return: Explain / False
        """
        if eid in self.explain_list:
            return self.explain_list[eid]

        return False

    def get_all_explain(self):
        return self.explain_list


