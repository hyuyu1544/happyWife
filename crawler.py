
import time
import requests
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


TARGET_URL = "https://tradead.tixplus.jp/wbc2026"

KEYWORDS = ["台湾", "チャイニーズ・タイペイ", "TPE", "Chinese Taipei"]

def check_tickets():
    target_url = "https://tradead.tixplus.jp/wbc2026"
    print(f"🔍 開始檢查: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    found_matches = []

    with sync_playwright() as p:
  
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

        try:
            page.goto(TARGET_URL, timeout=60000)
            
            try:
                page.wait_for_selector("#app", timeout=20000)
            except:
                print("⚠️ 網頁載入超時或結構改變")

            
            content = page.content()
            soup = BeautifulSoup(content, "html.parser")
            app_div = soup.find("div", id="app")
            if not app_div:
                print("⚠️ 找不到 id='app'，網站結構可能改變")
                return
            data_page_str = app_div.get("data-page")
            if not data_page_str:
                print("⚠️ 找不到 data-page 屬性")
                return
            
            data = json.loads(data_page_str)
            
        
            concerts = data.get("props", {}).get("concerts", [])
            
            print(f"📊 讀取到 {len(concerts)} 場比賽資料")


            for match in concerts:
                
                match_name = match.get("name", "未知名稱")
                match_date = match.get("concert_date_web_format", "日期未知") 
                listings_count = match.get("listings_count", 0) 
                
                
                is_taiwan_game = any(k in match_name for k in KEYWORDS)
                
                if is_taiwan_game:
                    print(f"🇹🇼 發現台灣賽事: {match_name} (目前票數: {listings_count})")
                    if listings_count > 0:
                        found_matches.append(f"{match_date} | {match_name} (剩餘: {listings_count}張)")
            
            return found_matches

        except Exception as e:
            print(f"❌ 發生錯誤: {e}")
        finally:
            browser.close()