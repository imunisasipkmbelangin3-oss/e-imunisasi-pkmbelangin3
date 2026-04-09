import streamlit as st
import requests
import pandas as pd
from datetime import date
import base64
import os

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
    .header-box { text-align: center; margin-bottom: 20px; }
    .judul-teks { color: #4a148c; font-weight: 800; font-size: 2.5rem; margin: 0; }
    .usia-badge { background-color: #7b1fa2; color: white; padding: 10px; border-radius: 10px; text-align: center; font-size: 1.5rem; font-weight: 800; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background: #7b1fa2; color: white; font-weight: 600; border: none; }
</style>
""", unsafe_allow_html=True)

# --- KONFIGURASI LINK PERMANEN ---
LINK_DRIVE = "https://drive.google.com/drive/folders/1X4Og0psVrv-8q2Y-pyi170XdAd4XhoHw?usp=drive_link"

# --- SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown('<div class="header-box"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("MASUK SISTEM"):
        if user == "admin" and pwd == "imunisasi2026":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Username atau Password salah!")
    st.stop()

# --- FUNGSI RESET DATA ---
def reset_form():
    st.session_state.nama_anak = ""
    st.session_state.nik = ""
    st.session_state.ayah = ""
    st.session_state.ibu = ""
    st.session_state.alamat = ""
    st.session_state.vaksin = []

# Inisialisasi State
if 'nama_anak' not in st.session_state: reset_form()

# Navigasi Sidebar
menu = st.sidebar.radio("Menu:", ["Input Data", "Dashboard", "Keluar"])
if menu == "Keluar":
    st.session_state['logged_in'] = False
    st.rerun()

# --- HALAMAN INPUT DATA ---
if menu == "Input Data":
    st.markdown('<div class="header-box"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    
    # Bagian Petugas
    nama_petugas = st.selectbox("Pilih Petugas*", [
        "-- Pilih --", "Winoto Hadi, A.Md.Kep", "Yanto Perdianta, S.Kep.Ns", "Eva Asri Deti, A.Md.Keb", 
        "Desiani, A.Md.Keb", "Dian Yuniarsih, A.Md.Keb", "Florentina Ina, A.Md.Keb", "Dayang Rafeah, A.Md.Keb", 
        "Solekah, A.Md.Keb", "Rita Epie, A.Md.Keb", "Jumini, A.Md.Keb", "Yuliana Ratih, A.Md.Keb", 
        "Esty Eva Naoumi, A.Md.Kep", "Trismiya Risva, A.Md.Keb", "Regina Susan, A.Md.Keb", 
        "Jeane Els Dame P, A.Md.Kep", "Andriyani, A.Md.Keb", "Dewi Palentek, A.Md.Kep", 
        "Riezka Dwi Andiny Sulistyaningsih, A.Md.Kep", "Bintari Dwi P, A.Md.Keb"
    ])

    st.markdown("---")
    st.markdown("### 👶 Data Anak")
    c1, c2 = st.columns(2)
    with c1:
        n_anak = st.text_input("Nama Lengkap Anak*", key="nama_anak")
        n_nik = st.text_input("NIK Anak*", key="nik")
        n_jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True)
    with c2:
        tgl_lhr = st.date_input("Tanggal Lahir", value=date.today())
        # Hitung Bulan Otomatis
        today = date.today()
        bln = (today.year - tgl_lhr.year) * 12 + today.month - tgl_lhr.month
        st.markdown(f'<div class="usia-badge">{bln} BULAN</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 👪 Keluarga & Alamat")
    c3, c4 = st.columns(2)
    with c3:
        n_ayah = st.text_input("Nama Ayah", key="ayah")
        n_ibu = st.text_input("Nama Ibu", key="ibu")
    with c4:
        n_alamat = st.text_area("Alamat Lengkap", key="alamat")

    st.markdown("---")
    st.markdown("### 💉 Vaksin & Dokumentasi")
    # Link Google Drive Tetap Berada di Inputan (Permanen)
    st.info(f"📂 **Dokumentasi Kegiatan:** Folder Google Drive sudah terpasang.")
    st.link_button("KLIK DISINI UNTUK UPLOAD FOTO", LINK_DRIVE, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    vaksins = ["HB O Inject", "BCG", "Polio 1", "DPT / HIB 1", "Polio 2", "Rotavirus 1", "DPT / HIB 2", "Polio 3", "Rotavirus 2", "DPT / HIB 3", "Polio 4", "Rotavirus 3", "IPV 1", "IPV 2", "Campak 9 bulan", "DPT Lanjutan", "Campak Lanjutan", "PCV 1", "PCV 2", "PCV 3", "JE", "TT CATIN", "TT 1 BUMIL", "TT 2 BUMIL", "TT 3 BUMIL", "TT 4 BUMIL", "TT 5 BUMIL"]
    n_vaksin = st.multiselect("Pilih Vaksin*", vaksins, key="vaksin")

    if st.button("SIMPAN DATA IMUNISASI"):
        if nama_petugas == "-- Pilih --" or not n_anak or not n_nik:
            st.error("Mohon lengkapi Nama Petugas, Nama Anak, dan NIK!")
        else:
            payload = {
                "nama_petugas": nama_petugas, "nama_anak": n_anak, "nik_anak": n_nik,
                "tgl_lahir": str(tgl_lhr), "jenis_kelamin": n_jk, "usia_bulan": bln,
                "nama_ayah": n_ayah, "nama_ibu": n_ibu, "alamat": n_alamat,
                "link_dokumentasi": LINK_DRIVE, "vaksin": ", ".join(n_vaksin)
            }
            res = requests.post(url_base, json=payload, headers=headers)
            if res.status_code in [200, 201]:
                st.success(f"✅ Data {n_anak} Berhasil Disimpan!")
                st.balloons()
                reset_form()
                st.rerun()

# --- HALAMAN DASHBOARD ---
elif menu == "Dashboard":
    st.markdown("<h1 style='text-align:center;'>📊 Dashboard</h1>", unsafe_allow_html=True)
    res = requests.get(url_base, headers=headers)
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
# --- FOOTER ---
st.markdown("<div style='text-align: center; color: #7b1fa2; font-size: 0.8rem; margin-top: 50px;'><hr>© 2026 E-Imunisasi - Dev by Riko Putra</div>", unsafe_allow_html=True)
