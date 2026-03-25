from playwright.sync_api import sync_playwright
import time
import tkinter as tk
from tkinter import messagebox
import winsound
import requests

# ---------------- 配置 ----------------
URL = "https://mcourses.zju.edu.cn/ongoing-rollcall-list"
KEYWORDS = ["雷达点名", "数字点名"]
REFRESH_INTERVAL = 5  # 秒
BARK_KEY = "Add your bark key here"
# --------------------------------------

def notify_user(keyword):
    """Windows弹窗 + 声音 + iPhone Bark推送"""
    print("触发提醒")

    # Windows 声音
    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

    # 顶层弹窗
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo("签到提醒", f"检测到关键字：{keyword}")
    root.destroy()

    # Bark 推送
    try:
        title = "签到提醒"
        body = f"检测到关键字：{keyword}"
        requests.get(
            f"https://api.day.app/{BARK_KEY}/{title}/{body}",
            timeout=5
        )
        print("已推送到 iPhone")
    except Exception as e:
        print("Bark 推送失败:", e)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(URL)

        input("请先登录网页，然后按回车开始监控...")

        print("开始稳定监控模式")

        notified = False

        while True:
            try:
                page.reload()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(2000)

                matched_keyword = None

                for word in KEYWORDS:
                    if page.locator(f"text={word}").count() > 0:
                        matched_keyword = word
                        break

                if matched_keyword:
                    if not notified:
                        notify_user(matched_keyword)
                        notified = True
                else:
                    notified = False

            except Exception as e:
                print("本轮检测异常，自动跳过:", e)

            time.sleep(REFRESH_INTERVAL)


if __name__ == "__main__":
    main()
