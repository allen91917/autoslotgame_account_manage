import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore, Style
from datetime import datetime
import subprocess
import logging
from webdriver_manager.chrome import ChromeDriverManager


def load_user_info():
    """從用戶資訊.txt讀取帳號、密碼和金額"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, '用戶資訊.txt')
        
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                # 跳過空行和註解行
                if not line or line.startswith('#'):
                    continue
                
                # 解析格式：帳號,密碼,金額
                parts = line.split(',')
                if len(parts) == 3:
                    account = parts[0].strip()
                    password = parts[1].strip()
                    amount = int(parts[2].strip())
                    print(Fore.GREEN + f"讀取成功 - 帳號: {account}, 金額: {amount}" + Style.RESET_ALL)
                    return account, password, amount
        
        print(Fore.RED + "未找到有效的用戶資訊" + Style.RESET_ALL)
        return None, None, None
        
    except FileNotFoundError:
        print(Fore.RED + "找不到 用戶資訊.txt 檔案" + Style.RESET_ALL)
        return None, None, None
    except Exception as e:
        print(Fore.RED + f"讀取用戶資訊時發生錯誤: {e}" + Style.RESET_ALL)
        return None, None, None


def init_environment():
    """初始化環境設定"""
    logging.basicConfig(level=logging.ERROR)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    sys.stdout.reconfigure(encoding='utf-8')
    
    try:
        result = subprocess.run(["chromedriver", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout:
            version = result.stdout.split()[1]
            print(f"ChromeDriver {version}")
        else:
            print("ChromeDriver 將自動下載安裝")
    except (FileNotFoundError, Exception) as e:
        print("ChromeDriver 未安裝，將使用 webdriver-manager 自動下載")

    init(autoreset=True)


def init_driver():
    """使用 ChromeDriverManager 初始化 Chrome WebDriver"""
    try:
        print("\n正在初始化 Chrome 瀏覽器...")
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--log-level=3')
        options.add_argument('--disable-gpu')
        options.add_argument('--mute-audio')
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })
        print("Chrome 瀏覽器初始化成功！\n")
        return driver
    except Exception as e:
        print(f"\033[31m錯誤：無法啟動 Chrome 瀏覽器：{e}\033[0m")
        print("\033[33m請確保已安裝 Google Chrome 瀏覽器\033[0m")
        print("\033[33m下載地址：https://www.google.com/chrome/\033[0m")
        input("\n按 Enter 結束...")
        sys.exit(1)


def login_to_system(driver, username_text, password_text):
    """登入系統"""
    print(Fore.CYAN + "正在導航到登入頁面..." + Style.RESET_ALL)
    
    # 導航到 https://admin.fin88.app
    driver.get("https://admin.fin88.app")
    driver.maximize_window()
    time.sleep(2)

    print(Fore.CYAN + "正在輸入帳號..." + Style.RESET_ALL)
    # 帳號 XPath: //input[@id="form_item_account"]
    username = WebDriverWait(driver, 180).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="form_item_account"]'))
    )
    username.click()
    time.sleep(0.5)
    username.clear()
    username.send_keys(username_text)

    print(Fore.CYAN + "正在輸入密碼..." + Style.RESET_ALL)
    # 密碼 XPath: //input[@id="form_item_password"]
    password = WebDriverWait(driver, 180).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="form_item_password"]'))
    )
    password.click()
    time.sleep(0.5)
    password.clear()
    password.send_keys(password_text)

    print(Fore.CYAN + "正在點擊登入按鈕..." + Style.RESET_ALL)
    # 登入 XPath: //button/span[text()='登 錄']/parent::button
    login = WebDriverWait(driver, 180).until(
        EC.element_to_be_clickable((By.XPATH, "//button/span[text()='登 錄']/parent::button"))
    )
    login.click()

    print(Fore.GREEN + "登入中，請稍候...\n" + Style.RESET_ALL)
    time.sleep(5)

    # 關閉公告彈窗
    try:
        print(Fore.CYAN + "檢查是否有公告彈窗..." + Style.RESET_ALL)
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='確 認']]"))
        )
        close_button.click()
        print(Fore.GREEN + "已關閉公告彈窗" + Style.RESET_ALL)
        time.sleep(1)
    except:
        print(Fore.YELLOW + "未發現公告彈窗或已關閉" + Style.RESET_ALL)

    try:
        current_url = driver.current_url
        print(Fore.GREEN + f"當前頁面: {current_url}" + Style.RESET_ALL)
        print(Fore.GREEN + "登入成功！" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"瀏覽器連接已斷開: {e}" + Style.RESET_ALL)
        raise


def navigate_to_member_management(driver):
    """導航到會員管理頁面"""
    try:
        print(Fore.CYAN + "正在點擊「下線代理管理」..." + Style.RESET_ALL)
        
        # 點擊「下線代理管理」
        agent_management = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'vben-simple-menu-sub-title') and text()='下線代理管理']"))
        )
        agent_management.click()
        print(Fore.GREEN + "已點擊「下線代理管理」" + Style.RESET_ALL)
        time.sleep(2)
        
        print(Fore.CYAN + "正在點擊「會員管理」..." + Style.RESET_ALL)
        
        # 點擊「會員管理」單選按鈕
        member_management = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(@class, 'ant-radio-button-wrapper')]//span[text()='會員管理']"))
        )
        member_management.click()
        print(Fore.GREEN + "已點擊「會員管理」" + Style.RESET_ALL)
        time.sleep(2)
        
        print(Fore.GREEN + "成功進入會員管理頁面！" + Style.RESET_ALL)
        
    except Exception as e:
        print(Fore.RED + f"導航到會員管理失敗: {e}" + Style.RESET_ALL)
        raise


def process_member_balances(driver, target_amount=5000):
    """處理所有會員餘額，將每個會員餘額設定為目標金額"""
    try:
        print(Fore.CYAN + f"\n開始處理會員餘額，目標金額: {target_amount}" + Style.RESET_ALL)
        time.sleep(2)
        
        # 找到所有餘額按鈕
        balance_buttons = driver.find_elements(By.XPATH, 
            "//button[contains(@class, 'ant-btn-link') and contains(@class, 'block')]//span")
        
        total_members = len(balance_buttons)
        print(Fore.GREEN + f"找到 {total_members} 個會員帳號" + Style.RESET_ALL)
        
        for index, button in enumerate(balance_buttons, 1):
            try:
                # 獲取當前餘額
                current_balance = button.text.strip()
                print(Fore.CYAN + f"\n處理第 {index}/{total_members} 個會員" + Style.RESET_ALL)
                print(Fore.YELLOW + f"當前餘額: {current_balance}" + Style.RESET_ALL)
                
                # 點擊餘額按鈕
                button.click()
                print(Fore.GREEN + "已點擊餘額按鈕" + Style.RESET_ALL)
                time.sleep(2)
                
                # 找到輸入框並輸入金額
                amount_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//input[@id="form_item_amount"]'))
                )
                amount_input.clear()
                time.sleep(1)
                amount_input.send_keys(str(target_amount))
                print(Fore.GREEN + f"已輸入金額: {target_amount}" + Style.RESET_ALL)
                time.sleep(2)
                
                # 點擊保存按鈕
                save_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ant-btn-primary')]//span[text()='保存']"))
                )
                save_button.click()
                print(Fore.GREEN + f"已點擊保存，餘額已更新為 {target_amount}" + Style.RESET_ALL)
                time.sleep(2)
                
                # 重新獲取所有按鈕（因為頁面可能已更新）
                balance_buttons = driver.find_elements(By.XPATH, 
                    "//button[contains(@class, 'ant-btn-link') and contains(@class, 'block')]//span")
                
            except Exception as e:
                print(Fore.RED + f"處理第 {index} 個會員時發生錯誤: {e}" + Style.RESET_ALL)
                continue
        
        print(Fore.GREEN + f"\n所有會員餘額處理完成！" + Style.RESET_ALL)
        
    except Exception as e:
        print(Fore.RED + f"處理會員餘額時發生錯誤: {e}" + Style.RESET_ALL)
        raise


def main():
    """主程式入口"""
    init_environment()
    
    # 從檔案讀取帳號資料
    print(Fore.CYAN + "正在讀取用戶資訊..." + Style.RESET_ALL)
    username, password, target_amount = load_user_info()
    
    if not username or not password or not target_amount:
        print(Fore.RED + "無法讀取用戶資訊，程式結束" + Style.RESET_ALL)
        input("\n按 Enter 結束...")
        return
    
    driver = None
    try:
        print(f"\n{'='*50}")
        print(Fore.YELLOW + f"開始登入系統" + Style.RESET_ALL)
        print(f"{'='*50}\n")
        
        # 初始化瀏覽器
        driver = init_driver()
        
        # 登入系統
        login_to_system(driver, username, password)
        
        # 導航到會員管理
        navigate_to_member_management(driver)
        time.sleep(2)
        
        # 處理所有會員餘額（使用檔案中的金額）
        process_member_balances(driver, target_amount=target_amount)        
        print(f"\n{'='*50}")
        print(Fore.GREEN + "所有操作完成！" + Style.RESET_ALL)
        print(f"{'='*50}\n")
        
        input("\n按 Enter 關閉瀏覽器...")
        
    except Exception as e:
        print(Fore.RED + f"發生錯誤: {e}" + Style.RESET_ALL)
    finally:
        if driver:
            try:
                print("\033[1;33m正在關閉瀏覽器...\033[0m")
                driver.quit()
                print(Fore.GREEN + "瀏覽器已關閉" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"關閉瀏覽器時發生錯誤: {e}" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
