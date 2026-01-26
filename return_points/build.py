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
        '--name=main',                      # 輸出的 exe 名稱
        '--onefile',                        # 打包成單一執行文件
        '--console',                        # 顯示控制台視窗
        '--icon=NONE',                      # 圖標（如有需要可以指定 .ico 文件）
        '--clean',                          # 清理臨時文件
        '--noconfirm',                      # 不詢問確認
        
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
        print(f"  - 可執行文件: {os.path.abspath('dist/main.exe')}")
        print("\n使用說明:")
        print("  1. 將 dist 資料夾整個複製到 Windows 電腦")
        print("  2. dist 資料夾中包含:")
        print("     - main.exe (主程式)")
        print("     - 用戶資訊.txt (帳號設定檔)")
        print("  3. 確保 Windows 電腦已安裝 Google Chrome 瀏覽器")
        print("  4. 雙擊 'main.exe' 執行")
        print("\n注意事項:")
        print("  - 首次執行時，會自動下載 ChromeDriver")
        print("  - 確保有穩定的網路連接")
        print("  - 建議在 Windows 10/11 64位元系統上運行")
        print("  - 支援中文路徑環境")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 打包失敗: {e}")
        return False
    except Exception as e:
        print(f"\n✗ 發生錯誤: {e}")
        return False


def copy_user_info():
    """複製用戶資訊.txt到dist資料夾"""
    try:
        if not os.path.exists('dist'):
            print("✗ dist 資料夾不存在")
            return False
        
        if os.path.exists('用戶資訊.txt'):
            shutil.copy2('用戶資訊.txt', 'dist/用戶資訊.txt')
            print("✓ 已複製 用戶資訊.txt 到 dist 資料夾")
            return True
        else:
            print("⚠ 警告: 找不到 用戶資訊.txt，請手動放置到 dist 資料夾")
            # 創建範例文件
            sample_content = """# 用戶資訊設定檔
# 格式：帳號,密碼,目標金額
# 範例：
# user1,password123,5000
# user2,password456,8000

# 請在下方填寫實際的帳號資訊
"""
            with open('dist/用戶資訊.txt', 'w', encoding='utf-8') as f:
                f.write(sample_content)
            print("✓ 已創建範例 用戶資訊.txt 到 dist 資料夾")
            return True
    except Exception as e:
        print(f"✗ 複製用戶資訊.txt失敗: {e}")
        return False


def main():
    """主程式"""
    print("="*60)
    print("返點系統 - Windows EXE 打包工具")
    print("="*60)
    
    # 切換到腳本所在的目錄
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"工作目錄: {script_dir}")
    
    # 檢查是否在正確的目錄
    if not os.path.exists('main.py'):
        print("✗ 錯誤: 找不到 main.py")
        print("請確保 main.py 與 build.py 在同一資料夾中")
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
        # 複製用戶資訊檔案
        copy_user_info()
        
        # 清理緩存檔案，只保留 dist
        print("\n清理緩存檔案...")
        folders_to_clean = ['build', '__pycache__']
        for folder in folders_to_clean:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"✓ 已刪除 {folder}")
        
        # 清理 .spec 文件
        for spec_file in Path('.').glob('*.spec'):
            spec_file.unlink()
            print(f"✓ 已刪除 {spec_file}")
        
        print("\n" + "="*60)
        print("打包完成！")
        print("="*60)
        print("\n最終檔案結構:")
        print("dist/")
        print("  ├── main.exe")
        print("  └── 用戶資訊.txt")
        print("\n請將整個 dist 資料夾複製到 Windows 電腦使用")
        print("="*60)
    else:
        print("\n打包失敗，請檢查錯誤訊息")


if __name__ == "__main__":
    main()
