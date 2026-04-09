import streamlit as st
import requests
from datetime import date
import base64
import os

# --- DATA KONEKSI (Tetap Sama) ---
url_base = "https://klvgimcpywyulayidpab.supabase.co/rest/v1/imunisasi"
api_key = "sb_publishable_gpm6D65eeBUufZYpE9aGqg_mWUG_YhC"

headers = {
    "apikey": api_key,
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

st.set_page_config(page_title="E-Imunisasi 2026", layout="centered", page_icon="💉")

# --- FUNGSI UNTUK MEMBACA GAMBAR PNG (TRANSPARAN) LOKAL ---
def get_base64_png(file_name):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, file_name)
    
    # Pastikan file ada dan ekstensinya .png (untuk transparansi)
    if os.path.exists(file_path) and file_name.lower().endswith('.png'):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- NAMA FILE GAMBAR SPESIFIK (Pastikan file ini ada di folder) ---
# Saya sudah mengubah namanya sesuai permintaan Mas Riko
nama_file_logo = "istockphoto-1323619822-612x612.png" 
img_data = get_base64_png(nama_file_logo)

# --- CSS (TAMPILAN MODERN DENGAN LOGO PNG TRANSPARAN) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

    /* Background Utama */
    .stApp {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        font-family: 'Poppins', sans-serif;
    }

    /* Kotak Form Utama */
    div[data-testid="stForm"] {
        background-color: white;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(106, 27, 154, 0.1);
        border: 1px solid #f3e5f5;
    }

    /* Container Header (Bersampingan) */
    .header-box {
        display: flex;
        align-items: center; /* Sejajarkan Vertikal Presisi */
        justify-content: center; /* Rata Tengah Horizontal Presisi */
        gap: 15px; /* Jarak antara Logo PNG dan Teks */
        margin-bottom: 5px;
        margin-top: 10px;
    }

    /* Styling Gambar Logo PNG */
    .logo-img {
        height: 65px; /* Sedikit lebih besar dari huruf 'E' judul */
        width: auto;
        border: none;
        box-shadow: none;
        object-fit: contain; /* Jaga proporsi */
        background-color: transparent !important; /* Memastikan background transparan */
    }

    /* Font Judul Utama Poppins Modern */
    .judul-teks {
        color: #4a148c; /* Ungu Tua */
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 3.5rem; /* Ukuran teks judul */
        margin: 0;
        letter-spacing: -1.5px;
    }

    /* Font Sub-Judul */
    .sub-judul {
        color: #7b1fa2; /* Ungu Sedang */
        text-align: center;
        font-size: 1.1rem;
        margin-top: -10px;
        margin-bottom: 30px;
    }

    /* Styling Header Bagian Form */
    h3 {
        color: #6a1b9a; /* Ungu */
        font-weight: 600;
        border-bottom: 2px solid #e1bee7;
        padding-bottom: 5px;
    }

    /* Styling Tombol Simpan (Ungu Modern) */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.8em;
        background: linear-gradient(45deg, #7b1fa2, #9c27b0);
        color: white;
        font-weight: 600;
        border: none;
    }
    
    /* Memastikan label input terlihat jelas */
    .stTextInput>label, .stSelectbox>label, .stDateInput>label, .stRadio>label, .stTextArea>label, .stMultiSelect>label {
        color: #4a148c !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- TAMPILAN HEADER (LOGO & JUDUL BERSAMPINGAN) ---
if img_data:
    # Kita gunakan container CSS '.header-box' untuk menengahkan seluruh elemen
    # Logo di kiri, Judul di kanan, diletakkan presisi di tengah layar
    st.markdown(f"""
    <div class="header-box">
        <img src="data:image/png;base64,{img_data}" class="logo-img" alt="Logo E-Imunisasi Centang">
        <h1 class="judul-teks">E-IMUNISASI</h1>
    </div>
    <p class="sub-judul">Sistem Pencatatan Imunisasi Digital Terpadu</p>
    """, unsafe_allow_html=True)
else:
    # Jika gambar gagal dimuat (file tidak ditemukan di folder)
    st.markdown("<h1 style='text-align:center;' class='judul-teks'>E-IMUNISASI</h1>", unsafe_allow_html=True)
    st.warning(f"File logo transparan '{nama_file_logo}' (PNG) tidak ditemukan di folder aplikasi.")

# --- DATA MASTER (Tetap Sama) ---
daftar_petugas = [
    "-- Pilih Nama Petugas --",
    "Winoto Hadi, A.Md.Kep", "Yanto Perdianta, S.Kep.Ns", "Eva Asri Deti, A.Md.Keb",
    "Desiani, A.Md.Keb", "Dian Yuniarsih, A.Md.Keb", "Florentina Ina, A.Md.Keb",
    "Dayang Rafeah, A.Md.Keb", "Solekah, A.Md.Keb", "Rita Epie, A.Md.Keb",
    "Jumini, A.Md.Keb", "Yuliana Ratih, A.Md.Keb", "Esty Eva Naoumi, A.Md.Kep",
    "Trismiya Risva, A.Md.Keb", "Regina Susan, A.Md.Keb", "Jeane Els Dame P, A.Md.Kep",
    "Andriyani, A.Md.Keb", "Dewi Palentek, A.Md.Kep", 
    "Riezka Dwi Andiny Sulistyaningsih, A.Md.Kep", "Bintari Dwi P, A.Md.Keb"
]

daftar_vaksin = [
    "HB O Inject", "BCG", "Polio 1", "DPT / HIB 1", "Polio 2", "Rotavirus 1", 
    "DPT / HIB 2", "Polio 3", "Rotavirus 2", "DPT / HIB 3", "Polio 4", 
    "Rotavirus 3", "IPV 1", "IPV 2", "Campak 9 bulan", "DPT Lanjutan", 
    "Campak Lanjutan", "PCV 1", "PCV 2", "PCV 3", "JE", "TT CATIN", 
    "TT 1 BUMIL", "TT 2 BUMIL", "TT 3 BUMIL", "TT 4 BUMIL", "TT 5 BUMIL"
]

# --- FORM INPUT (Tetap Sama) ---
with st.form("main_form", clear_on_submit=True):
    st.markdown("### 👨‍⚕️ Petugas Pelaksana")
    nama_petugas = st.selectbox("Nama Petugas Bertugas*", daftar_petugas)
    
    st.markdown("### 👶 Informasi Anak")
    c1, c2 = st.columns(2)
    with c1:
        nama = st.text_input("Nama Lengkap Anak*")
        nik = st.text_input("NIK Anak*")
    with c2:
        tgl_lahir = st.date_input("Tanggal Lahir")
        jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True)

    today = date.today()
    usia_bulan = (today.year - tgl_lahir.year) * 12 + today.month - tgl_lahir.month
    st.info(f"Usia saat ini: **{usia_bulan} Bulan**")
    
    st.markdown("### 👪 Orang Tua & Alamat")
    c3, c4 = st.columns(2)
    with c3:
        nama_ayah = st.text_input("Nama Ayah")
        nama_ibu = st.text_input("Nama Ibu")
    with c4:
        alamat = st.text_area("Alamat Lengkap Domisili")

    st.markdown("### 💉 Tindakan Medik")
    vaksin_dipilih = st.multiselect("Vaksin*", daftar_vaksin)

    submit = st.form_submit_button("SIMPAN INPUTAN")

    if submit:
        # Validasi (Tetap Sama)
        if nama_petugas == "-- Pilih Nama Petugas --" or not nama or not nik:
            st.error("❌ Mohon lengkapi data wajib (*)")
        else:
            payload = {
                "nama_petugas": nama_petugas, "nama_anak": nama, "nik_anak": nik,
                "tgl_lahir": str(tgl_lahir), "usia_bulan": usia_bulan,
                "jenis_kelamin": jk, "nama_ayah": nama_ayah, "nama_ibu": nama_ibu,
                "alamat": alamat, "vaksin": ", ".join(vaksin_dipilih)
            }
            try:
                response = requests.post(url_base, json=payload, headers=headers)
                if response.status_code in [200, 201]:
                    st.balloons()
                    st.success("✅ Data berhasil diverifikasi dan disimpan!")
            except:
                st.error("❌ Terjadi kesalahan koneksi.")

# --- FOOTER ---
st.markdown("""
<div style="text-align: center; color: #7b1fa2; font-size: 0.85rem; margin-top: 30px;">
    <hr style="border-top: 1px solid #e1bee7;">
    © 2026 Aplikasi E-Imunisasi Digital - Dev by Riko Putra
</div>
""", unsafe_allow_html=True)