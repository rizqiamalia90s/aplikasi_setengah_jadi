#deteksi csp.exe sebagai virus lalu tampilkan notifikasi
#deteksi kedua file dengan nama sama dan menampilkan mana yang virus

import os
import psutil
from datetime import datetime

class FileManager:
    def __init__(self):
        # Inisialisasi path awal ke desktop
        self.current_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        
    def get_absolute_path(self, nama):
        # Menggabungkan current_path dengan nama file/folder
        return os.path.join(self.current_path, nama)

    def pindah_direktori(self):
        try:
            print(f"\nLokasi sekarang: {self.current_path}")
            target = input("Masukkan path tujuan (..: folder sebelumnya, /: ke Desktop): ")
            
            if target == "/":
                # Kembali ke desktop
                self.current_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            elif target == "..":
                # Mundur satu folder
                self.current_path = os.path.dirname(self.current_path)
            else:
                # Gabungkan dengan path sekarang
                new_path = os.path.join(self.current_path, target)
                if os.path.exists(new_path) and os.path.isdir(new_path):
                    self.current_path = new_path
                else:
                    print("Folder tidak ditemukan!")
                    return
                
            print(f"Pindah ke: {self.current_path}")
            
        except Exception as e:
            print(f"Terjadi kesalahan: {str(e)}")

    def buat_file(self):
        try:
            print(f"\nLokasi sekarang: {self.current_path}")
            nama_file = input("Masukkan nama file (dengan .txt): ")
            file_path = self.get_absolute_path(nama_file)
            
            print("\nMasukkan isi file (tekan Enter dua kali untuk selesai):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
                
            with open(file_path, "w") as file:
                file.write("\n".join(lines))
            print(f"\nFile berhasil dibuat di: {file_path}")
        except Exception as e:
            print(f"Terjadi kesalahan saat membuat file: {str(e)}")

    def baca_file(self):
        try:
            print(f"\nLokasi sekarang: {self.current_path}")
            nama_file = input("Masukkan nama file yang ingin dibaca: ")
            file_path = self.get_absolute_path(nama_file)
            
            print("\nIsi file:")
            print("-" * 50)
            with open(file_path, "r") as file:
                print(file.read())
            print("-" * 50)
        except FileNotFoundError:
            print("File tidak ditemukan!")
        except Exception as e:
            print(f"Terjadi kesalahan saat membaca file: {str(e)}")

    def buat_folder(self):
        try:
            print(f"\nLokasi sekarang: {self.current_path}")
            nama_folder = input("Masukkan nama folder yang ingin dibuat: ")
            folder_path = self.get_absolute_path(nama_folder)
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"\nFolder '{nama_folder}' berhasil dibuat di: {folder_path}")
            else:
                print(f"\nFolder '{nama_folder}' sudah ada!")
        except Exception as e:
            print(f"Terjadi kesalahan saat membuat folder: {str(e)}")

    def tampilkan_isi_folder(self):
        try:
            print(f"\nLokasi sekarang: {self.current_path}")
            print("\nIsi folder saat ini:")
            print("-" * 50)
            
            isi_folder = os.listdir(self.current_path)
            if not isi_folder:
                print("Folder kosong!")
            else:
                for item in isi_folder:
                    item_path = self.get_absolute_path(item)
                    if os.path.isfile(item_path):
                        print(f"File  : {item}")
                    elif os.path.isdir(item_path):
                        print(f"Folder: {item}")
            print("-" * 50)
        except Exception as e:
            print(f"Terjadi kesalahan saat membaca folder: {str(e)}")

def tampilkan_proses():
    try:
        print("\nDaftar Proses yang Sedang Berjalan:")
        print("-" * 130)
        print(f"{'PID':<8} {'Nama Proses':<25} {'Executable':<30} {'Status':<10} {'Memory (MB)':<12} {'CPU %':<8} {'Threads':<8} {'Created':<20}")
        print("-" * 130)
        
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'status', 'memory_info', 'cpu_percent', 'num_threads', 'create_time']):
            try:
                info = proc.info
                # Dapatkan informasi dasar
                pid = info['pid']
                nama = info['name']
                exe = info['exe'] if info['exe'] else "N/A"
                exe = os.path.basename(exe)  # Ambil nama file saja
                status = info['status']
                
                # Informasi memory
                memory = info['memory_info'].rss / 1024 / 1024  # Konversi ke MB
                
                # CPU usage
                cpu = info['cpu_percent']
                
                # Thread count
                threads = info['num_threads']
                
                # Creation time
                created = datetime.fromtimestamp(info['create_time']).strftime('%Y-%m-%d %H:%M:%S')
                
                # Format dan print informasi
                print(f"{pid:<8} {nama[:24]:<25} {exe[:29]:<30} {status[:9]:<10} {memory:,.2f}MB{' ':<4} {cpu:,.1f}%{' ':<2} {threads:<8} {created}")
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
                pass
            except Exception as e:
                print(f"Error pada proses: {str(e)}")
                
        print("-" * 130)
        
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca proses: {str(e)}")

def main():
    fm = FileManager()
    
    while True:
        print("\nMenu Utama:")
        print("1. Manajemen File")
        print("2. Manajemen Folder")
        print("3. Task Manager")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1-4): ")
        
        if pilihan == "1":
            while True:
                print("\nMenu File:")
                print("1. Buat File Teks")
                print("2. Baca File Teks")
                print("3. Pindah Direktori")
                print("4. Kembali ke Menu Utama")
                
                sub_pilihan = input("Pilih menu (1-4): ")
                if sub_pilihan == "1":
                    fm.buat_file()
                elif sub_pilihan == "2":
                    fm.baca_file()
                elif sub_pilihan == "3":
                    fm.pindah_direktori()
                elif sub_pilihan == "4":
                    break
                else:
                    print("Pilihan tidak valid!")
                    
        elif pilihan == "2":
            while True:
                print("\nMenu Folder:")
                print("1. Buat Folder")
                print("2. Tampilkan Isi Folder")
                print("3. Pindah Direktori")
                print("4. Kembali ke Menu Utama")
                
                sub_pilihan = input("Pilih menu (1-4): ")
                if sub_pilihan == "1":
                    fm.buat_folder()
                elif sub_pilihan == "2":
                    fm.tampilkan_isi_folder()
                elif sub_pilihan == "3":
                    fm.pindah_direktori()
                elif sub_pilihan == "4":
                    break
                else:
                    print("Pilihan tidak valid!")
                    
        elif pilihan == "3":
            tampilkan_proses()
            
        elif pilihan == "4":
            print("Program selesai!")
            break
            
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main() 