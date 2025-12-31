import base64
import os

def convert_file_to_base64():
    # 提示使用者輸入檔案路徑
    file_path = input("base64編碼\n請輸入檔案全域位置 (例如 C:/data/test.txt 或 /home/user/test.txt): ").strip()
    
    # 移除使用者可能誤輸入的引號
    file_path = file_path.replace('"', '').replace("'", "")

    # 檢查檔案是否存在
    if not os.path.exists(file_path):
        print(f"錯誤：找不到檔案 '{file_path}'，請檢查路徑是否正確。")
        return

    try:
        # 取得資料夾路徑、檔名與副檔名
        folder_path = os.path.dirname(file_path)
        file_full_name = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(file_full_name)

        # 讀取原始檔案並進行 Base64 編碼
        with open(file_path, "rb") as f:
            file_content = f.read()
            base64_bytes = base64.b64encode(file_content)
            base64_string = base64_bytes.decode("utf-8")

        # 在終端機顯示結果 (若檔案太大只顯示前 200 字元)
        print("\n--- 轉換結果 ---")
        if len(base64_string) > 200:
            print(base64_string[:200] + " ... (內容過長，已省略後續顯示)")
        else:
            print(base64_string)
        print("----------------\n")

        # 儲存到相同的資料夾
        output_filename = f"{file_name}_en64.txt"
        output_path = os.path.join(folder_path, output_filename)

        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(base64_string)

        print(f"成功！轉換後的內容已儲存至：\n{output_path}")

    except Exception as e:
        print(f"處理過程中發生錯誤: {e}")

if __name__ == "__main__":
    convert_file_to_base64()
