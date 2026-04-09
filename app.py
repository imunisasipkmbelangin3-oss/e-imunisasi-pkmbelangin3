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

# --- CSS TAMPILAN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); font-family: 'Poppins', sans-serif; }
    .header-box { display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 20px; }
    .judul-teks { color: #4a148c; font-weight: 800; font-size: 3rem; margin: 0; }
    .kartu-putih { background-color: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
    .usia-output { background-color: #7b1fa2; color: white; padding: 15px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# --- SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown('<div class="header-box"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    with st.container():
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("MASUK"):
            if user == "admin" and pwd == "imunisasi2026":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Username atau Password salah!")
    st.stop()

# --- NAVIGASI ---
menu = st.sidebar.radio("Menu:", ["Input Data", "Dashboard", "Keluar"])
if menu == "Keluar":
    st.session_state['logged_in'] = False
    st.rerun()

# --- HALAMAN INPUT ---
if menu == "Input Data":
    st.markdown('<div class="header-box"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    
    # Bagian Input Tanpa Kotak Putih yang Mengganggu
    st.markdown("### 👨‍⚕️ Petugas Pelaksana")
    nama_petugas = st.selectbox("Pilih Petugas*", ["-- Pilih --", "Winoto Hadi, A.Md.Kep", "Yanto Perdianta, S.Kep.Ns", "Eva Asri Deti, A.Md.Keb", "Desiani, A.Md.Keb", "Dian Yuniarsih, A.Md.Keb"])
    
    st.markdown("---")
    st.markdown("### 👶 Informasi Anak")
    
    c1, c2 = st.columns(2)
    with c1:
        nama_anak = st.text_input("Nama Anak*")
        nik = st.text_input("NIK Anak*")
        jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True)
    
    with c2:
        # PERBAIKAN: Tanggal lahir diletakkan di luar form agar reaktif
        tgl_lahir = st.date_input("Tanggal Lahir", value=date.today(), key="tgl_lahir_input")
        
        # HITUNG USIA SECARA LANGSUNG
        today = date.today()
        total_bulan = (today.year - tgl_lahir.year) * 12 + today.month - tgl_lahir.month
        
        # Tampilkan Hasil Hitungan
        st.markdown(f'<div class="usia-output">{total_bulan} BULAN</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 👪 Orang Tua & Alamat")
    nama_ayah = st.text_input("Nama Ayah")
    nama_ibu = st.text_input("Nama Ibu")
    alamat = st.text_area("Alamat Lengkap")

    st.markdown("---")
    st.markdown("### 💉 Tindakan Vaksin")
    daftar_vaksin = ["HB O Inject", "BCG", "Polio 1", "DPT 1", "Polio 2", "Rotavirus 1", "DPT 2", "Polio 3", "Campak", "PCV 1"]
    vaksin_pilihan = st.multiselect("Vaksin yang Diberikan*", daftar_vaksin)

    if st.button("SIMPAN DATA", use_container_width=True):
        if nama_petugas == "-- Pilih --" or not nama_anak or not nik:
            st.error("Data wajib belum lengkap!")
        else:
            payload = {
                "nama_petugas": nama_petugas, "nama_anak": nama_anak, "nik_anak": nik,
                "tgl_lahir": str(tgl_lahir), "jenis_kelamin": jk, "usia_bulan": total_bulan,
                "nama_ayah": nama_ayah, "nama_ibu": nama_ibu, "alamat": alamat,
                "vaksin": ", ".join(vaksin_pilihan)
            }
            res = requests.post(url_base, json=payload, headers=headers)
            if res.status_code in [200, 201]:
                st.success(f"Berhasil simpan data {nama_anak}!")
                st.balloons()

# --- HALAMAN DASHBOARD ---
elif menu == "Dashboard":
    st.markdown("<h1 style='text-align:center;'>📊 Monitoring</h1>", unsafe_allow_html=True)
    res = requests.get(url_base, headers=headers)
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        if not df.empty:
            st.metric("Total Terdata", len(df))
            fig = px.bar(df['nama_petugas'].value_counts().reset_index(), x='index', y='nama_petugas', color='nama_petugas', title="Capaian Petugas")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df, use_container_width=True)
