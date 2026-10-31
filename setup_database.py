import pandas as pd
import sqlite3
import os

# Nama file Excel dan Database
excel_file = 'Data_Bubble_Wrap.xlsx'
db_file = 'bubble_wrap_system.db'

print("Memulai pembuatan database otomatis...")

# 1. Periksa apakah file Excel ada
if not os.path.exists(excel_file):
    print(f"❌ Error: File '{excel_file}' tidak ditemukan di folder ini!")
    exit()

# 2. Baca file Excel
df = pd.read_excel(excel_file)
print("✔ Data Excel berhasil dibaca.")

# 3. Hubungkan ke database SQLite (file akan otomatis dibuat jika belum ada)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 4. Buat tabel transaksi untuk mencatat log mesin
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
print("✔ Tabel 'tabel_transaksi' berhasil dibuat.")

# 5. Masukkan data Excel secara otomatis ke 'tabel_parameter'
df_sql = df.rename(columns={
    'Kategori': 'kategori',
    'Uom Length - Meter (width 40cm)': 'max_panjang_meter',
    'Ukuran': 'ukuran'
})

df_sql.to_sql('tabel_parameter', conn, if_exists='replace', index=False)
print("✔ Tabel 'tabel_parameter' berhasil dibuat dan data Excel berhasil diimpor!")

# Tutup koneksi database
conn.commit()
conn.close()

print(f"\n🎉 Selesai! File database '{db_file}' siap digunakan.")