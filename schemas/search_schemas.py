"""搜索相关的Schema定义"""
from pydantic import BaseModel, model_validator
from typing import List

from crawler.payloads import (
    CampusID,
    MatchMode,
    Oper,
    SearchField,
)


class SearchItemModel(BaseModel):
    """搜索项模型"""
    oper: Oper | None
    searchField: SearchField
    matchMode: MatchMode
    searchFieldContent: str


class SemanticFrameModel(BaseModel):
    """语义框架模型"""
    campusId: List[CampusID | None]
    searchItems: List[SearchItemModel]

    @model_validator(mode="after")
    def check_rule(self):
        if not self.searchItems:
            raise ValueError("searchItems 不能为空")

        if self.searchItems[0].oper is not None:
            raise ValueError("第一个 oper 必须为 None")

        for i in range(1, len(self.searchItems)):
            if self.searchItems[i].oper is None:
                raise ValueError(f"第{i}个 oper 不能为 None")

        for i, item in enumerate(self.searchItems):
            if self.searchItems[i].searchFieldContent is None or self.searchItems[i].searchFieldContent.strip() == "":
                raise ValueError(f"第{i}个 searchFieldContent 不能为空")

        return self
