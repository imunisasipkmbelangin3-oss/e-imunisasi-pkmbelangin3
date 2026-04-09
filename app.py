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
    .header-box { display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 25px; }
    .judul-teks { color: #4a148c; font-weight: 800; font-size: 3rem; margin: 0; }
    .usia-badge { background-color: #7b1fa2; color: white; padding: 15px; border-radius: 12px; text-align: center; font-size: 1.6rem; font-weight: 800; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

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

# --- NAVIGASI ---
menu = st.sidebar.radio("Navigasi:", ["Input Data", "Dashboard", "Keluar"])
if menu == "Keluar":
    st.session_state['logged_in'] = False
    st.rerun()

# --- HALAMAN INPUT ---
if menu == "Input Data":
    st.markdown('<div class="header-box"><h1 class="judul-teks">E-IMUNISASI</h1></div>', unsafe_allow_html=True)

    # FUNGSI RESET (KOSONGKAN DATA)
    def reset_data():
        st.session_state.nama_anak = ""
        st.session_state.nik = ""
        st.session_state.ayah = ""
        st.session_state.ibu = ""
        st.session_state.alamat = ""
        st.session_state.vaksin = []

    # Inisialisasi State jika belum ada
    if 'nama_anak' not in st.session_state: reset_data()

    st.markdown("### 👨‍⚕️ Petugas")
    nama_petugas = st.selectbox("Pilih Petugas*", ["-- Pilih --", "Winoto Hadi, A.Md.Kep", "Yanto Perdianta, S.Kep.Ns", "Eva Asri Deti, A.Md.Keb", "Desiani, A.Md.Keb", "Dian Yuniarsih, A.Md.Keb"])
    
    st.markdown("---")
    st.markdown("### 👶 Informasi Anak")
    col_a, col_b = st.columns(2)
    with col_a:
        # Gunakan 'key' agar bisa dikosongkan secara otomatis
        nama_anak = st.text_input("Nama Lengkap Anak*", key="nama_anak")
        nik = st.text_input("NIK Anak*", key="nik")
        jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True)
    
    with col_b:
        tgl_lahir = st.date_input("Tanggal Lahir", value=date.today())
        today = date.today()
        total_bulan = (today.year - tgl_lahir.year) * 12 + today.month - tgl_lahir.month
        st.markdown(f'<div class="usia-badge">{total_bulan} BULAN</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 👪 Orang Tua & Alamat")
    c1, c2 = st.columns(2)
    with c1:
        nama_ayah = st.text_input("Nama Ayah", key="ayah")
        nama_ibu = st.text_input("Nama Ibu", key="ibu")
    with c2:
        alamat = st.text_area("Alamat Lengkap", key="alamat")

    st.markdown("---")
    st.markdown("### 💉 Vaksin")
    semua_vaksin = ["HB O Inject", "BCG", "Polio 1", "DPT / HIB 1", "Polio 2", "Rotavirus 1", "DPT / HIB 2", "Polio 3", "Rotavirus 2", "DPT / HIB 3", "Polio 4", "Rotavirus 3", "IPV 1", "IPV 2", "Campak 9 bulan", "DPT Lanjutan", "Campak Lanjutan", "PCV 1", "PCV 2", "PCV 3", "JE", "TT CATIN", "TT 1 BUMIL", "TT 2 BUMIL", "TT 3 BUMIL", "TT 4 BUMIL", "TT 5 BUMIL"]
    vaksin_dipilih = st.multiselect("Pilih Vaksin*", semua_vaksin, key="vaksin")

    if st.button("SIMPAN DATA", use_container_width=True):
        if nama_petugas == "-- Pilih --" or not nama_anak or not nik:
            st.error("❌ Nama Petugas, Nama Anak, dan NIK wajib diisi!")
        else:
            payload = {
                "nama_petugas": nama_petugas, "nama_anak": nama_anak, "nik_anak": nik,
                "tgl_lahir": str(tgl_lahir), "jenis_kelamin": jk, "usia_bulan": total_bulan,
                "nama_ayah": nama_ayah, "nama_ibu": nama_ibu, "alamat": alamat,
                "vaksin": ", ".join(vaksin_dipilih)
            }
            res = requests.post(url_base, json=payload, headers=headers)
            if res.status_code in [200, 201]:
                st.success(f"✅ Data {nama_anak} Berhasil Disimpan!")
                st.balloons()
                # KOSONGKAN FORM SETELAH SUKSES
                reset_data()
                st.rerun() # Refresh halaman agar inputan benar-benar kosong

# --- HALAMAN DASHBOARD (VERSI GRAFIK LENGKAP) ---
elif menu == "Dashboard":
    st.markdown("<h1 style='text-align:center; color:#4a148c;'>📊 Dashboard Monitoring</h1>", unsafe_allow_html=True)
    
    try:
        res = requests.get(url_base, headers=headers)
        if res.status_code == 200:
            data_json = res.json()
            if data_json:
                df = pd.DataFrame(data_json)
                
                # --- RINGKASAN DATA ---
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Anak", len(df))
                
                # Deteksi kolom petugas untuk ringkasan
                kp = 'nama_petugas' if 'nama_petugas' in df.columns else df.columns[0]
                c2.metric("Petugas Aktif", df[kp].nunique())
                c3.metric("Update", date.today().strftime("%d/%m/%Y"))

                # --- BAGIAN GRAFIK ---
                st.markdown("### 📈 Capaian Input Per Petugas")
                
                # Hitung jumlah input per petugas
                df_counts = df[kp].value_counts().reset_index()
                df_counts.columns = ['Petugas', 'Jumlah']
                
                # Buat Grafik Batang
                fig = px.bar(
                    df_counts, 
                    x='Petugas', 
                    y='Jumlah',
                    text='Jumlah',
                    color='Jumlah',
                    color_continuous_scale='Purples',
                    labels={'Petugas': 'Nama Petugas', 'Jumlah': 'Total Data'}
                )
                
                # Percantik tampilan grafik
                fig.update_traces(textposition='outside')
                fig.update_layout(
                    xaxis_tickangle=-45,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # --- BAGIAN TABEL ---
                st.markdown("### 📋 Tabel Riwayat Data")
                st.dataframe(df, use_container_width=True)
                
                # Tambahkan tombol download kalau Mas butuh laporannya dalam Excel/CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Data (CSV)", data=csv, file_name=f"data_imunisasi_{date.today()}.csv", mime='text/csv')
                
            else:
                st.info("Belum ada data yang tersimpan di database.")
        else:
            st.error(f"Gagal mengambil data: {res.status_code}")
    except Exception as e:
        st.error(f"Terjadi kesalahan teknis: {e}")

# --- FOOTER ---
st.markdown("<div style='text-align: center; color: #7b1fa2; font-size: 0.8rem; margin-top: 50px;'><hr>© 2026 E-Imunisasi Digital - Dev by Riko Putra</div>", unsafe_allow_html=True)
