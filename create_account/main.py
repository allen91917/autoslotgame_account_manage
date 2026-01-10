import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ============FIN網址================
URL = "https://admin.fin88.app"
# ============TG網址================
# URL = "https://admin.tg5688.com"


# ============================
# 建立 Chrome Driver（使用 ChromeDriverManager）
# ============================
def create_driver():
    """建立 Selenium ChromeDriver（使用 ChromeDriverManager 自動管理）"""

    print("使用 ChromeDriverManager 自動下載並管理 chromedriver...")
    driver_path = ChromeDriverManager().install()

    # ============================
    # Chrome Options
    # ============================
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-save-password-bubble")

    # 關閉 Chrome 密碼儲存提示
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # 設定視窗大小
    chrome_options.add_argument("--window-size=1280,800")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # ============================
    # 最強 anti-detection
    # ============================
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            """
        },
    )

    return driver


# ============================
#  暱稱產生
# ============================

def generate_random_name():
    """隨機生成暱稱：可能單姓 or 雙姓 + 兩字名字"""

    # 單姓
    single_last_names = [
        "陳","林","黃","張","李","王","吳","劉","蔡","楊","許","鄭","謝","洪","郭",
        "邱","曾","廖","賴","徐","周","葉","蘇","莊","呂","江","何","蕭","羅","高",
        "潘","簡","朱","鍾","彭","游","翁","戴","范","宋","余","程","連","唐","馬",
        "董","石"
    ]

    # 新增：雙姓
    double_last_names = [
        "歐陽", "司馬", "諸葛", "上官", "司徒", "夏侯", "張簡", "范姜", "南宮", "西門",
        "東方", "皇甫", "慕容", "長孫", "宇文", "司空", "公孫", "令狐"
    ]

    # 讓雙姓比率稍微低一點（自然一點）
    if random.random() < 0.1:  # 10% 使用雙姓
        last_name = random.choice(double_last_names)
    else:
        last_name = random.choice(single_last_names)

    # 名字第一字
    first_char_list = [
        "家","冠","孟","志","承","柏","俊","冠","子","宇","怡","雅","淑","珮","品","欣",
        "嘉","彥","佳","宗","昇","美","詩","柔","芷","心","宥","睿","建","哲","廷","瑜",
        "郁","婉","雨","馨","明","偉","宏","諾","安","雲","語"
    ]
    
    # 名字第二字
    second_char_list = [
        "瑋","宇","軒","豪","翰","翰","宏","霖","傑","翔","叡","君","婷","芬","琪","萱",
        "婷","雯","萱","怡","蓉","慧","涵","婷","玲","琳","筑","芊","瑜","妤","平","晴",
        "哲","豪","明","偉","哲","成","達","潔","嫻","安","菲","菁"
    ]

    # 兩字名字組合
    name = last_name + random.choice(first_char_list) + random.choice(second_char_list)
    return name



# ============================
#  ⭐ 新增：帳號紀錄 TXT
# ============================

def init_agent_txt(agent_account, agent_password, txt_path):
    """第一次登入代理就建立 TXT 並寫入代理帳密（含中文標題）"""
    if not os.path.exists(txt_path):
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("代理帳號,代理密碼\n")
            f.write(f"{agent_account},{agent_password}\n")
            f.write("遊戲帳號,遊戲密碼\n")   # 先寫標題，內容等最後 append


def append_random_account(created_account, txt_path):
    """封控後把隨機生成的遊戲帳號寫入 TXT"""
    with open(txt_path, "a", encoding="utf-8") as f:
        f.write(f"{created_account['account']},{created_account['password']}\n")


# ============================
#  登入代理帳號
# ============================

def login(driver):
    """讓使用者輸入帳號密碼後，自動登入，並導向個人頁面"""

    # === 1️⃣ 使用者輸入帳密 ===
    account = input("請輸入帳號：").strip()
    password = input("請輸入密碼：").strip()

    print(f"已儲存帳號密碼，準備登入...")

    # === 2️⃣ 定位 XPath ===
    account_xpath = "//input[@id='form_item_account']"
    password_xpath = "//input[@id='form_item_password']"
    login_button_xpath = "//button/span[text()='登 錄']/parent::button"

    try:
        # === 3️⃣ 輸入帳號 ===
        acc_el = driver.find_element("xpath", account_xpath)
        acc_el.clear()
        acc_el.send_keys(account)
        print("已輸入帳號")

        # === 4️⃣ 輸入密碼 ===
        pwd_el = driver.find_element("xpath", password_xpath)
        pwd_el.clear()
        pwd_el.send_keys(password)
        print("已輸入密碼")

        print("帳密輸入完成")

        # === 5️⃣ 點擊登入按鈕 ===
        login_btn = driver.find_element("xpath", login_button_xpath)
        login_btn.click()

        # 等待跳轉完成
        time.sleep(8)

        # # ⭐ 不再點擊返回首頁,直接導向個人頁面
        # target_url = "https://admin.fin88.app/#/dashboard/workbench"
        # # print(f"導向個人頁面:{target_url}")
        # driver.get(target_url)

        # # 等待頁面載入
        # time.sleep(2)

        # 關閉公告彈窗
        try:
            # print("檢查是否有公告彈窗...")
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='確 認']]"))
            )
            close_button.click()
            # print("已關閉公告彈窗")
            time.sleep(1)
        except:
            print("未發現公告彈窗或已關閉")

    except Exception as e:
        print(" 登入時發生錯誤:", e)

    # 回傳登入帳密（寫 txt 用）
    return account, password



# ============================
#  代理控制 → 進入創帳號畫面
# ============================

def agent_control(driver):
    """登入完成後，依照順序點擊 代理控制 相關按鈕"""

    wait = WebDriverWait(driver, 20)

    time.sleep(3)  # 等待頁面加載

    try:
        # === 1️⃣ 點擊「agent_button」(下線代理管理) ===
        # print("尋找下線代理管理按鈕...")
        agent_button_xpath = "//li[contains(@class, 'vben-menu-item')]//span[text()='下線代理管理']"
        
        # 先確認元素存在
        agent_btn = wait.until(EC.presence_of_element_located((By.XPATH, agent_button_xpath)))
        
        # 滾動到元素位置
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", agent_btn)
        time.sleep(1)
        
        # 等待可點擊並點擊
        agent_btn = wait.until(EC.element_to_be_clickable((By.XPATH, agent_button_xpath)))
        agent_btn.click()
        # print("已點擊 agent_button")
        time.sleep(6)  # 等待頁面加載

        # === 2️⃣ 點擊「direct_member」(會員管理) ===
        # print("尋找會員管理按鈕...")
        direct_member_xpath = "//label[contains(@class, 'ant-radio-button-wrapper')]//span[text()='會員管理']"
        
        dm_btn = wait.until(EC.presence_of_element_located((By.XPATH, direct_member_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", dm_btn)
        time.sleep(1)
        
        dm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, direct_member_xpath)))
        dm_btn.click()
        # print("已點擊 direct_member")
        time.sleep(3)  # 等待頁面加載

        # === 3️⃣ 點擊「create_button」(新建會員) ===
        # print("尋找新建會員按鈕...")
        create_button_xpath = "//button[contains(@class, 'ant-btn-primary')]//span[text()='新建會員']"
        
        create_btn = wait.until(EC.presence_of_element_located((By.XPATH, create_button_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", create_btn)
        time.sleep(1)
        
        create_btn = wait.until(EC.element_to_be_clickable((By.XPATH, create_button_xpath)))
        create_btn.click()
        # print("已點擊 create_button")
        time.sleep(3)  # 等待頁面加載

    except Exception as e:
        print("agent_control 發生錯誤：", e)
        print(" 提示：請確認是否已成功登入並停留在正確頁面")


# ============================
#  ✅ 這裡是你原本的 create_account（含下滑）
# ============================

def create_account(driver):
    """
    創建會員帳號流程（不使用 safe_click）
    1. 下滑到隨機按鈕
    2. 點擊隨機
    3. 讀取帳號
    4. 填寫密碼（aaaa1111）
    """

    wait = WebDriverWait(driver, 10)

    random_btn_xpath = "//button[contains(@class, 'ant-btn-primary')]//span[text()='自動生成']/parent::button"
    account_input_xpath = "//input[@id='form_item_accountNo']"
    next1_button_xpath = "//button[contains(@class, 'ant-btn-primary')]//span[text()='下一步']/parent::button"

    # ⭐ 新增：密碼欄位 XPath
    password_input_xpath = "//input[@id='form_item_pwd']"
    comfirm_password_input_xpath = "//input[@id='form_item_pwd2']"

    # ⭐ 固定密碼
    default_password = "aaaa1111"

    # === 2️⃣ 點擊隨機按鈕 ===
    random_btn = wait.until(EC.element_to_be_clickable((By.XPATH, random_btn_xpath)))
    random_btn.click()
    print("已點擊自動生成按鈕，等待帳號生成...")
    time.sleep(5)  # 等待系統生成帳號

    # === 3️⃣ 從頁面 HTML 提取帳號 ===
    account_value = None
    print("正在讀取帳號...")
    
    for attempt in range(10):
        try:
            import re
            page_source = driver.page_source
            
            # 用正則表達式從 HTML 中提取帳號
            match = re.search(r'id="form_item_accountNo"[^>]*value="([^"]+)"', page_source)
            
            if match and match.group(1):
                account_value = match.group(1)
                # print(f"成功讀取帳號：{account_value}")
                break
            else:
                # print(f"第 {attempt + 1} 次嘗試，帳號尚未生成...")
                time.sleep(1)
                
        except Exception as e:
            # print(f"第 {attempt + 1} 次讀取失敗：{e}")
            time.sleep(1)
    
    if not account_value:
        print(" 無法讀取帳號")
        account_value = "ERROR_NO_ACCOUNT"

    # === 4️⃣ 填入密碼 ===
    password_input = wait.until(
        EC.presence_of_element_located((By.XPATH, password_input_xpath))
    )
    password_input.clear()
    password_input.send_keys(default_password)
    # print(f"已輸入密碼：{default_password}")

    comfirm_password_input = wait.until(
        EC.presence_of_element_located((By.XPATH, comfirm_password_input_xpath))
    )
    comfirm_password_input.clear()
    comfirm_password_input.send_keys(default_password)
    # print(f"已輸入確認密碼：{default_password}")

    # === 5️⃣ 填入暱稱 ===
    nickname_xpath = "//input[@id='form_item_nickName']"

    nickname_input = wait.until(
        EC.presence_of_element_located((By.XPATH, nickname_xpath))
    )

    nickname = generate_random_name()
    nickname_input.clear()
    nickname_input.send_keys(nickname)

    # print(f"已輸入暱稱：{nickname}")
    time.sleep(1)
    
    # === 6️⃣ 點擊下一步 === 
    next1_button = wait.until(EC.element_to_be_clickable((By.XPATH, next1_button_xpath)))
    next1_button.click()
    time.sleep(3)  # 等待下一頁加載

    # 若要回傳整組資訊，可以這樣：
    return {
        "account": account_value,
        "password": default_password
    }


# ============================
#  設定額度
# ============================

def set_credit_limit(driver):
    """
    設定額度為固定 5000，並按下下一步
    """

    wait = WebDriverWait(driver, 10)

    credit_input_xpath = "//input[@id='form_item_remain']"
    next_button_xpath = "//button[contains(@class, 'ant-btn-primary')]//span[text()='下一步']/parent::button"

    limit_value = "5000"  # 固定額度

    # print("開始設定額度為 5000 ...")

    # === 1️⃣ 找到額度輸入框 ===
    credit_input = wait.until(
        EC.presence_of_element_located((By.XPATH, credit_input_xpath))
    )

    # 讓畫面自動捲到額度欄位
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", credit_input)
    time.sleep(0.5)

    # === 2️⃣ 輸入額度 ===
    credit_input.clear()
    credit_input.send_keys(limit_value)
    # print(f"已輸入額度：{limit_value}")

    time.sleep(0.3)

    # === 3️⃣ 按下下一步 ===
    next_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, next_button_xpath))
    )
    next_button.click()

    print("已按下下一步（Next）")
    time.sleep(3)  # 等待下一頁加載


# ============================
#  manufacturers
# ============================

def manufacturers(driver):
    """
    按下一步 → 下滑到確認按鈕 → 按確認
    每次動作 sleep 2 秒
    """

    wait = WebDriverWait(driver, 10)

    next_btn_xpath = "//button[contains(@class, 'ant-btn-primary')]//span[text()='下一步']/parent::button"

    # print("進入廠商階段")

    # === 1️⃣ 按 下一步 ===
    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, next_btn_xpath)))
    next_btn.click()
    # print("已按下『下一步』")
    time.sleep(2)


def hold_position(driver):
    """
    按下一步 → 下滑到確認按鈕 → 按確認
    每次動作 sleep 2 秒
    """

    wait = WebDriverWait(driver, 10)

    next_btn_xpath = "//button[contains(@class, 'ant-btn-primary')]//span[text()='下一步']/parent::button"

    # print("進入退水設定")

    # === 1️⃣ 找到下一步按鈕並下滑 ===
    next_btn = wait.until(EC.presence_of_element_located((By.XPATH, next_btn_xpath)))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_btn)
    time.sleep(1)

    # === 2️⃣ 等待按鈕可點擊後點擊 ===
    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, next_btn_xpath)))
    next_btn.click()
    # print("已按下『下一步』")
    time.sleep(2)
# ============================
#  限紅設定
# ============================

def Table_limit(driver):
    """
    限紅設定流程
    1. 點擊限紅下拉選單並選擇第一個選項
    2. 輸入封頂數值為 0
    3. 點擊下一步
    """

    wait = WebDriverWait(driver, 10)

    # 使用 id 定位下拉選單
    table_limit_xpath = "//input[@id='form_item_betLimitId']"
    cap_xpath = "//input[@id='form_item_topRemain']"
    next_btn_xpath = "//button[contains(@class, 'ant-btn-primary')]//span[text()='下一步']/parent::button"
    cancel_btn_xpath = "//button[contains(@class, 'ant-btn-default')]//span[text()='取 消']/.."

    # print("進入限紅設定階段")

    try:
        # === 1️⃣ 點擊限紅下拉選單 ===
        # 點擊包含選單的 div 容器,而不是 input
        table_limit_xpath = "//div[contains(@class, 'ant-select')][@codefield='betLimitId']"
        table_limit = wait.until(EC.element_to_be_clickable((By.XPATH, table_limit_xpath)))
        
        # 滾動到元素位置
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", table_limit)
        time.sleep(0.5)
        
        table_limit.click()
        # print("已點擊限紅下拉選單")
        time.sleep(1)

        # === 2️⃣ 選擇第一個選項 (100-1000) ===
        first_option_xpath = "//div[contains(@class, 'ant-select-item-option')][@title='100-1000']"
        first_option = wait.until(EC.element_to_be_clickable((By.XPATH, first_option_xpath)))
        first_option.click()
        # print("已選擇限紅選項：100-1000")
        time.sleep(1)

        # === 3️⃣ 輸入封頂數值 ===
        cap_input = wait.until(EC.presence_of_element_located((By.XPATH, cap_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", cap_input)
        time.sleep(0.5)
        
        cap_input.clear()
        cap_input.send_keys("0")
        # print("已輸入封頂數值：0")
        time.sleep(0.5)

        # === 4️⃣ 點擊下一步 ===
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, next_btn_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_btn)
        time.sleep(0.5)
        
        next_btn.click()
        # print("已按下『下一步』")
        time.sleep(2)

        cancel_btn = wait.until(EC.element_to_be_clickable((By.XPATH, cancel_btn_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", cancel_btn)
        time.sleep(0.5)
        
        cancel_btn.click()
        # print("已按下『取消』")
        time.sleep(2)

        # print("限紅流程（Table limit）完成")

    except Exception as e:
        print("Table_limit 發生錯誤：", e)


# =======================================
#  主程式 讓使用者選擇要創建 5 隻或 10 隻
# =======================================

def main():
    driver = create_driver()

    
    # print(f"前往網站：{URL}")
    driver.get(URL)

    # print("已成功導向網站")

    # ⭐ 使用者選擇要創建 5 隻或 10 隻
    while True:
        try:
            create_count = int(input("請選擇要創建帳號數量 (5 或 10)：").strip())
            if create_count in (5, 10):
                break
            else:
                print("請只能輸入 5 或 10")
        except:
            print("請輸入數字 5 或 10")

    print(f"將創建 {create_count} 隻帳號\n")

    # ⭐ 先登入一次代理
    agent_account, agent_password = login(driver)

    # ⭐ TXT 建在桌面
    DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
    txt_path = os.path.join(DESKTOP, f"{agent_account}.txt")

    init_agent_txt(agent_account, agent_password, txt_path)

    # ⭐ 跑 N 次
    for i in range(1, create_count + 1):
        print("\n=============================")
        print(f"開始創建第 {i} 隻帳號")
        print("=============================\n")

        agent_control(driver)

        created_account = create_account(driver)
        print("本次創建的帳號：", created_account)

        set_credit_limit(driver)
        manufacturers(driver)
        hold_position(driver)
        Table_limit(driver)

        append_random_account(created_account, txt_path)
        print(f"已寫入：{created_account} -> {txt_path}")

    # ⭐ 全部創完 → 等 5 秒 → 關閉 → 結束程式
    print(f"\n全部 {create_count} 隻帳號創建完畢")
    print("5 秒後自動關閉瀏覽器並結束程式...")
    time.sleep(5)

    driver.quit()
    os._exit(0)



if __name__ == "__main__":
    main()
