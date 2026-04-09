import streamlit as st
import requests
import pandas as pd
from datetime import date
import base64
import os
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="E-Imunisasi 2026", layout="wide", page_icon="💉")

# --- KONEKSI DATABASE ---
url_base = "https://klvgimcpywyulayidpab.supabase.co/rest/v1/imunisasi"
api_key = "sb_publishable_gpm6D65eeBUufZYpE9aGqg_mWUG_YhC"
headers = {
    "apikey": api_key,
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# --- CSS TAMPILAN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); font-family: 'Poppins', sans-serif; }
    .header-box { text-align: center; padding: 10px; margin-bottom: 20px; }
    .judul-teks { color: #4a148c; font-weight: 800; font-size: 2.5rem; margin: 0; }
    .usia-badge { background-color: #7b1fa2; color: white; padding: 10px; border-radius: 10px; text-align: center; font-size: 1.5rem; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# --- SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown('<div class="header-box"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    user = st.text_input("Username", key="login_user")
    pwd = st.text_input("Password", type="password", key="login_pwd")
    if st.button("MASUK SISTEM", key="btn_login"):
        if user == "admin" and pwd == "imunisasi2026":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Username atau Password salah!")
    st.stop()

# --- FUNGSI RESET FORM ---
def clear_form():
    st.session_state["v_nama"] = ""
    st.session_state["v_nik"] = ""
    st.session_state["v_ayah"] = ""
    st.session_state["v_ibu"] = ""
    st.session_state["v_alamat"] = ""
    st.session_state["v_link"] = ""
    st.session_state["v_vaksin"] = []

# Navigasi
menu = st.sidebar.radio("Menu:", ["Input Data", "Dashboard", "Keluar"])
if menu == "Keluar":
    st.session_state['logged_in'] = False
    st.rerun()

# --- HALAMAN INPUT ---
if menu == "Input Data":
    st.markdown('<div class="header-box"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    
    st.markdown("### 👨‍⚕️ Data Petugas")
    nama_petugas = st.selectbox("Pilih Petugas*", [
        "-- Pilih --", "Winoto Hadi, A.Md.Kep", "Yanto Perdianta, S.Kep.Ns", "Eva Asri Deti, A.Md.Keb", 
        "Desiani, A.Md.Keb", "Dian Yuniarsih, A.Md.Keb", "Florentina Ina, A.Md.Keb", "Dayang Rafeah, A.Md.Keb", 
        "Solekah, A.Md.Keb", "Rita Epie, A.Md.Keb", "Jumini, A.Md.Keb", "Yuliana Ratih, A.Md.Keb", 
        "Esty Eva Naoumi, A.Md.Kep", "Trismiya Risva, A.Md.Keb", "Regina Susan, A.Md.Keb", 
        "Jeane Els Dame P, A.Md.Kep", "Andriyani, A.Md.Keb", "Dewi Palentek, A.Md.Kep", 
        "Riezka Dwi Andiny Sulistyaningsih, A.Md.Kep", "Bintari Dwi P, A.Md.Keb"
    ], key="sel_petugas")

    st.markdown("---")
    st.markdown("### 👶 Informasi Balita")
    c1, c2 = st.columns(2)
    with c1:
        nama_anak = st.text_input("Nama Anak*", key="v_nama")
        nik = st.text_input("NIK*", key="v_nik")
        jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True, key="v_jk")
    with c2:
        tgl_lahir = st.date_input("Tanggal Lahir", value=date.today(), key="v_tgl")
        today = date.today()
        usia_bln = (today.year - tgl_lahir.year) * 12 + today.month - tgl_lahir.month
        st.markdown("Usia Terhitung:")
        st.markdown(f'<div class="usia-badge">{usia_bln} BULAN</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 👪 Keluarga, Alamat & Dokumentasi")
    c3, c4 = st.columns(2)
    with c3:
        nama_ayah = st.text_input("Nama Ayah", key="v_ayah")
        nama_ibu = st.text_input("Nama Ibu", key="v_ibu")
    with c4:
        alamat = st.text_area("Alamat Lengkap", key="v_alamat")
        link_dok = st.text_input("🔗 Link Google Drive Foto (Dokumentasi)", placeholder="Paste link di sini...", key="v_link")

    st.markdown("---")
    st.markdown("### 💉 Jenis Vaksin")
    daftar_vaksin = [
        "HB O Inject", "BCG", "Polio 1", "DPT / HIB 1", "Polio 2", "Rotavirus 1", 
        "DPT / HIB 2", "Polio 3", "Rotavirus 2", "DPT / HIB 3", "Polio 4", 
        "Rotavirus 3", "IPV 1", "IPV 2", "Campak 9 bulan", "DPT Lanjutan", 
        "Campak Lanjutan", "PCV 1", "PCV 2", "PCV 3", "JE", "TT CATIN", 
        "TT 1 BUMIL", "TT 2 BUMIL", "TT 3 BUMIL", "TT 4 BUMIL", "TT 5 BUMIL"
    ]
    vaksin_pilihan = st.multiselect("Vaksin*", daftar_vaksin, key="v_vaksin")

    if st.button("SIMPAN DATA SEKARANG", use_container_width=True, key="btn_simpan"):
        if nama_petugas == "-- Pilih --" or not nama_anak or not nik:
            st.error("Data petugas, nama anak, dan NIK harus diisi!")
        else:
            payload = {
                "nama_petugas": nama_petugas, "nama_anak": nama_anak, "nik_anak": nik,
                "tgl_lahir": str(tgl_lahir), "jenis_kelamin": jk, "usia_bulan": usia_bln,
                "nama_ayah": nama_ayah, "nama_ibu": nama_ibu, "alamat": alamat,
                "link_dokumentasi": link_dok, "vaksin": ", ".join(vaksin_pilihan)
            }
            res = requests.post(url_base, json=payload, headers=headers)
            if res.status_code in [200, 201]:
                st.success(f"Berhasil simpan data {nama_anak}!")
                st.balloons()
                clear_form() # Kosongkan data
                st.rerun()

# --- HALAMAN DASHBOARD ---
elif menu == "Dashboard":
    st.markdown("<h1 style='text-align:center;'>📊 Dashboard Monitoring</h1>", unsafe_allow_html=True)
    res = requests.get(url_base, headers=headers)
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        if not df.empty:
            st.metric("Total Anak Terdata", len(df))
            
            # Grafik Horizontal agar nama tidak miring
            counts = df['nama_petugas'].value_counts().reset_index()
            counts.columns = ['Petugas', 'Jumlah']
            fig = px.bar(counts, x='Jumlah', y='Petugas', orientation='h', text='Jumlah', 
                         color='Jumlah', color_continuous_scale='Purples')
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=150))
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabel dengan link yang bisa diklik
            st.markdown("### 📋 Data Lengkap")
            st.dataframe(df, use_container_width=True)
