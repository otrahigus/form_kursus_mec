import streamlit as st
import requests
import json
from datetime import datetime

# ---------- KONFIGURASI ----------
# Ganti URL ini dengan link API Google Sheets dari Sheet.best (nanti dijelaskan)
SHEET_URL = "https://api.sheetbest.com/sheets/c19c4310-8e7a-4680-8442-4b5784579e0c" 

# ---------- JUDUL HALAMAN ----------
st.set_page_config(page_title="Form Pendaftaran Kursus", page_icon="📝")
st.title("📝 Formulir Pendaftaran Kursus")
st.markdown("Isi data anaknya ya, Bu/Pak. Boleh pilih lebih dari 1 program.")

# ---------- FORMULIR UTAMA (pakai st.form agar tidak reload terus) ----------
with st.form("form_pendaftaran", clear_on_submit=False):

    # === BAGIAN 1: DATA DIRI ===
    st.header("👤 Data Diri Siswa")
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Lengkap Siswa *")
        nama_panggilan = st.text_input("Nama Panggilan (opsional)")
        orang_tua = st.text_input("Nama Orang Tua / Wali *")
    with col2:
        wa = st.text_input("Nomor WhatsApp Orang Tua *", placeholder="81234567890")
        alamat = st.text_input("Alamat (RT / Nama Dusun) *")

    # === BAGIAN 2: DATA PENDUKUNG ===
    st.header("📚 Data Pendukung")
    col3, col4 = st.columns(2)
    with col3:
        sekolah_kelas = st.selectbox(
            "Sekolah & Kelas *",
            ["SD Kelas 1", "SD Kelas 2", "SD Kelas 3", "SD Kelas 4", "SD Kelas 5", "SD Kelas 6",
             "SMP Kelas 1", "SMP Kelas 2", "SMP Kelas 3"]
        )
    with col4:
        pekerjaan_ortu = st.selectbox(
            "Pekerjaan Orang Tua",
            ["Petani/Berkebun", "Buruh Tani", "Pedagang/Jualan", "Karyawan/PNS", "Ibu Rumah Tangga", "Lainnya"]
        )

    # === BAGIAN 3: PILIH PROGRAM (Boleh lebih dari 1) ===
    st.header("🎯 Pilih Program Kursus")
    programs = st.multiselect(
        "Program apa saja yang ingin diikuti? (boleh lebih dari satu) *",
        ["Program A - Komputer", "Program B - Menggambar", "Program C - Ngaji"]
    )

    # === BAGIAN 4: JADWAL KHUSUS PROGRAM A (Muncul bersyarat) ===
    st.header("📅 Jadwal Program A (Komputer)")
    jadwal_a = None
    if "Program A - Komputer" in programs:
        jadwal_a = st.selectbox(
            "Pilih jadwal untuk Program A:",
            ["Sesi 1 (Senin & Rabu, 08.00 - 09.30)",
             "Sesi 2 (Senin & Rabu, 10.00 - 11.30)",
             "Sesi 3 (Selasa & Kamis, 08.00 - 09.30)",
             "Sesi 4 (Selasa & Kamis, 10.00 - 11.30)",
             "Sesi 5 (Sabtu, 09.00 - 11.00)"]
        )
    else:
        st.info("ℹ️ Karena tidak memilih Program A, lewati bagian ini.")

    # === TOMBOL SUBMIT ===
    submitted = st.form_submit_button("✅ Daftar Sekarang")

    # ---------- PROSES DATA SAAT SUBMIT ----------
    if submitted:
        # Validasi wajib
        if not nama or not orang_tua or not wa or not alamat or not programs:
            st.error("❌ Mohon lengkapi semua data yang bertanda * (bintang).")
        else:
            # Siapkan data
            data_pendaftar = {
                "tanggal_daftar": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nama_lengkap": nama,
                "nama_panggilan": nama_panggilan if nama_panggilan else "-",
                "orang_tua": orang_tua,
                "no_wa": wa,
                "alamat": alamat,
                "sekolah_kelas": sekolah_kelas,
                "pekerjaan_ortu": pekerjaan_ortu,
                "program_dipilih": ", ".join(programs),
                "jadwal_a": jadwal_a if jadwal_a else "-"
            }

            # ---------- SIMPAN KE GOOGLE SHEETS (via Sheet.best) ----------
            try:
                response = requests.post(SHEET_URL, json=data_pendaftar)
                if response.status_code == 200 or response.status_code == 201:
                    st.success(f"✅ Pendaftaran *{nama}* berhasil! Data sudah tersimpan aman.")
                    st.balloons()
                else:
                    # Jika gagal ke sheets, tetap tampilkan data di layar biar tidak hilang
                    st.warning("⚠️ Data tidak tersimpan ke Google Sheets (cek koneksi/URL). Tapi berikut data Anda:")
                    st.json(data_pendaftar)
            except Exception as e:
                st.error(f"❌ Gagal terhubung ke server penyimpanan: {e}")
                st.info("Tapi data tetap bisa dilihat di bawah ini (screenshot/catat ya):")
                st.json(data_pendaftar)

            # Tampilkan ringkasan data (untuk verifikasi orang tua)
            with st.expander("📋 Lihat Ringkasan Data Pendaftaran"):
                st.write(f"*Nama:* {nama}")
                st.write(f"*WA Orang Tua:* {wa}")
                st.write(f"*Program:* {', '.join(programs)}")
                if jadwal_a:
                    st.write(f"*Jadwal A:* {jadwal_a}")