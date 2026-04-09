import streamlit as st
import requests
import pandas as pd
from datetime import date
import base64
import os
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="E-Imunisasi 2026", layout="centered", page_icon="💉")

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

# --- CSS GLOBAL ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); font-family: 'Poppins', sans-serif; }
    .header-box { display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 10px; }
    .judul-teks { color: #4a148c; font-weight: 800; font-size: 3rem; margin: 0; letter-spacing: -1px; }
    .sub-judul { color: #7b1fa2; text-align: center; font-size: 1rem; margin-bottom: 20px; margin-top: -10px; }
    div[data-testid="stForm"] { background-color: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
    .stButton>button { width: 100%; border-radius: 12px; height: 3em; background: linear-gradient(45deg, #7b1fa2, #9c27b0); color: white; font-weight: 600; border: none; }
</style>
""", unsafe_allow_html=True)

# --- SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    # Tampilan Judul di Halaman Login
    if img_data:
        st.markdown(f'<div class="header-box"><img src="data:image/png;base64,{img_data}" height="60"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    else:
        st.markdown('<h1 style="text-align:center; color:#4a148c;">E-IMUNISASI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-judul">Sistem Pencatatan Imunisasi Digital Terpadu</p>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("<h3 style='text-align:center; color:#4a148c;'>🔐 Login Petugas</h3>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        submit_login = st.form_submit_button("MASUK")
        if submit_login:
            if user == "admin" and pwd == "imunisasi2026":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Username atau Password salah!")
    st.stop()

# --- SIDEBAR NAVIGASI (Hanya muncul jika sudah login) ---
st.sidebar.title("📌 Navigasi")
menu = st.sidebar.radio("Pilih Halaman:", ["Input Data", "Dashboard Monitoring", "Keluar"])

if menu == "Keluar":
    st.session_state['logged_in'] = False
    st.rerun()

# --- HALAMAN 1: INPUT DATA ---
if menu == "Input Data":
    if img_data:
        st.markdown(f'<div class="header-box"><img src="data:image/png;base64,{img_data}" height="60"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="sub-judul">Formulir Input Data Imunisasi</p>', unsafe_allow_html=True)
    
    with st.form("main_form", clear_on_submit=True):
        st.markdown("### 👨‍⚕️ Data Petugas")
        daftar_petugas = ["-- Pilih --", "Winoto Hadi, A.Md.Kep", "Yanto Perdianta, S.Kep.Ns", "Eva Asri Deti, A.Md.Keb", "Desiani, A.Md.Keb", "Dian Yuniarsih, A.Md.Keb", "Florentina Ina, A.Md.Keb"]
        nama_petugas = st.selectbox("Nama Petugas*", daftar_petugas)
        
        st.markdown("### 👶 Data Anak")
        c1, c2 = st.columns(2)
        with c1:
            nama_anak = st.text_input("Nama Lengkap Anak*")
            nik = st.text_input("NIK Anak*")
            jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True)
        with c2:
            tgl_lahir = st.date_input("Tanggal Lahir")
            # Hitung Usia Otomatis
            today = date.today()
            usia_bln = (today.year - tgl_lahir.year) * 12 + today.month - tgl_lahir.month
            st.info(f"Usia saat ini: **{usia_bln} Bulan**")

        st.markdown("### 👪 Data Orang Tua & Alamat")
        c3, c4 = st.columns(2)
        with c3:
            nama_ayah = st.text_input("Nama Ayah")
            nama_ibu = st.text_input("Nama Ibu")
        with c4:
            alamat = st.text_area("Alamat Lengkap Domisili")

        st.markdown("### 💉 Tindakan Vaksinasi")
        daftar_vaksin = ["HB O Inject", "BCG", "Polio 1", "DPT 1", "Polio 2", "Rotavirus 1", "DPT 2", "Polio 3", "Campak", "PCV"]
        vaksin_pilihan = st.multiselect("Pilih Vaksin*", daftar_vaksin)

        submit = st.form_submit_button("SIMPAN DATA IMUNISASI")

        if submit:
            if nama_petugas == "-- Pilih --" or not nama_anak or not nik:
                st.error("❌ Nama Petugas, Nama Anak, dan NIK wajib diisi!")
            else:
                payload = {
                    "nama_petugas": nama_petugas, "nama_anak": nama_anak, "nik_anak": nik,
                    "tgl_lahir": str(tgl_lahir), "jenis_kelamin": jk, "usia_bulan": usia_bln,
                    "nama_ayah": nama_ayah, "nama_ibu": nama_ibu, "alamat": alamat,
                    "vaksin": ", ".join(vaksin_pilihan)
                }
                try:
                    res = requests.post(url_base, json=payload, headers=headers)
                    if res.status_code in [200, 201]:
                        st.balloons()
                        st.success(f"✅ Data {nama_anak} berhasil disimpan!")
                except:
                    st.error("Gagal terhubung ke database.")

# --- HALAMAN 2: DASHBOARD MONITORING ---
elif menu == "Dashboard Monitoring":
    st.markdown("<h1 style='text-align:center; color:#4a148c;'>📊 Dashboard Monitoring</h1>", unsafe_allow_html=True)
    
    res = requests.get(url_base, headers=headers)
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        if not df.empty:
            # Baris Ringkasan
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Anak", len(df))
            col2.metric("Petugas Terlibat", df['nama_petugas'].nunique())
            col3.metric("Update Terakhir", str(date.today()))
            
            # Grafik
            st.markdown("### 📈 Grafik Kinerja Petugas")
            fig = px.bar(df['nama_petugas'].value_counts().reset_index(), x='index', y='nama_petugas', 
                         labels={'index':'Nama Petugas', 'nama_petugas':'Jumlah Input'},
                         color_discrete_sequence=['#9c27b0'])
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### 📋 Tabel Riwayat Data")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Belum ada data yang tersimpan.")

# --- FOOTER ---
st.markdown("""
<div style="text-align: center; color: #7b1fa2; font-size: 0.85rem; margin-top: 30px;">
    <hr style="border-top: 1px solid #e1bee7;">
    © 2026 Aplikasi E-Imunisasi Digital - Dev by Riko Putra
</div>
""", unsafe_allow_html=True)