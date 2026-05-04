import os
from bs4 import BeautifulSoup

def extract_link_tags(directory):
    # Ekstensi file yang ingin diperiksa (tambahkan jika ada .jsx, .vue, dll)
    valid_extensions = ('.html', '.php', '.js', '.jsx', '.tsx')
    
    print(f"Mencari tag <link> di direktori:\n{directory}\n")
    print("-" * 50)

    # os.walk akan menelusuri folder utama dan semua subfoldernya
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(valid_extensions):
                file_path = os.path.join(root, file)
                
                try:
                    # Membuka file. Menggunakan errors='ignore' agar script tidak crash jika ada karakter aneh
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    # Parsing isi file sebagai HTML
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Mencari semua tag <link>
                    link_tags = soup.find_all('link')
                    
                    # Jika tag <link> ditemukan di file ini, cetak hasilnya
                    if link_tags:
                        print(f"\n📄 Ditemukan di file: {file_path}")
                        for tag in link_tags:
                            print(f"   {tag}")
                            
                except Exception as e:
                    print(f"Gagal membaca {file_path} karena: {e}")

# Path folder yang Anda berikan (menggunakan 'r' di depan untuk raw string Windows path)
folder_path = r"D:\Kuliah\joki\Kerja Praktek Aqil\kp aqil\backend\FE\stitch_seblak_rika_customer_portal"

if __name__ == "__main__":
    if os.path.exists(folder_path):
        extract_link_tags(folder_path)
    else:
        print(f"Folder tidak ditemukan: {folder_path}\nPastikan path tersebut benar.")