from pydantic import BaseModal

class SearchResultItem(BaseModal):
    # 搜索结果条目数据类型
    url: str
    title: str
    snippet: str


class SearchResults(BaseModal):
    # 搜索结果数据类型
    query: str
    data_range: str
    total_results: int
    results: list[SearchResultItem]