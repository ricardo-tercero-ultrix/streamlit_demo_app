from typing import (
    Optional,
)
from patents import PatentsHandler
from constants import PATENT_FILE_NAME
from utils import get_website_content
from langchain_utils import summarize_website

def summarize_patent(patent_id: str, handler: Optional[PatentsHandler] = None) -> Optional[str]:
    if handler is None:
        handler = PatentsHandler(PATENT_FILE_NAME)
    url = handler.get_patent_website(patent_id)
    if url is not None:
        # content = get_website_content(url)
        return summarize_website(url=url)
    return None
