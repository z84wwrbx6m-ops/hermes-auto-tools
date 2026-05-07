"""网页数据采集核心模块"""
import httpx
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import json

class WebScraper:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout, follow_redirects=True)
    
    def fetch_text(self, url: str) -> str:
        """获取网页纯文本内容"""
        resp = self.client.get(url, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)
    
    def fetch_structured(self, url: str) -> Dict[str, Any]:
        """获取结构化数据（标题、元描述、内容）"""
        resp = self.client.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        return {
            "title": soup.title.string if soup.title else "",
            "meta_description": soup.find("meta", attrs={"name": "description"})["content"] 
                if soup.find("meta", attrs={"name": "description"}) else "",
            "text_length": len(soup.get_text(strip=True)),
        }
    
    def close(self):
        self.client.close()

__all__ = ["WebScraper"]
