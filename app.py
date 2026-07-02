import streamlit as st
import requests
import json
from datetime import datetime

# ---------- KONFIGURASI ----------
# Ganti URL ini dengan link API Google Sheets dari Sheet.best (nanti dijelaskan)
SHEET_URL = "https://api.sheetbest.com/sheets/72f98a03-5ba2-434d-b486-b66320253153" 

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
        ["Program MATH DROP-IN", "Program ENGLISH FOR KIDS", "Program ENGLISH FOR TEENS", "Program PREMIUM MATH"]
    )

    # === BAGIAN 4: JADWAL KHUSUS PROGRAM A (Muncul bersyarat) ===
    st.header("📅 Jadwal Program MATH DROP-IN")

    jadwal_a = []
    if "Program MATH DROP-IN" in programs:
        jadwal_a = st.multiselect(
            label="Pilih jadwal untuk Program MATH DROP-IN",
            options=
            ["Day 1 (Senin, 18.00 - 20.00)",
             "Day 2 (Selasa, 18.00 - 20.00)",
             "Day 3 (Rabu, 18.00 - 20.00)",
             "Day 4 (Kamis, 18.00 - 20.00)",
             "Day 5 (Jumat, 18.00 - 20.00)"],
             placeholder="Pilih minimal satu jadwal"
        )
        #Tampilan hasil pilihan
        st.write("Jadwal yang dipilih:", jadwal_a)

    else:
        st.info("ℹ️ Karena tidak memilih Program MATH DROP-IN, lewati bagian ini.")

    # === TOMBOL SUBMIT ===
    submitted = st.form_submit_button("✅ Daftar Sekarang")

    # ---------- PROSES DATA SAAT SUBMIT ----------
    if submitted:
        # Validasi wajib
        if not nama or not orang_tua or not wa or not alamat or not programs:
            st.error("❌ Mohon lengkapi semua data yang bertanda * (bintang).")
        # Validasi khusus program MATH DROP-IN: Wajib pilih minimal 1 jadwal
        elif "Program MATH DROP-IN" in programs and len(jadwal_a) == 0:
            st.error("❌ Anda memilih program MATH DROP-IN, tapi belum memilih jadwalnya. Pilih minimal 1 jadwal.")
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
