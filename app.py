import streamlit as st
import requests
import pandas as pd
from datetime import date
import base64
import os
import plotly.express as px # Untuk grafik dashboard

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="E-Imunisasi 2026", layout="wide", page_icon="💉")

# --- DATA KONEKSI DATABASE ---
url_base = "https://klvgimcpywyulayidpab.supabase.co/rest/v1/imunisasi"
api_key = "sb_publishable_gpm6D65eeBUufZYpE9aGqg_mWUG_YhC"
headers = {
    "apikey": api_key,
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# --- FUNGSI MEMBACA LOGO ---
def get_base64_png(file_name):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

img_data = get_base64_png("istockphoto-1323619822-612x612.png")

# --- SISTEM LOGIN SEDERHANA ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    st.markdown("<h2 style='text-align:center; color:#4a148c;'>🔐 Login Petugas</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        submit_login = st.form_submit_button("MASUK")
        if submit_login:
            # Ganti username & password sesukanya di sini
            if user == "admin" and pwd == "imunisasi2026":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Username atau Password salah!")

# --- JIKA BELUM LOGIN, TAMPILKAN HALAMAN LOGIN ---
if not st.session_state['logged_in']:
    login()
    st.stop()

# --- JIKA SUDAH LOGIN, TAMPILKAN MENU UTAMA ---
st.sidebar.title("📌 MENU UTAMA")
menu = st.sidebar.radio("Pilih Halaman:", ["Input Data", "Dashboard Monitoring", "Keluar"])

if menu == "Keluar":
    st.session_state['logged_in'] = False
    st.rerun()

# --- CSS GLOBAL ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); font-family: 'Poppins', sans-serif; }
    .header-box { display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 20px; }
    .judul-teks { color: #4a148c; font-weight: 800; font-size: 3rem; margin: 0; }
    div[data-testid="stMetricValue"] { color: #4a148c; }
</style>
""", unsafe_allow_html=True)

# --- HALAMAN 1: INPUT DATA ---
if menu == "Input Data":
    if img_data:
        st.markdown(f'<div class="header-box"><img src="data:image/png;base64,{img_data}" height="60"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    
    with st.form("main_form", clear_on_submit=True):
        st.markdown("### 👨‍⚕️ Petugas & 👶 Anak")
        col1, col2 = st.columns(2)
        with col1:
            nama_petugas = st.selectbox("Petugas*", ["-- Pilih --", "Winoto Hadi", "Yanto Perdianta", "Eva Asri", "Desiani", "Dian Yuniarsih"])
            nama_anak = st.text_input("Nama Anak*")
        with col2:
            nik = st.text_input("NIK*")
            tgl_lahir = st.date_input("Tanggal Lahir")
        
        st.markdown("### 💉 Vaksinasi")
        vaksin_pilihan = st.multiselect("Pilih Vaksin*", ["BCG", "Polio", "DPT 1", "DPT 2", "Campak", "PCV"])
        
        submit = st.form_submit_button("SIMPAN DATA")
        if submit:
            if nama_petugas == "-- Pilih --" or not nama_anak or not nik:
                st.error("Data wajib belum lengkap!")
            else:
                payload = {"nama_petugas": nama_petugas, "nama_anak": nama_anak, "nik_anak": nik, "vaksin": ", ".join(vaksin_pilihan), "tgl_lahir": str(tgl_lahir)}
                res = requests.post(url_base, json=payload, headers=headers)
                if res.status_code in [200, 201]:
                    st.success("Berhasil disimpan!")
                    st.balloons()

# --- HALAMAN 2: DASHBOARD MONITORING ---
elif menu == "Dashboard Monitoring":
    st.markdown("<h1 style='color:#4a148c;'>📊 Dashboard Monitoring</h1>", unsafe_allow_html=True)
    
    # Ambil data dari Supabase
    res = requests.get(url_base, headers=headers)
    if res.status_code == 200:
        data = res.json()
        df = pd.DataFrame(data)
        
        if not df.empty:
            # Baris 1: Ringkasan
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Imunisasi", len(df))
            c2.metric("Petugas Aktif", df['nama_petugas'].nunique())
            c3.metric("Jenis Vaksin", 12) # Contoh statis
            
            # Baris 2: Grafik & Tabel
            col_left, col_right = st.columns([1, 1])
            with col_left:
                st.markdown("### 📈 Tren Per Petugas")
                fig = px.bar(df['nama_petugas'].value_counts(), color_discrete_sequence=['#9c27b0'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col_right:
                st.markdown("### 📋 Data Terbaru")
                st.dataframe(df[['nama_anak', 'vaksin', 'nama_petugas']].tail(10), use_container_width=True)
        else:
            st.info("Belum ada data di database.")