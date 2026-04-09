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

# --- INITIALIZE SESSION STATE (UNTUK PENGUNCI DATA) ---
# Link ini akan selalu muncul otomatis
LINK_PERMANEN = "https://drive.google.com/drive/folders/1X4Og0psVrv-8q2Y-pyi170XdAd4XhoHw?usp=drive_link"

if 'v_link' not in st.session_state:
    st.session_state['v_link'] = LINK_PERMANEN

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

# --- FUNGSI RESET FORM (Tanpa menghapus link permanen) ---
def clear_form():
    st.session_state["v_nama"] = ""
    st.session_state["v_nik"] = ""
    st.session_state["v_ayah"] = ""
    st.session_state["v_ibu"] = ""
    st.session_state["v_alamat"] = ""
    # Link tidak dikosongkan agar tetap ada untuk input selanjutnya
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
        st.text_input("Nama Anak*", key="v_nama")
        st.text_input("NIK*", key="v_nik")
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
        st.text_input("Nama Ayah", key="v_ayah")
        st.text_input("Nama Ibu", key="v_ibu")
    with c4:
        st.text_area("Alamat Lengkap", key="v_alamat")
        # KOLOM LINK SEKARANG MENGAMBIL DATA DARI SESSION STATE PERMANEN
        st.text_input("🔗 Link Google Drive Dokumentasi", key="v_link")

    st.markdown("---")
    st.markdown("### 💉 Jenis Vaksin")
    daftar_vaksin = [
        "HB O Inject", "BCG", "Polio 1", "DPT / HIB 1", "Polio 2", "Rotavirus 1", 
        "DPT / HIB 2", "Polio 3", "Rotavirus 2", "DPT / HIB 3", "Polio 4", 
        "Rotavirus 3", "IPV 1", "IPV 2", "Campak 9 bulan", "DPT Lanjutan", 
        "Campak Lanjutan", "PCV 1", "PCV 2", "PCV 3", "JE", "TT CATIN", 
        "TT 1 BUMIL", "TT 2 BUMIL", "TT 3 BUMIL", "TT 4 BUMIL", "TT 5 BUMIL"
    ]
    st.multiselect("Vaksin*", daftar_vaksin, key="v_vaksin")

    if st.button("SIMPAN DATA SEKARANG", use_container_width=True, key="btn_simpan"):
        if nama_petugas == "-- Pilih --" or not st.session_state.v_nama or not st.session_state.v_nik:
            st.error("Data petugas, nama anak, dan NIK harus diisi!")
        else:
            payload = {
                "nama_petugas": nama_petugas, 
                "nama_anak": st.session_state.v_nama, 
                "nik_anak": st.session_state.v_nik,
                "tgl_lahir": str(tgl_lahir), 
                "jenis_kelamin": jk, 
                "usia_bulan": usia_bln,
                "nama_ayah": st.session_state.v_ayah, 
                "nama_ibu": st.session_state.v_ibu, 
                "alamat": st.session_state.v_alamat,
                "link_dokumentasi": st.session_state.v_link, 
                "vaksin": ", ".join(st.session_state.v_vaksin)
            }
            res = requests.post(url_base, json=payload, headers=headers)
            if res.status_code in [200, 201]:
                st.success(f"Berhasil simpan data {st.session_state.v_nama}!")
                st.balloons()
                clear_form()
                st.rerun()

# --- HALAMAN DASHBOARD (VERSI DETEKSI LINK OTOMATIS) ---
elif menu == "Dashboard":
    st.markdown("<h1 style='text-align:center; color:#4a148c;'>📊 Dashboard Monitoring</h1>", unsafe_allow_html=True)
    
    res = requests.get(url_base, headers=headers)
    if res.status_code == 200:
        data_json = res.json()
        if data_json:
            df = pd.DataFrame(data_json)
            
            # --- Metrics ---
            st.metric("Total Anak Terdata", len(df))
            
            # --- Grafik ---
            kp = 'nama_petugas' if 'nama_petugas' in df.columns else df.columns[0]
            counts = df[kp].value_counts().reset_index()
            counts.columns = ['Petugas', 'Jumlah']
            fig = px.bar(counts, x='Jumlah', y='Petugas', orientation='h', text='Jumlah', color='Jumlah', color_continuous_scale='Purples')
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=150))
            st.plotly_chart(fig, use_container_width=True)
            
            # --- TABEL DENGAN DETEKSI KOLOM LINK ---
            st.markdown("### 📋 Data Lengkap (Klik Link untuk Lihat Foto)")
            
            # Mencari kolom mana yang mengandung kata 'link' atau 'dok'
            kolom_link = [c for c in df.columns if 'link' in c.lower() or 'dok' in c.lower()]
            
            config_kolom = {}
            for col in kolom_link:
                config_kolom[col] = st.column_config.LinkColumn(
                    "Link Dokumentasi",
                    display_text="Buka Foto/Drive"
                )
            
            st.dataframe(
                df, 
                use_container_width=True,
                column_config=config_kolom # Menggunakan konfigurasi yang sudah dideteksi
            )
            
        else:
            st.info("Belum ada data.")

# --- FOOTER ---
st.markdown("<div style='text-align: center; color: #7b1fa2; font-size: 0.8rem; margin-top: 50px;'><hr>© 2026 E-Imunisasi - Dev by Riko Putra</div>", unsafe_allow_html=True)
