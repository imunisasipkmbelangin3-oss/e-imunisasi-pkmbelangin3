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
    if img_data:
        st.markdown(f'<div class="header-box"><img src="data:image/png;base64,{img_data}" height="60"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    else:
        st.markdown('<h1 style="text-align:center; color:#4a148c;">E-IMUNISASI</h1>', unsafe_allow_html=True)
    
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

# --- NAVIGASI ---
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio("Pindah Halaman:", ["Input Data", "Dashboard Monitoring", "Keluar"])

if menu == "Keluar":
    st.session_state['logged_in'] = False
    st.rerun()

# --- HALAMAN 1: INPUT DATA ---
if menu == "Input Data":
    if img_data:
        st.markdown(f'<div class="header-box"><img src="data:image/png;base64,{img_data}" height="60"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    
    with st.form("main_form", clear_on_submit=True):
        st.markdown("### 👨‍⚕️ Petugas")
        nama_petugas = st.selectbox("Nama Petugas*", ["-- Pilih --", "Winoto Hadi, A.Md.Kep", "Yanto Perdianta, S.Kep.Ns", "Eva Asri Deti, A.Md.Keb", "Desiani, A.Md.Keb", "Dian Yuniarsih, A.Md.Keb"])
        
        st.markdown("### 👶 Data Anak")
        c1, c2 = st.columns(2)
        with c1:
            nama_anak = st.text_input("Nama Anak*")
            nik = st.text_input("NIK*")
            jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True)
        with c2:
            tgl_lahir = st.date_input("Tanggal Lahir")
            tgl_skrg = date.today()
            usia_bln = (tgl_skrg.year - tgl_lahir.year) * 12 + tgl_skrg.month - tgl_lahir.month
            st.info(f"Usia: **{usia_bln} Bulan**")

        st.markdown("### 👪 Orang Tua & Alamat")
        c3, c4 = st.columns(2)
        with c3:
            nama_ayah = st.text_input("Nama Ayah")
            nama_ibu = st.text_input("Nama Ibu")
        with c4:
            alamat = st.text_area("Alamat Lengkap")

        st.markdown("### 💉 Vaksin")
        vaksin = st.multiselect("Vaksin*", ["HB O", "BCG", "Polio 1", "DPT 1", "PCV 1", "Campak"])
        
        submit = st.form_submit_button("SIMPAN DATA")
        if submit:
            if nama_petugas == "-- Pilih --" or not nama_anak or not nik:
                st.error("Lengkapi data wajib!")
            else:
                payload = {
                    "nama_petugas": nama_petugas, "nama_anak": nama_anak, "nik_anak": nik,
                    "tgl_lahir": str(tgl_lahir), "jenis_kelamin": jk, "usia_bulan": usia_bln,
                    "nama_ayah": nama_ayah, "nama_ibu": nama_ibu, "alamat": alamat,
                    "vaksin": ", ".join(vaksin)
                }
                res = requests.post(url_base, json=payload, headers=headers)
                if res.status_code in [200, 201]:
                    st.success("Data Tersimpan!")
                    st.balloons()

# --- HALAMAN 2: DASHBOARD MONITORING ---
elif menu == "Dashboard Monitoring":
    st.markdown("<h1 style='text-align:center; color:#4a148c;'>📊 Dashboard Monitoring</h1>", unsafe_allow_html=True)
    
    try:
        res = requests.get(url_base, headers=headers)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                col1, col2 = st.columns(2)
                col1.metric("Total Anak", len(df))
                col2.metric("Petugas Aktif", df['nama_petugas'].nunique() if 'nama_petugas' in df.columns else 0)
                
                st.markdown("### 📈 Grafik Kinerja")
                if 'nama_petugas' in df.columns:
                    counts = df['nama_petugas'].value_counts().reset_index()
                    counts.columns = ['Petugas', 'Jumlah']
                    fig = px.bar(counts, x='Petugas', y='Jumlah', color='Jumlah', color_continuous_scale='Purples')
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("### 📋 Tabel Data")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Data kosong.")
    except Exception as e:
        st.error(f"Error: {e}")

# --- FOOTER ---
st.markdown("<div style='text-align: center; color: #7b1fa2; font-size: 0.8rem; margin-top: 50px;'><hr>© 2026 E-Imunisasi - Dev by Riko Putra</div>", unsafe_allow_html=True)