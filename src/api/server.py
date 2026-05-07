"""FastAPI 服务入口 - 带 API 密钥认证"""
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.scraper import WebScraper
import os
import hmac

app = FastAPI(title="Hermes Auto Tools API", version="0.2.0")

# CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

scraper = WebScraper()

# API 密钥（从环境变量读取，默认开发模式）
API_KEY = os.environ.get("HERMES_API_KEY", "dev-key-123")

def verify_key(x_api_key: str = Header(None)):
    """简单的 API 密钥验证"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="缺少 API 密钥")
    if not hmac.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=403, detail="API 密钥无效")
    return x_api_key

@app.get("/")
def root():
    return {"status": "ok", "service": "Hermes Auto Tools", "version": "0.2.0"}

@app.get("/scrape")
def scrape(url: str, api_key: str = Depends(verify_key)):
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="无效URL")
    try:
        text = scraper.fetch_text(url)
        return {"url": url, "text_length": len(text), "content": text[:5000]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scrape/structured")
def scrape_structured(url: str, api_key: str = Depends(verify_key)):
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="无效URL")
    try:
        data = scraper.fetch_structured(url)
        return {"url": url, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy", "service": "hermes-auto-tools"}

@app.on_event("shutdown")
def shutdown():
    scraper.close()
