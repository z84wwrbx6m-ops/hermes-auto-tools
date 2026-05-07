"""FastAPI 服务入口"""
from fastapi import FastAPI, HTTPException
from src.scraper import WebScraper

app = FastAPI(title="Hermes Auto Tools API", version="0.1.0")
scraper = WebScraper()

@app.get("/")
def root():
    return {"status": "ok", "service": "Hermes Auto Tools"}

@app.get("/scrape")
def scrape(url: str):
    """采集指定URL的文本内容"""
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="无效URL")
    try:
        text = scraper.fetch_text(url)
        return {"url": url, "text_length": len(text), "content": text[:5000]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scrape/structured")
def scrape_structured(url: str):
    """获取结构化数据"""
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="无效URL")
    try:
        data = scraper.fetch_structured(url)
        return {"url": url, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
def shutdown():
    scraper.close()
