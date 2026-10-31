import streamlit as st
import pandas as pd
import time
import os
import sqlite3
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Bubble Wrap Metering Dispenser", layout="wide")

st.title("📦 Smart Bubble Wrap Dispenser System")
st.subheader("Semi-Auto Metering Control (No Auto-Cutter)")

DB_NAME = "bubble_wrap_system.db"

# --- 1. FUNGSI DATABASE ---
def log_transaksi(barcode, kategori, ukuran, panjang):
    """Fungsi untuk menyimpan log transaksi ke database SQLite"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO tabel_transaksi (waktu, barcode_resi, kategori, ukuran_paket, panjang_meter, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (waktu_sekarang, barcode, kategori, ukuran, panjang, 'SUCCESS'))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Gagal menyimpan ke database: {e}")

@st.cache_data
def load_data():
    file_path = 'Data_Bubble_Wrap.xlsx'
    if not os.path.exists(file_path):
        return None
    df = pd.read_excel(file_path)
    return df

df = load_data()

if df is None:
    st.error("❌ File 'Data_Bubble_Wrap.xlsx' tidak ditemukan di folder yang sama dengan 'app.py'!")
    st.stop()

# Deteksi nama kolom length secara dinamis
length_col = [col for col in df.columns if 'Length' in col or 'Uom' in col][0]

# --- 2. INPUT AREA (OPERATOR CONTROL PANEL) ---
st.sidebar.header("Operator Control Panel")
mode = st.sidebar.radio("Pilih Mode Input:", ("Manual Selection", "Barcode/Scan Mode"))

selected_length = 0
input_identifier = "-"

if mode == "Manual Selection":
    kategori = st.sidebar.selectbox("Pilih Kategori:", df['Kategori'].unique())
    ukuran = st.sidebar.selectbox("Pilih Ukuran:", df[df['Kategori'] == kategori]['Ukuran'].unique())
    
    data_row = df[(df['Kategori'] == kategori) & (df['Ukuran'] == ukuran)]
    selected_length = float(data_row.iloc[0][length_col])
    input_identifier = f"Manual - {kategori}"
    
    st.sidebar.success(f"Target Panjang: **{selected_length} Meter**")

else:
    barcode = st.sidebar.text_input("Scan Barcode Resi / SKU:")
    if barcode:
        st.sidebar.info(f"Scanning: {barcode}...")
        selected_length = 0.44  # Contoh default untuk demo barcode
        input_identifier = barcode
    else:
        st.sidebar.warning("Menunggu scan resi...")

# Copyright Muryan Awaludin di bagian bawah Operator Control Panel
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Copyright © 2026 Muryan Awaludin</p>", unsafe_allow_html=True)

# --- 3. MAIN DASHBOARD (VISUALISASI DISPENSER) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### Status Mesin Dispenser")
    
    status_placeholder = st.empty()
    progress_bar = st.progress(0)
    instruction_box = st.empty()
    
    if st.button("▶ Keluarkan Bubble Wrap (Dispense)", type="primary"):
        if selected_length > 0:
            status_placeholder.info(f"Motor berputar... Mengeluarkan bubble wrap sepanjang {selected_length} meter.")
            instruction_box.warning("⏳ Harap tunggu, motor sedang memberi panjang yang pas...")
            
            # Simulasi pergerakan motor
            for i in range(101):
                time.sleep(0.02)
                progress_bar.progress(i)
            
            status_placeholder.success(f"✔ Berhenti Otomatis! Target {selected_length} meter tercapai.")
            instruction_box.info("✂ Silakan sobek bubble wrap pada tepi meja, lalu ambil paket berikutnya.")
            
            # --- EKSEKUSI PENCATATAN KE DATABASE DI SINI ---
            # Data otomatis disimpan ke database saat proses dispensing sukses
            kategori_val = kategori if mode == "Manual Selection" else "Barcode Scan Item"
            ukuran_val = ukuran if mode == "Manual Selection" else "Standard Size"
            
            log_transaksi(
                barcode=input_identifier, 
                kategori=kategori_val, 
                ukuran=ukuran_val, 
                panjang=selected_length
            )
            
        else:
            st.error("Silakan pilih ukuran atau scan barcode terlebih dahulu.")

with col2:
    st.write("### Data Database Acuan")
    st.dataframe(df, use_container_width=True)

    st.write("### Log Sistem")
    st.code("System Ready...\nDatabase Connection: ACTIVE")