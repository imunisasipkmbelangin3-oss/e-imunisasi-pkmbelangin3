import streamlit as st
import requests
import pandas as pd
from datetime import date
import base64
import os
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="E-Imunisasi 2026", layout="centered", page_icon="💉")

# --- KONEKSI DATABASE ---
url_base = "https://klvgimcpywyulayidpab.supabase.co/rest/v1/imunisasi"
api_key = "sb_publishable_gpm6D65eeBUufZYpE9aGqg_mWUG_YhC"
headers = {
    "apikey": api_key,
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# --- FUNGSI LOGO ---
def get_base64_png(file_name):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

img_data = get_base64_png("istockphoto-1323619822-612x612.png")

# --- CSS TAMPILAN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); font-family: 'Poppins', sans-serif; }
    .header-box { display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 25px; }
    .judul-teks { color: #4a148c; font-weight: 800; font-size: 3rem; margin: 0; }
    .usia-badge { background-color: #7b1fa2; color: white; padding: 15px; border-radius: 12px; text-align: center; font-size: 1.6rem; font-weight: 800; margin-top: 10px; box-shadow: 0 4px 15px rgba(123, 31, 162, 0.3); }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background: linear-gradient(45deg, #7b1fa2, #9c27b0); color: white; font-weight: 600; border: none; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# --- SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    if img_data:
        st.markdown(f'<div class="header-box"><img src="data:image/png;base64,{img_data}" height="70"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="header-box"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    
    with st.container():
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("MASUK SISTEM"):
            if user == "admin" and pwd == "imunisasi2026":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Username atau Password salah!")
    st.stop()

# --- NAVIGASI ---
menu = st.sidebar.radio("Navigasi Halaman:", ["Input Data Baru", "Dashboard Monitoring", "Keluar"])
if menu == "Keluar":
    st.session_state['logged_in'] = False
    st.rerun()

# --- HALAMAN INPUT ---
if menu == "Input Data Baru":
    if img_data:
        st.markdown(f'<div class="header-box"><img src="data:image/png;base64,{img_data}" height="60"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    
    st.markdown("### 👨‍⚕️ Petugas Pelaksana")
    daftar_petugas = [
        "-- Pilih Nama Petugas --", "Winoto Hadi, A.Md.Kep", "Yanto Perdianta, S.Kep.Ns", 
        "Eva Asri Deti, A.Md.Keb", "Desiani, A.Md.Keb", "Dian Yuniarsih, A.Md.Keb", 
        "Florentina Ina, A.Md.Keb", "Dayang Rafeah, A.Md.Keb", "Solekah, A.Md.Keb", 
        "Rita Epie, A.Md.Keb", "Jumini, A.Md.Keb", "Yuliana Ratih, A.Md.Keb", 
        "Esty Eva Naoumi, A.Md.Kep", "Trismiya Risva, A.Md.Keb", "Regina Susan, A.Md.Keb", 
        "Jeane Els Dame P, A.Md.Kep", "Andriyani, A.Md.Keb", "Dewi Palentek, A.Md.Kep", 
        "Riezka Dwi Andiny Sulistyaningsih, A.Md.Kep", "Bintari Dwi P, A.Md.Keb"
    ]
    nama_petugas = st.selectbox("Nama Petugas Bertugas*", daftar_petugas)
    
    st.markdown("---")
    st.markdown("### 👶 Informasi Anak")
    col_a, col_b = st.columns(2)
    with col_a:
        nama_anak = st.text_input("Nama Lengkap Anak*")
        nik = st.text_input("NIK Anak*")
        jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True)
    
    with col_b:
        tgl_lahir = st.date_input("Tanggal Lahir", value=date.today())
        # HITUNG BULAN OTOMATIS (REAKTIF)
        today = date.today()
        total_bulan = (today.year - tgl_lahir.year) * 12 + today.month - tgl_lahir.month
        st.markdown(f'<div class="usia-badge">{total_bulan} BULAN</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 👪 Orang Tua & Alamat")
    c1, c2 = st.columns(2)
    with c1:
        nama_ayah = st.text_input("Nama Ayah")
        nama_ibu = st.text_input("Nama Ibu")
    with c2:
        alamat = st.text_area("Alamat Lengkap")

    st.markdown("---")
    st.markdown("### 💉 Tindakan Medik (Vaksin)")
    # DAFTAR VAKSIN LENGKAP KEMBALI
    semua_vaksin = [
        "HB O Inject", "BCG", "Polio 1", "DPT / HIB 1", "Polio 2", "Rotavirus 1", 
        "DPT / HIB 2", "Polio 3", "Rotavirus 2", "DPT / HIB 3", "Polio 4", 
        "Rotavirus 3", "IPV 1", "IPV 2", "Campak 9 bulan", "DPT Lanjutan", 
        "Campak Lanjutan", "PCV 1", "PCV 2", "PCV 3", "JE", "TT CATIN", 
        "TT 1 BUMIL", "TT 2 BUMIL", "TT 3 BUMIL", "TT 4 BUMIL", "TT 5 BUMIL"
    ]
    vaksin_dipilih = st.multiselect("Pilih Vaksin yang Diberikan*", semua_vaksin)

    if st.button("SIMPAN DATA IMUNISASI"):
        if nama_petugas == "-- Pilih Nama Petugas --" or not nama_anak or not nik:
            st.error("❌ Nama Petugas, Nama Anak, dan NIK tidak boleh kosong!")
        else:
            payload = {
                "nama_petugas": nama_petugas, "nama_anak": nama_anak, "nik_anak": nik,
                "tgl_lahir": str(tgl_lahir), "jenis_kelamin": jk, "usia_bulan": total_bulan,
                "nama_ayah": nama_ayah, "nama_ibu": nama_ibu, "alamat": alamat,
                "vaksin": ", ".join(vaksin_dipilih)
            }
            try:
                res = requests.post(url_base, json=payload, headers=headers)
                if res.status_code in [200, 201]:
                    st.success(f"✅ Berhasil! Data {nama_anak} ({total_bulan} bln) telah masuk database.")
                    st.balloons()
                else:
                    st.error(f"Gagal simpan: {res.text}")
            except Exception as e:
                st.error(f"Koneksi terganggu: {e}")

# --- HALAMAN DASHBOARD ---
elif menu == "Dashboard Monitoring":
    st.markdown("<h1 style='text-align:center; color:#4a148c;'>📊 Monitoring Capaian</h1>", unsafe_allow_html=True)
    res = requests.get(url_base, headers=headers)
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        if not df.empty:
            st.metric("Total Anak Terdata", len(df))
            counts = df['nama_petugas'].value_counts().reset_index()
            counts.columns = ['Petugas', 'Jumlah']
            fig = px.bar(counts, x='Petugas', y='Jumlah', color='Jumlah', color_continuous_scale='Purples', text='Jumlah')
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("### 📋 Detail Data")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Belum ada data.")

st.markdown("<div style='text-align: center; color: #7b1fa2; font-size: 0.8rem; margin-top: 50px;'><hr>© 2026 E-Imunisasi Digital - Dev by Riko Putra</div>", unsafe_allow_html=True)
