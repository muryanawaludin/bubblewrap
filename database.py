import sqlite3
from datetime import datetime

DB_NAME = "bubble_wrap_system.db"

def init_db():
    """Inisialisasi pembuatan database dan tabel jika belum ada"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Buat tabel transaksi
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabel_transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        waktu TEXT,
        barcode_resi TEXT,
        kategori TEXT,
        ukuran_paket TEXT,
        panjang_meter REAL,
        status TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def log_transaksi(barcode, kategori, ukuran, panjang):
    """Fungsi yang dipanggil mesin saat selesai dispensing"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO tabel_transaksi (waktu, barcode_resi, kategori, ukuran_paket, panjang_meter, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (waktu_sekarang, barcode, kategori, ukuran, panjang, 'SUCCESS'))
    
    conn.commit()
    conn.close()

# Jalankan inisialisasi saat pertama kali
if __name__ == "__main__":
    init_db()
    print("Database SQLite berhasil dibuat!")