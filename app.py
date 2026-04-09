# --- HALAMAN 2: DASHBOARD MONITORING (VERSI PERBAIKAN VALUEERROR) ---
elif menu == "Dashboard Monitoring":
    st.markdown("<h1 style='text-align:center; color:#4a148c;'>📊 Dashboard Monitoring</h1>", unsafe_allow_html=True)
    
    try:
        res = requests.get(url_base, headers=headers)
        if res.status_code == 200:
            data_json = res.json()
            if data_json:
                df = pd.DataFrame(data_json)
                
                # --- BAGIAN RINGKASAN ATAS ---
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Anak", len(df))
                
                # Cek apakah kolom 'nama_petugas' ada
                kolom_petugas = 'nama_petugas' if 'nama_petugas' in df.columns else df.columns[0]
                col2.metric("Petugas Terlibat", df[kolom_petugas].nunique())
                col3.metric("Update Terakhir", str(date.today()))
                
                # --- BAGIAN GRAFIK ---
                st.markdown("### 📈 Grafik Kinerja Petugas")
                # Menyiapkan data untuk grafik agar tidak ValueError
                data_grafik = df[kolom_petugas].value_counts().reset_index()
                data_grafik.columns = ['Nama Petugas', 'Jumlah Input'] # Memberi nama kolom baru
                
                fig = px.bar(
                    data_grafik, 
                    x='Nama Petugas', 
                    y='Jumlah Input',
                    color='Jumlah Input',
                    color_continuous_scale='Purples',
                    template='plotly_white'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # --- BAGIAN TABEL ---
                st.markdown("### 📋 Tabel Riwayat Data")
                st.dataframe(df, use_container_width=True)
                
                # Tombol Download Data
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Laporan (CSV)", data=csv, file_name=f"laporan_imunisasi_{date.today()}.csv", mime='text/csv')
                
            else:
                st.info("Database masih kosong. Silakan input data terlebih dahulu.")
        else:
            st.error(f"Gagal mengambil data. Status: {res.status_code}")
    except Exception as e:
        st.error(f"Terjadi kesalahan teknis: {e}")