import streamlit as st
import requests
from datetime import datetime
import base64

# ---------- KONFIGURASI ----------
SHEET_URL = "https://api.sheetbest.com/sheets/72f98a03-5ba2-434d-b486-b66320253153"

# ---------- PENGATURAN HALAMAN ----------
st.set_page_config(
    page_title="Form Pendaftaran Kursus", 
    page_icon="📝",
    layout="centered"
)

# ---------- CSS KUSTOM (Background Gradasi & Desain) ----------
st.image("https://drive.google.com/file/d/1HB7JWLcFGoRanNczUo-zMg9kzMvp22ah/view?usp=share_link")
st.markdown("""
<style>
    /* Background gradasi biru ke hijau */
    .stApp {
        background: linear-gradient(135deg, #e0f7fa 0%, #e8f5e9 100%);
    }
    
    /* Kartu putih untuk setiap bagian */
    .card {
        background-color: white;
        padding: 25px 20px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border: 1px solid rgba(255,255,255,0.5);
    }
    
    /* Judul utama */
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a237e;
        margin-bottom: 5px;
    }
    
    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #546e7a;
        margin-bottom: 20px;
    }
    
    /* Header setiap bagian */
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #0d47a1;
        border-left: 5px solid #42a5f5;
        padding-left: 12px;
        margin-bottom: 15px;
    }
    
    /* Label wajib */
    .required {
        color: #d32f2f;
        font-weight: 600;
    }
    
    /* Tombol Submit */
    .stButton button {
        background: linear-gradient(135deg, #1a237e, #283593) !important;
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        padding: 15px !important;
        border-radius: 15px !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        transform: scale(1.01) !important;
        box-shadow: 0 8px 25px rgba(26,35,126,0.3) !important;
    }
    
    /* Checkbox lebih besar */
    .stCheckbox label {
        font-size: 1.05rem !important;
        padding: 5px 0 !important;
    }
    
    /* Input text lebih besar */
    .stTextInput input, .stSelectbox select {
        font-size: 1rem !important;
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 10px 15px !important;
    }
    
    /* Info box */
    .info-box {
        background: #e3f2fd;
        padding: 15px 20px;
        border-radius: 15px;
        border-left: 5px solid #1e88e5;
        color: #0d47a1;
        margin: 10px 0;
    }
    
    /* Warning box */
    .warning-box {
        background: #fff3e0;
        padding: 15px 20px;
        border-radius: 15px;
        border-left: 5px solid #ff9800;
        color: #e65100;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div style="text-align: center; padding: 10px 0 5px 0;">
    <span style="font-size: 3rem;">🏫</span>
    <h1 class="main-title">Pendaftaran Kursus</h1>
    <p class="sub-title">📱 Isi data anaknya ya, Bu/Pak. Boleh pilih lebih dari 1 program.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# BAGIAN 1: DATA DIRI
# ==========================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">👤 Data Diri Siswa</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    nama = st.text_input("Nama Lengkap Siswa *", placeholder="Contoh: Ahmad Fauzi")
    nama_panggilan = st.text_input("Nama Panggilan (opsional)", placeholder="Contoh: Ahmad")
    orang_tua = st.text_input("Nama Orang Tua / Wali *", placeholder="Contoh: Bapak Slamet")
with col2:
    wa = st.text_input("Nomor WhatsApp Orang Tua *", placeholder="81234567890")
    alamat = st.text_input("Alamat (RT / Nama Dusun) *", placeholder="Contoh: RT 02, Dusun Krajan")

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# BAGIAN 2: DATA PENDUKUNG
# ==========================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">📚 Data Pendukung</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    sekolah_kelas = st.selectbox(
        "Sekolah & Kelas *",
        ["Pilih...", "SD Kelas 1", "SD Kelas 2", "SD Kelas 3", "SD Kelas 4", "SD Kelas 5", "SD Kelas 6",
         "SMP Kelas 1", "SMP Kelas 2", "SMP Kelas 3"]
    )
with col4:
    pekerjaan_ortu = st.selectbox(
        "Pekerjaan Orang Tua",
        ["Pilih...", "Petani/Berkebun", "Buruh Tani", "Pedagang/Jualan", "Karyawan/PNS", "Ibu Rumah Tangga", "Lainnya"]
    )

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# BAGIAN 3: PILIHAN PROGRAM
# ==========================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">🎯 Pilih Program Kursus</div>', unsafe_allow_html=True)
st.markdown("*Centang semua program yang ingin diikuti.*")

cek_program_a = st.checkbox("💻 Program MATH DROP-IN")
cek_program_b = st.checkbox("🎨 Program ENGLISH FOR KIDS")
cek_program_c = st.checkbox("📖 Program ENGLISH FOR TEENS")
cek_program_d = st.checkbox("📖 Program PREMIUM MATH")

programs = []
if cek_program_a:
    programs.append("Program MATH DROP-IN")
if cek_program_b:
    programs.append("Program ENGLISH FOR KIDS")
if cek_program_c:
    programs.append("Program ENGLISH FOR TEENS")
if cek_program_d:
    programs.append("Program PREMIUM MATH")

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# BAGIAN 4: JADWAL PROGRAM A (MUNCUL OTOMATIS)
# ==========================================
jadwal_a = []
if cek_program_a:
    st.markdown('<div class="card" style="border: 2px solid #42a5f5;">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📅 Jadwal Program MATH DROP-IN</div>', unsafe_allow_html=True)
    st.markdown("*Centang jadwal yang diinginkan (boleh pilih 1-5).*")
    
    if st.checkbox("🕐 Sesi 1 (Senin, 18.00 - 20.00)"):
        jadwal_a.append("Sesi 1 (Senin, 18.00 - 20.00)")
    if st.checkbox("🕑 Sesi 2 (Selasa, 18.00 - 20.00)"):
        jadwal_a.append("Sesi 2 (Selasa, 18.00 - 20.00)")
    if st.checkbox("🕒 Sesi 3 (Rabu, 18.00 - 20.00)"):
        jadwal_a.append("Sesi 3 (Rabu, 18.00 - 20.00)")
    if st.checkbox("🕓 Sesi 4 (Kamis, 18.00 - 20.00)"):
        jadwal_a.append("Sesi 4 (Kamis, 18.00 - 20.00)")
    if st.checkbox("🕔 Sesi 5 (Jumat, 18.00 - 20.00)"):
        jadwal_a.append("Sesi 5 (Jumat, 18.00 - 20.00)")

    if len(jadwal_a) == 0:
        st.markdown('<div class="warning-box">⚠️ Belum ada jadwal yang dipilih. Centang minimal 1.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color: #2e7d32; font-weight: 500;">✅ {len(jadwal_a)} jadwal dipilih</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="card" style="background: #f5f5f5;">', unsafe_allow_html=True)
    st.markdown('<div class="info-box">ℹ️ Karena tidak memilih Program MATH DROP-IN, bagian jadwal tidak muncul.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TOMBOL SUBMIT & SIMPAN DATA
# ==========================================
st.markdown("---")
submitted = st.button("✅ Daftar Sekarang", type="primary", use_container_width=True)

if submitted:
    # Validasi
    if not nama or not orang_tua or not wa or not alamat:
        st.error("❌ Mohon lengkapi semua data yang bertanda *.")
    elif sekolah_kelas == "Pilih...":
        st.error("❌ Pilih Sekolah & Kelas terlebih dahulu.")
    elif len(programs) == 0:
        st.error("❌ Pilih minimal 1 program kursus.")
    elif cek_program_a and len(jadwal_a) == 0:
        st.error("❌ Anda memilih Program MATH DROP-IN, tapi belum memilih jadwal. Centang minimal 1.")
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
            "jadwal_a": ", ".join(jadwal_a) if jadwal_a else "-"
        }

        # Kirim ke Sheet.best
        try:
            response = requests.post(SHEET_URL, json=data_pendaftar)
            if response.status_code in [200, 201]:
                st.success(f"✅ Pendaftaran *{nama}* berhasil! Data sudah tersimpan.")
                st.balloons()
            else:
                st.error(f"❌ Gagal simpan ke server. Status: {response.status_code}")
                st.json(data_pendaftar)
        except Exception as e:
            st.error(f"❌ Error koneksi: {e}")
            st.info("Data tidak tersimpan, berikut datanya (screenshot/catat):")
            st.json(data_pendaftar)

        # Tampilkan ringkasan
        with st.expander("📋 Lihat Ringkasan Data Pendaftaran"):
            st.write(f"*Nama:* {nama}")
            st.write(f"*WA:* {wa}")
            st.write(f"*Program:* {', '.join(programs)}")
            if jadwal_a:
                st.write(f"*Jadwal A:* {', '.join(jadwal_a)}")

# ---------- FOOTER ----------
st.markdown("""
<div style="text-align: center; padding: 30px 0 10px 0; color: #90a4ae; font-size: 0.8rem;">
    <hr style="border: none; border-top: 2px solid #e0e0e0;">
    Made with ❤️ untuk warga kampung
</div>
""", unsafe_allow_html=True)