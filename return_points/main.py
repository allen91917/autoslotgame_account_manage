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
        options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False
        })
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
    """處理所有會員餘額，根據廠商餘額計算調整金額"""
    try:
        print(Fore.CYAN + f"\n開始處理會員餘額，目標金額: {target_amount}" + Style.RESET_ALL)
        time.sleep(2)
        
        # 找到所有會員行(排除表頭,只找實際的資料行)
        member_rows = driver.find_elements(By.XPATH, 
            "//div[contains(@class, 'my-table-row-box')]//div[contains(@class, 'my-table-row')]")
        
        total_rows = len(member_rows)
        # 第一筆是代理,不是會員,所以會員數要-1
        total_members = total_rows - 1
        print(Fore.GREEN + f"找到 {total_members} 個會員帳號(第1筆為代理,已排除)" + Style.RESET_ALL)
        
        # 從第2筆開始處理(跳過第1筆代理)
        for index in range(2, total_rows + 1):
            try:
                # 使用更精確的 XPath 定位餘額和廠商餘額
                balance_xpath = f"(//div[contains(@class, 'my-table-row-box')]//div[contains(@class, 'my-table-row')])[{index}]//div[contains(@class, 'my-table-cell') and .//div[text()='餘額']]//button//span"
                vendor_balance_xpath = f"(//div[contains(@class, 'my-table-row-box')]//div[contains(@class, 'my-table-row')])[{index}]//div[contains(@class, 'my-table-cell') and .//div[text()='廠商餘額']]//span[1]"
                balance_button_xpath = f"(//div[contains(@class, 'my-table-row-box')]//div[contains(@class, 'my-table-row')])[{index}]//div[.//div[text()='餘額']]//button"
                
                # 顯示時要-1,因為跳過了第1筆代理
                member_number = index - 1
                print(Fore.CYAN + f"\n處理第 {member_number}/{total_members} 個會員" + Style.RESET_ALL)
                
                # 獲取餘額
                balance_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, balance_xpath))
                )
                balance_text = balance_element.text.strip().replace(',', '')
                
                # 獲取廠商餘額
                vendor_balance_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, vendor_balance_xpath))
                )
                vendor_balance_text = vendor_balance_element.text.strip().replace(',', '')
                
                # 檢查是否為空字串
                if not balance_text or not vendor_balance_text:
                    print(Fore.YELLOW + f"餘額資訊不完整，跳過" + Style.RESET_ALL)
                    continue
                
                current_balance = float(balance_text)
                vendor_balance = float(vendor_balance_text)
                
                print(Fore.YELLOW + f"餘額: {current_balance:,.2f}" + Style.RESET_ALL)
                print(Fore.YELLOW + f"廠商餘額: {vendor_balance:,.2f}" + Style.RESET_ALL)
                
                # 判斷是否在遊戲中：如果餘額為0但廠商餘額有錢
                if current_balance == 0 and vendor_balance > 0:
                    print(Fore.YELLOW + "⚠ 帳號在遊戲中（餘額為0但廠商餘額有錢），跳過調整" + Style.RESET_ALL)
                    continue
                
                # 基於餘額本身計算需要調整的金額
                adjustment = target_amount - current_balance
                
                if abs(adjustment) < 0.01:  # 容許 0.01 的誤差
                    print(Fore.GREEN + f"餘額已經接近目標金額 {target_amount}，跳過" + Style.RESET_ALL)
                    continue
                
                print(Fore.YELLOW + f"需要調整: {adjustment:+.2f}" + Style.RESET_ALL)
                
                # 點擊餘額按鈕
                balance_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, balance_button_xpath))
                )
                balance_button.click()
                print(Fore.GREEN + "已點擊餘額按鈕" + Style.RESET_ALL)
                time.sleep(2)
                
                # 判斷是增加還是減少
                if adjustment > 0:
                    # 小於目標金額，需要增加 (value="1")
                    print(Fore.CYAN + "選擇增加餘額選項" + Style.RESET_ALL)
                    add_radio = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@type="radio" and @value="1"]'))
                    )
                    driver.execute_script("arguments[0].click();", add_radio)
                    time.sleep(2)  # 增加等待時間讓輸入框準備好
                else:
                    # 大於目標金額，需要減少 (value="2")
                    print(Fore.CYAN + "選擇減少餘額選項" + Style.RESET_ALL)
                    subtract_radio = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@type="radio" and @value="2"]'))
                    )
                    driver.execute_script("arguments[0].click();", subtract_radio)
                    time.sleep(2)  # 增加等待時間讓輸入框準備好
                
                # 等待輸入框出現並變為可用
                print(Fore.CYAN + "等待輸入框準備就緒..." + Style.RESET_ALL)
                amount_input = WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH, '//input[@id="form_item_amount"]'))
                )
                # 確保輸入框可點擊
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//input[@id="form_item_amount"]'))
                )
                time.sleep(1)
                
                # 清空並輸入金額
                amount_input.click()
                time.sleep(0.5)
                amount_input.clear()
                time.sleep(1)
                amount_input.send_keys(str(abs(int(adjustment))))
                print(Fore.GREEN + f"已輸入調整金額: {abs(int(adjustment))}" + Style.RESET_ALL)
                time.sleep(2)
                
                # 點擊保存按鈕
                save_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ant-btn-primary')]//span[text()='保存']"))
                )
                save_button.click()
                print(Fore.GREEN + f"已點擊保存，餘額將更新為 {target_amount:,.2f}" + Style.RESET_ALL)
                time.sleep(2)
                
                # 等待並關閉可能出現的彈窗（包括成功提示或錯誤提示）
                try:
                    # 等待彈窗消失或關閉按鈕出現
                    time.sleep(1)
                    # 檢查是否有關閉按鈕並點擊
                    close_buttons = driver.find_elements(By.XPATH, 
                        "//button[contains(@class, 'ant-modal-close') or .//span[contains(@class, 'anticon-close')]]")
                    for close_btn in close_buttons:
                        try:
                            if close_btn.is_displayed():
                                close_btn.click()
                                time.sleep(1)
                        except:
                            pass
                    # 按 ESC 鍵關閉彈窗
                    from selenium.webdriver.common.keys import Keys
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                    time.sleep(1)
                except:
                    pass
                
                print(Fore.GREEN + f"✓ 第 {member_number} 個會員處理完成" + Style.RESET_ALL)
                
            except Exception as e:
                print(Fore.RED + f"處理第 {member_number} 個會員時發生錯誤: {e}" + Style.RESET_ALL)
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
        print("\n" + Fore.CYAN + "準備開始處理會員餘額..." + Style.RESET_ALL)
        time.sleep(3)
        
        # 處理所有會員餘額(使用檔案中的金額)
        process_member_balances(driver, target_amount=target_amount)        
        print(f"\n{'='*50}")
        print(Fore.GREEN + "所有操作完成!" + Style.RESET_ALL)
        print(f"{'='*50}\n")
        
    except Exception as e:
        print(Fore.RED + f"發生錯誤: {e}" + Style.RESET_ALL)
    finally:
        if driver:
            try:
                # 自動關閉瀏覽器
                print(Fore.YELLOW + "3秒後自動關閉瀏覽器..." + Style.RESET_ALL)
                time.sleep(3)
                print(Fore.YELLOW + "正在關閉瀏覽器..." + Style.RESET_ALL)
                driver.quit()
                print(Fore.GREEN + "瀏覽器已關閉" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"關閉瀏覽器時發生錯誤: {e}" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
