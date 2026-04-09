import streamlit as st
import requests
import pandas as pd
from datetime import date
import plotly.express as px

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="E-Imunisasi 2026", layout="wide", page_icon="💉")

# --- 2. KONEKSI DATABASE ---
url_base = "https://klvgimcpywyulayidpab.supabase.co/rest/v1/imunisasi"
api_key = "sb_publishable_gpm6D65eeBUufZYpE9aGqg_mWUG_YhC"
headers = {
    "apikey": api_key,
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# --- 3. CSS TAMPILAN PROFESIONAL ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); font-family: 'Poppins', sans-serif; }
    .header-box { text-align: center; margin-bottom: 30px; }
    .judul-teks { color: #4a148c; font-weight: 800; font-size: 2.8rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
    .usia-badge { background-color: #7b1fa2; color: white; padding: 12px; border-radius: 10px; text-align: center; font-size: 1.6rem; font-weight: 800; }
    .stMetric { background: white; padding: 15px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

# --- 4. DATA STATIC & SESSION STATE ---
LINK_DRIVE = "https://drive.google.com/drive/folders/1X4Og0psVrv-8q2Y-pyi170XdAd4XhoHw?usp=drive_link"

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

# --- 5. SISTEM LOGIN ---
if not st.session_state['logged_in']:
    st.markdown('<div class="header-box"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            if st.button("MASUK SISTEM", use_container_width=True):
                if user == "admin" and pwd == "imunisasi2026":
                    st.session_state['logged_in'] = True
                    st.rerun()
                else: st.error("Username atau Password salah!")
    st.stop()

# --- 6. FUNGSI RESET ---
def reset_form():
    for key in ["nama_anak", "nik", "ayah", "ibu", "alamat", "vaksin"]:
        st.session_state[key] = "" if key != "vaksin" else []

# Navigasi Sidebar
menu = st.sidebar.radio("Navigasi Menu:", ["Input Data", "Dashboard", "Keluar"])
if menu == "Keluar":
    st.session_state['logged_in'] = False
    st.rerun()

# --- 7. HALAMAN INPUT DATA ---
if menu == "Input Data":
    st.markdown('<div class="header-box"><h1 class="judul-teks">E-IMUNISASI</h1><p>Sistem Pendataan Imunisasi Digital 2026</p></div>', unsafe_allow_html=True)
    
    nama_petugas = st.selectbox("Pilih Petugas Medis*", [
        "-- Pilih --", "Winoto Hadi, A.Md.Kep", "Yanto Perdianta, S.Kep.Ns", "Eva Asri Deti, A.Md.Keb", 
        "Desiani, A.Md.Keb", "Dian Yuniarsih, A.Md.Keb", "Florentina Ina, A.Md.Keb", "Dayang Rafeah, A.Md.Keb", 
        "Solekah, A.Md.Keb", "Rita Epie, A.Md.Keb", "Jumini, A.Md.Keb", "Yuliana Ratih, A.Md.Keb", 
        "Esty Eva Naoumi, A.Md.Kep", "Trismiya Risva, A.Md.Keb", "Regina Susan, A.Md.Keb", 
        "Jeane Els Dame P, A.Md.Kep", "Andriyani, A.Md.Keb", "Dewi Palentek, A.Md.Kep", 
        "Riezka Dwi Andiny Sulistyaningsih, A.Md.Kep", "Bintari Dwi P, A.Md.Keb"
    ])

    st.markdown("### 👶 Identitas Anak & Orang Tua")
    c1, c2 = st.columns(2)
    with c1:
        n_anak = st.text_input("Nama Lengkap Anak*", key="nama_anak")
        n_nik = st.text_input("NIK Anak*", key="nik")
        tgl_lhr = st.date_input("Tanggal Lahir", value=date.today())
        today = date.today()
        bln = (today.year - tgl_lhr.year) * 12 + today.month - tgl_lhr.month
        st.markdown(f'<div class="usia-badge">{bln} BULAN</div>', unsafe_allow_html=True)
    with c2:
        n_jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True)
        n_ayah = st.text_input("Nama Ayah", key="ayah")
        n_ibu = st.text_input("Nama Ibu", key="ibu")

    st.markdown("### 🏠 Alamat & Dokumentasi")
    n_alamat = st.text_area("Alamat Lengkap", key="alamat")
    st.info(f"📂 **Dokumentasi:** Gunakan link di bawah untuk unggah foto ke Google Drive.")
    st.link_button("🚀 BUKA GOOGLE DRIVE (UPLOAD FOTO)", LINK_DRIVE, use_container_width=True)
    
    st.markdown("### 💉 Layanan Vaksin")
    vaksins = ["HB O Inject", "BCG", "Polio 1", "DPT / HIB 1", "Polio 2", "Rotavirus 1", "DPT / HIB 2", "Polio 3", "Rotavirus 2", "DPT / HIB 3", "Polio 4", "Rotavirus 3", "IPV 1", "IPV 2", "Campak 9 bulan", "DPT Lanjutan", "Campak Lanjutan", "PCV 1", "PCV 2", "PCV 3", "JE", "TT CATIN", "TT 1 BUMIL", "TT 2 BUMIL", "TT 3 BUMIL", "TT 4 BUMIL", "TT 5 BUMIL"]
    n_vaksin = st.multiselect("Pilih Jenis Vaksin*", vaksins, key="vaksin")

    if st.button("💾 SIMPAN DATA KE DATABASE", use_container_width=True):
        if nama_petugas == "-- Pilih --" or not n_anak or not n_nik:
            st.warning("⚠️ Mohon lengkapi Nama Petugas, Nama Anak, dan NIK!")
        else:
            payload = {
                "nama_petugas": nama_petugas, "nama_anak": n_anak, "nik_anak": n_nik,
                "tgl_lahir": str(tgl_lhr), "jenis_kelamin": n_jk, "usia_bulan": bln,
                "nama_ayah": n_ayah, "nama_ibu": n_ibu, "alamat": n_alamat,
                "link_dokumentasi": LINK_DRIVE, "vaksin": ", ".join(n_vaksin)
            }
            res = requests.post(url_base, json=payload, headers=headers)
            if res.status_code in [200, 201]:
                st.success(f"✅ Data {n_anak} berhasil disimpan!")
                st.balloons()
                reset_form()
                st.rerun()

# --- 8. HALAMAN DASHBOARD (PROFESIONAL) ---
elif menu == "Dashboard":
    st.markdown('<div class="header-box"><h1 class="judul-teks">📊 DASHBOARD MONITORING</h1></div>', unsafe_allow_html=True)
    
    res = requests.get(url_base, headers=headers)
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        if not df.empty:
            # Row 1: Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Anak", len(df))
            kp = 'nama_petugas' if 'nama_petugas' in df.columns else df.columns[0]
            c2.metric("Petugas Aktif", df[kp].nunique())
            c3.metric("Periode", "Tahun 2026")

            # Row 2: Grafik Rekap Vaksin
            st.markdown("---")
            st.subheader("💉 Rekapitulasi Jenis Vaksin Terpakai")
            all_v = df['vaksin'].str.split(', ').explode()
            v_counts = all_v.value_counts().reset_index()
            v_counts.columns = ['Vaksin', 'Total']
            
            fig_v = px.bar(v_counts, x='Total', y='Vaksin', orientation='h', text='Total',
                           color='Total', color_continuous_scale='GnBu')
            fig_v.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
            st.plotly_chart(fig_v, use_container_width=True)

            # Row 3: Grafik Petugas
            st.markdown("---")
            st.subheader("📈 Capaian Input Data Per Petugas")
            p_counts = df[kp].value_counts().reset_index()
            p_counts.columns = ['Petugas', 'Jumlah']
            
            fig_p = px.bar(p_counts, x='Jumlah', y='Petugas', orientation='h', text='Jumlah',
                           color='Jumlah', color_continuous_scale='Purples')
            fig_p.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=150))
            st.plotly_chart(fig_p, use_container_width=True)

            # Row 4: Tabel Data
            st.markdown("---")
            st.subheader("📋 Data Riwayat Lengkap")
            st.dataframe(df, use_container_width=True)
            
            # Download Button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Ekspor Laporan (CSV)", data=csv, file_name=f"laporan_imunisasi_{date.today()}.csv")
        else:
            st.info("Database masih kosong.")
    else: st.error("Gagal mengambil data database.")

# --- 9. FOOTER ---
st.markdown("<div style='text-align: center; color: #7b1fa2; font-size: 0.8rem; margin-top: 50px;'><hr>© 2026 E-Imunisasi Digital - Dev by Riko Putra</div>", unsafe_allow_html=True)
