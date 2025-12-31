import base64
import os
try:
    import magic
    # Windows 使用者需要確保 python-magic-bin 也安裝了
    magic_instance = magic.Magic(mime=True)
except ImportError:
    print("警告：缺少 python-magic 庫，將使用基本檔案類型判斷。")

mime_map = {
    # --- 文字與文件 ---
    'text/plain': '.txt',
    'application/pdf': '.pdf',
    'application/msword': '.doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'application/vnd.ms-excel': '.xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
    'application/vnd.ms-powerpoint': '.ppt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
    'text/html': '.html',
    'text/css': '.css',
    'text/csv': '.csv',
    'application/json': '.json',
    'application/xml': '.xml',
    'application/rtf': '.rtf',
    'application/epub+zip': '.epub',

    # --- 圖片 ---
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/gif': '.gif',
    'image/webp': '.webp',
    'image/bmp': '.bmp',
    'image/x-icon': '.ico',
    'image/vnd.microsoft.icon': '.ico',
    'image/tiff': '.tiff',
    'image/svg+xml': '.svg',
    'image/heic': '.heic',
    'image/heif': '.heif',
    'image/avif': '.avif',
    'image/photoshop': '.psd',
    'application/x-photoshop': '.psd',

    # --- 音訊 ---
    'audio/mpeg': '.mp3',
    'audio/wav': '.wav',
    'audio/x-wav': '.wav',
    'audio/ogg': '.ogg',
    'audio/flac': '.flac',
    'audio/aac': '.aac',
    'audio/midi': '.mid',
    'audio/x-m4a': '.m4a',
    'audio/mp4': '.m4a',

    # --- 影片 ---
    'video/mp4': '.mp4',
    'video/x-matroska': '.mkv',
    'video/x-msvideo': '.avi',
    'video/quicktime': '.mov',
    'video/webm': '.webm',
    'video/x-flv': '.flv',
    'video/mpeg': '.mpeg',

    # --- 壓縮檔 ---
    'application/zip': '.zip',
    'application/x-rar-compressed': '.rar',
    'application/x-7z-compressed': '.7z',
    'application/x-tar': '.tar',
    'application/x-gzip': '.gz',
    'application/x-bzip2': '.bz2',
    'application/x-xz': '.xz',

    # --- 執行檔與系統檔 ---
    'application/x-msdownload': '.exe',
    'application/x-dosexec': '.exe',        # 解決你遇到的 GitHub Desktop 問題
    'application/x-msdos-program': '.exe',  # 傳統 DOS/Windows 程序
    'application/x-msi': '.msi',            # Windows 安裝套件
    'application/x-apple-diskimage': '.dmg',# macOS 磁碟映像
    'application/x-sh': '.sh',              # Shell Script
    'application/x-executable': '.bin',      # Linux 執行檔

    # --- 字體 ---
    'font/ttf': '.ttf',
    'font/otf': '.otf',
    'font/woff': '.woff',
    'font/woff2': '.woff2',
    'application/vnd.ms-fontobject': '.eot',
}


def convert_base64_to_file():
    # 1. 提示使用者輸入檔案路徑
    # .strip()去除首尾空格
    file_path = input("base64解碼\n請輸入檔案全域位置 (例如 C:/data/test.txt 或 /home/user/test.txt): ").strip()
    
    # 移除使用者可能誤輸入的引號 (拖曳檔案進終端機時常會帶有引號)
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

        # 2. 讀取原始檔案並進行 Base64 解碼
        # open()第二個參數決定對待檔案的方式, r=read, w=write, b以位元組型態, rb以位元組型態讀入, wb以位元組型態寫入(例如圖片)
        # f 變數只是檔案控制握把
        # file_content, base64_bytes 皆是 bytes型態，但其內容不一樣
        # Base64 會把原始資料每 3 個 Byte 一組，重新切分成 4 個 Byte，並且對照 Base64 表格 換成特定的字元
        with open(file_path, "rb") as f:
            file_content = f.read()
            base64_bytes = base64.b64decode(file_content)

        # 檔案格式
        mime_type = magic.from_buffer(base64_bytes, mime=True)
        print(f"偵測到文件類型: {mime_type}")

        # 從清單中尋找
        doc_type = mime_map.get(mime_type)

        # 3. 在終端機顯示結果
        print("\n--- 轉換結果 ---")
        if doc_type:
            if doc_type == '.txt':
                preview = base64_bytes.decode("utf-8")
                print(preview)
            else:
                print(f"內容為二進位格式({doc_type})，無法以文字預覽")
        else:
            if mime_type and '/' in mime_type:
                # 取得/後面的部分作為副檔名, 以及特殊後綴 .x-pitch
                auto_ext = mime_type.split('/')[-1]
                doc_type = '.' + auto_ext.replace('x-', '')
            else:
                doc_type = '.bin'
            print(f"內容為二進位格式({doc_type})，無法以文字預覽")
        print("----------------\n")

        # 4. 儲存到相同的資料夾
        output_filename = f"{file_name}_de64{doc_type}"
        output_path = os.path.join(folder_path, output_filename)

        if doc_type == '.txt':
            with open(output_path, "w", encoding='utf-8', newline='') as out_file:
                origin_string = base64_bytes.decode('utf-8')
                out_file.write(origin_string)
        else:
            # wb模式不需要encoding或newline
            with open(output_path, "wb") as out_file:
                out_file.write(base64_bytes)

        print(f"成功！轉換後的內容已儲存至：\n{output_path}")

    except Exception as e:
        print(f"處理過程中發生錯誤: {e}")

if __name__ == "__main__":
    convert_base64_to_file()
