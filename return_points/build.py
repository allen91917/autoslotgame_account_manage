"""
打包 main.py 成 Windows 可執行文件
使用 PyInstaller 進行打包

使用說明：
1. 先安裝 PyInstaller: pip install pyinstaller
2. 執行此腳本: python build.py
3. 打包完成後，可執行文件會在 dist 資料夾中
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_pyinstaller():
    """檢查是否已安裝 PyInstaller"""
    try:
        import PyInstaller
        print("✓ PyInstaller 已安裝")
        return True
    except ImportError:
        print("✗ PyInstaller 未安裝")
        print("正在安裝 PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller 安裝成功")
            return True
        except Exception as e:
            print(f"✗ PyInstaller 安裝失敗: {e}")
            return False


def clean_build_folders():
    """清理之前的打包文件"""
    folders_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    print("\n清理舊的打包文件...")
    for folder in folders_to_clean:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✓ 已刪除 {folder}")
    
    # 清理 .spec 文件
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"✓ 已刪除 {spec_file}")


def build_exe():
    """使用 PyInstaller 打包成 exe"""
    print("\n開始打包...")
    
    # PyInstaller 參數配置
    pyinstaller_args = [
        'main.py',                          # 主程式文件
        '--name=返點系統',                   # 輸出的 exe 名稱
        '--onefile',                        # 打包成單一執行文件
        '--console',                       # 顯示控制台視窗
        '--icon=NONE',                      # 圖標（如有需要可以指定 .ico 文件）
        '--clean',                          # 清理臨時文件
        '--noconfirm',                      # 不詢問確認
        
        # 包含資料文件
        '--add-data=用戶資訊.txt;.',         # Windows 使用分號，將文件包含到根目錄
        
        # 隱藏導入（確保這些模組被包含）
        '--hidden-import=selenium',
        '--hidden-import=selenium.webdriver',
        '--hidden-import=selenium.webdriver.chrome',
        '--hidden-import=selenium.webdriver.chrome.service',
        '--hidden-import=selenium.webdriver.common.by',
        '--hidden-import=selenium.webdriver.support.ui',
        '--hidden-import=selenium.webdriver.support.expected_conditions',
        '--hidden-import=webdriver_manager',
        '--hidden-import=webdriver_manager.chrome',
        '--hidden-import=colorama',
        '--hidden-import=logging',
        '--hidden-import=threading',
        
        # 排除不需要的模組以減小文件大小
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        '--exclude-module=tkinter',
        
        # 其他選項
        '--noupx',                          # 不使用 UPX 壓縮（避免某些防毒軟體誤報）
    ]
    
    try:
        # 執行 PyInstaller
        subprocess.check_call(['pyinstaller'] + pyinstaller_args)
        print("\n" + "="*60)
        print("✓ 打包成功！")
        print("="*60)
        print("\n打包文件位置:")
        print(f"  - 可執行文件: {os.path.abspath('dist/返點系統.exe')}")
        print("\n使用說明:")
        print("  1. 將 dist 資料夾中的 '返點系統.exe' 複製到 Windows 電腦")
        print("  2. 確保 '用戶資訊.txt' 在相同目錄下（已內建，但也可外部提供）")
        print("  3. 確保 Windows 電腦已安裝 Google Chrome 瀏覽器")
        print("  4. 雙擊 '返點系統.exe' 執行")
        print("\n注意事項:")
        print("  - 首次執行時，會自動下載 ChromeDriver")
        print("  - 確保有穩定的網路連接")
        print("  - 建議在 Windows 10/11 64位元系統上運行")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 打包失敗: {e}")
        return False
    except Exception as e:
        print(f"\n✗ 發生錯誤: {e}")
        return False


def create_readme():
    """創建使用說明文件"""
    readme_content = """返點系統 使用說明
==================

系統需求：
---------
1. Windows 10/11 64位元作業系統
2. Google Chrome 瀏覽器（最新版本）
3. 穩定的網路連接

使用步驟：
---------
1. 準備 '用戶資訊.txt' 文件（如果需要修改帳號資訊）
   格式：帳號,密碼,金額
   範例：
   user1,pass123,5000
   user2,pass456,8000
   # 開頭為註解行，會被忽略

2. 雙擊執行 '返點系統.exe'

3. 程式會自動：
   - 初始化 Chrome 瀏覽器
   - 登入各個帳號
   - 處理會員餘額調整
   - 完成後自動關閉

注意事項：
---------
- 首次執行時會自動下載 ChromeDriver，需要網路連接
- 執行期間不要關閉瀏覽器視窗
- 如遇到問題，請檢查 '用戶資訊.txt' 格式是否正確
- 建議執行時關閉防毒軟體或將此程式加入白名單

常見問題：
---------
Q: 程式無法啟動？
A: 確認已安裝 Google Chrome 瀏覽器

Q: 顯示帳號密碼錯誤？
A: 檢查 '用戶資訊.txt' 中的帳號密碼是否正確

Q: 處理速度很慢？
A: 多線程同時處理多個帳號，請耐心等待

聯絡支援：
---------
如有問題請聯絡系統管理員
"""
    
    try:
        readme_path = os.path.join('dist', '使用說明.txt')
        if os.path.exists('dist'):
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print(f"✓ 已創建使用說明: {readme_path}")
    except Exception as e:
        print(f"✗ 創建使用說明失敗: {e}")


def main():
    """主程式"""
    print("="*60)
    print("返點系統 - Windows EXE 打包工具")
    print("="*60)
    
    # 檢查是否在正確的目錄
    if not os.path.exists('main.py'):
        print("✗ 錯誤: 找不到 main.py")
        print("請在 return_points 資料夾中執行此腳本")
        return
    
    if not os.path.exists('用戶資訊.txt'):
        print("⚠ 警告: 找不到 用戶資訊.txt")
        print("打包後需要手動提供此文件")
    
    # 檢查 PyInstaller
    if not check_pyinstaller():
        print("\n請手動安裝 PyInstaller: pip install pyinstaller")
        return
    
    # 清理舊文件
    clean_build_folders()
    
    # 開始打包
    success = build_exe()
    
    if success:
        # 創建使用說明
        create_readme()
        
        print("\n" + "="*60)
        print("打包完成！請到 dist 資料夾查看結果")
        print("="*60)
    else:
        print("\n打包失敗，請檢查錯誤訊息")


if __name__ == "__main__":
    main()
