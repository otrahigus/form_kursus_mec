import streamlit as st
import requests
from datetime import datetime

# =========================================================
# KONFIGURASI
# =========================================================
SHEET_URL = "https://api.sheetbest.com/sheets/72f98a03-5ba2-434d-b486-b66320253153"

st.set_page_config(
    page_title="Pendaftaran Kursus",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
    /* =====================================================
       PALET WARNA:
       Biru tua   #0b3d91  (judul, aksen utama)
       Biru       #1565c0  (aksen sekunder)
       Hijau      #00796b / #2e7d32 (sukses, aksen kedua)
       Putih      #ffffff  (kartu, teks di atas warna gelap)
       Teks gelap #0f2436  (teks utama di atas putih)
       ===================================================== */

    /* ---------- Global ---------- */
    .stApp {
        background: linear-gradient(160deg, #e6f1fb 0%, #e5f6ee 100%);
    }
    #MainMenu, footer {visibility: hidden;}
    div.block-container {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 640px;
    }

    /* Paksa semua teks default (markdown, label, dsb) jadi gelap & jelas */
    html, body, [class^="css"], .stMarkdown, .stMarkdown p,
    div[data-testid="stMarkdownContainer"] p {
        color: #0f2436 !important;
    }

    /* ---------- Header ---------- */
    .hero {
        background: linear-gradient(135deg, #0b3d91 0%, #0d6efd 55%, #00897b 100%);
        padding: 34px 24px 30px 24px;
        border-radius: 22px;
        text-align: center;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(11,61,145,0.3);
    }
    .hero .emoji { font-size: 2.8rem; display:block; margin-bottom: 6px;}
    .hero h1 {
        color: #ffffff !important;
        font-size: 1.7rem;
        font-weight: 800;
        margin: 0 0 6px 0;
        letter-spacing: -0.3px;
    }
    .hero p {
        color: #ffffff !important;
        font-size: 0.95rem;
        margin: 0;
        line-height: 1.4;
        opacity: 0.95;
    }

    /* ---------- Progress ---------- */
    .progress-wrap {
        background: #ffffff;
        border-radius: 14px;
        padding: 12px 16px;
        margin-bottom: 4px;
        border: 1px solid #d7e6f2;
        box-shadow: 0 4px 14px rgba(11,61,145,0.06);
    }
    .progress-label {
        display:flex; justify-content: space-between;
        font-size: 0.85rem; font-weight: 700; color:#0b3d91 !important;
        margin-bottom: 6px;
    }
    div[data-testid="stProgress"] div[role="progressbar"] > div {
        background: linear-gradient(90deg, #0d6efd, #00897b) !important;
    }

    /* ---------- Section card ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important;
        border-radius: 18px !important;
        box-shadow: 0 6px 20px rgba(11,61,145,0.08);
        border: 1px solid #dbe9f5 !important;
    }
    .section-title {
        font-size: 1.08rem;
        font-weight: 800;
        color: #0b3d91 !important;
        display:flex; align-items:center; gap:8px;
        margin-bottom: 4px;
    }
    .section-sub {
        font-size: 0.85rem;
        color: #45607a !important;
        margin-bottom: 14px;
    }
    .required { color: #d32f2f !important; font-weight: 700; }

    /* ---------- Label input (nama field, dsb) ---------- */
    div[data-testid="stWidgetLabel"] p {
        color: #0f2436 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }

    /* ---------- Text input & selectbox ---------- */
    .stTextInput input {
        border-radius: 12px !important;
        border: 1.5px solid #c3d9ea !important;
        background-color: #ffffff !important;
        color: #0f2436 !important;
    }
    .stTextInput input::placeholder { color: #90a4b7 !important; }
    .stTextInput input:focus {
        border-color: #0d6efd !important;
        box-shadow: 0 0 0 3px rgba(13,110,253,0.15) !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border: 1.5px solid #c3d9ea !important;
        background-color: #ffffff !important;
        color: #0f2436 !important;
    }
    .stSelectbox div[data-baseweb="select"] * { color: #0f2436 !important; }
    ul[data-testid="stSelectboxVirtualDropdown"] li,
    ul[data-testid="stSelectboxVirtualDropdown"] li * {
        color: #0f2436 !important;
        background-color: #ffffff !important;
    }

    /* ---------- Program chips (checkbox look) ---------- */
    .stCheckbox {
        background: #f2f8fc;
        border-radius: 12px;
        padding: 6px 12px;
        margin-bottom: 6px;
        border: 1.5px solid #d7e6f2;
        transition: all .15s ease;
    }
    .stCheckbox:hover { background: #e6f1fb; border-color: #0d6efd; }
    .stCheckbox label p,
    .stCheckbox label span {
        font-size: 0.98rem !important;
        color: #0f2436 !important;
        font-weight: 600 !important;
    }
    .stCheckbox svg { color: #00897b !important; }

    /* ---------- Alerts ---------- */
    .hint-box, .warn-box, .ok-box, .muted-box {
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 0.87rem;
        margin-top: 6px;
        font-weight: 600;
    }
    .hint-box {
        background: #e3f2fd;
        border-left: 4px solid #0d6efd;
        color: #0b3d91 !important;
    }
    .warn-box {
        background: #fff4e5;
        border-left: 4px solid #ef6c00;
        color: #8a4a00 !important;
    }
    .ok-box {
        background: #e2f5ec;
        border-left: 4px solid #00897b;
        color: #00594c !important;
    }
    .muted-box {
        background: #eef2f5;
        border-left: 4px solid #90a4ae;
        color: #37474f !important;
        font-weight: 500;
    }

    /* ---------- Submit button ---------- */
    .stButton button {
        background: linear-gradient(135deg, #0b3d91, #00897b) !important;
        color: #ffffff !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        padding: 14px !important;
        border-radius: 14px !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0 8px 20px rgba(11,61,145,0.3) !important;
        transition: transform .15s ease, box-shadow .15s ease !important;
    }
    .stButton button p { color: #ffffff !important; font-weight: 800 !important; }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 26px rgba(11,61,145,0.4) !important;
    }

    /* ---------- Expander ringkasan ---------- */
    div[data-testid="stExpander"] {
        background: #ffffff !important;
        border-radius: 14px !important;
        border: 1px solid #dbe9f5 !important;
    }
    div[data-testid="stExpander"] summary p { color: #0b3d91 !important; font-weight: 700 !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] li { color: #0f2436 !important; }

    .footer-note {
        text-align: center;
        padding: 26px 0 6px 0;
        color: #5b7a90;
        font-size: 0.8rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <span class="emoji">🏫</span>
    <h1>Pendaftaran Kursus</h1>
    <p>📱 Isi data anaknya ya, Bu/Pak. Boleh pilih lebih dari 1 program.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# BAGIAN 1: DATA DIRI
# =========================================================
with st.container(border=True):
    st.markdown('<div class="section-title">👤 Data Diri Siswa</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Kolom bertanda <span class="required">*</span> wajib diisi</div>', unsafe_allow_html=True)

    nama = st.text_input("Nama Lengkap Siswa *", placeholder="Contoh: Ahmad Fauzi")
    nama_panggilan = st.text_input("Nama Panggilan (opsional)", placeholder="Contoh: Ahmad")
    orang_tua = st.text_input("Nama Orang Tua / Wali *", placeholder="Contoh: Bapak Slamet")

    col1, col2 = st.columns(2)
    with col1:
        wa = st.text_input("No. WhatsApp Orang Tua *", placeholder="81234567890")
    with col2:
        alamat = st.text_input("Alamat (RT / Dusun) *", placeholder="Contoh: RT 02, Krajan")

# =========================================================
# BAGIAN 2: DATA PENDUKUNG
# =========================================================
with st.container(border=True):
    st.markdown('<div class="section-title">📚 Data Pendukung</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Membantu kami menyesuaikan kelas</div>', unsafe_allow_html=True)

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

# =========================================================
# BAGIAN 3: PILIHAN PROGRAM
# =========================================================
with st.container(border=True):
    st.markdown('<div class="section-title">🎯 Pilih Program Kursus</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Centang semua program yang ingin diikuti</div>', unsafe_allow_html=True)

    cek_program_a = st.checkbox("💻 Program MATH DROP-IN")
    cek_program_b = st.checkbox("🎨 Program ENGLISH FOR KIDS")
    cek_program_c = st.checkbox("📖 Program ENGLISH FOR TEENS")
    cek_program_d = st.checkbox("✏️ Program PREMIUM MATH")

    programs = []
    if cek_program_a: programs.append("Program MATH DROP-IN")
    if cek_program_b: programs.append("Program ENGLISH FOR KIDS")
    if cek_program_c: programs.append("Program ENGLISH FOR TEENS")
    if cek_program_d: programs.append("Program PREMIUM MATH")

    if programs:
        st.markdown(f'<div class="ok-box">✅ {len(programs)} program dipilih</div>', unsafe_allow_html=True)

# =========================================================
# BAGIAN 4: JADWAL PROGRAM A (MUNCUL OTOMATIS)
# =========================================================
jadwal_a = []
if cek_program_a:
    with st.container(border=True):
        st.markdown('<div class="section-title">📅 Jadwal MATH DROP-IN</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Centang jadwal yang diinginkan (boleh lebih dari 1)</div>', unsafe_allow_html=True)

        sesi_list = [
            ("🕐 Sesi 1 (Senin, 18.00–20.00)", "Sesi 1 (Senin, 18.00 - 20.00)"),
            ("🕑 Sesi 2 (Selasa, 18.00–20.00)", "Sesi 2 (Selasa, 18.00 - 20.00)"),
            ("🕒 Sesi 3 (Rabu, 18.00–20.00)", "Sesi 3 (Rabu, 18.00 - 20.00)"),
            ("🕓 Sesi 4 (Kamis, 18.00–20.00)", "Sesi 4 (Kamis, 18.00 - 20.00)"),
            ("🕔 Sesi 5 (Jumat, 18.00–20.00)", "Sesi 5 (Jumat, 18.00 - 20.00)"),
        ]
        for label, value in sesi_list:
            if st.checkbox(label):
                jadwal_a.append(value)

        if len(jadwal_a) == 0:
            st.markdown('<div class="warn-box">⚠️ Belum ada jadwal dipilih. Centang minimal 1.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ok-box">✅ {len(jadwal_a)} jadwal dipilih</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="muted-box">ℹ️ Bagian jadwal akan muncul otomatis jika Anda memilih Program MATH DROP-IN.</div>', unsafe_allow_html=True)

st.write("")

# =========================================================
# PROGRESS INDIKATOR (opsional, membantu pengguna)
# =========================================================
required_fields = [nama, orang_tua, wa, alamat]
filled = sum(1 for f in required_fields if f.strip())
if sekolah_kelas != "Pilih...":
    filled += 1
if programs:
    filled += 1
total_steps = len(required_fields) + 2
pct = int((filled / total_steps) * 100)

st.markdown(f"""
<div class="progress-wrap">
    <div class="progress-label"><span>Kelengkapan formulir</span><span>{pct}%</span></div>
</div>
""", unsafe_allow_html=True)
st.progress(pct / 100)

# =========================================================
# TOMBOL SUBMIT & SIMPAN DATA
# =========================================================
submitted = st.button("✅ Daftar Sekarang", type="primary", use_container_width=True)

if submitted:
    if not nama or not orang_tua or not wa or not alamat:
        st.error("❌ Mohon lengkapi semua data yang bertanda *.")
    elif sekolah_kelas == "Pilih...":
        st.error("❌ Pilih Sekolah & Kelas terlebih dahulu.")
    elif len(programs) == 0:
        st.error("❌ Pilih minimal 1 program kursus.")
    elif cek_program_a and len(jadwal_a) == 0:
        st.error("❌ Anda memilih Program MATH DROP-IN, tapi belum memilih jadwal. Centang minimal 1.")
    else:
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

        try:
            response = requests.post(SHEET_URL, json=data_pendaftar)
            if response.status_code in [200, 201]:
                st.success(f"✅ Pendaftaran **{nama}** berhasil! Data sudah tersimpan.")
                st.balloons()
            else:
                st.error(f"❌ Gagal simpan ke server. Status: {response.status_code}")
                st.json(data_pendaftar)
        except Exception as e:
            st.error(f"❌ Error koneksi: {e}")
            st.info("Data tidak tersimpan, berikut datanya (screenshot/catat):")
            st.json(data_pendaftar)

        with st.expander("📋 Lihat Ringkasan Data Pendaftaran"):
            st.write(f"**Nama:** {nama}")
            st.write(f"**WA:** {wa}")
            st.write(f"**Program:** {', '.join(programs)}")
            if jadwal_a:
                st.write(f"**Jadwal A:** {', '.join(jadwal_a)}")

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer-note">
    <hr style="border: none; border-top: 1px solid #dfe6ee; margin-bottom: 12px;">
    Made with ❤️ untuk warga kampung
</div>
""", unsafe_allow_html=True)        border-radius: 22px;
        text-align: center;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(26,35,126,0.25);
    }
    .hero .emoji { font-size: 2.8rem; display:block; margin-bottom: 6px;}
    .hero h1 {
        color: #ffffff;
        font-size: 1.7rem;
        font-weight: 800;
        margin: 0 0 6px 0;
        letter-spacing: -0.3px;
    }
    .hero p {
        color: #dbe4ff;
        font-size: 0.95rem;
        margin: 0;
        line-height: 1.4;
    }

    /* ---------- Progress ---------- */
    .progress-wrap {
        background: #ffffff;
        border-radius: 14px;
        padding: 12px 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    }
    .progress-label {
        display:flex; justify-content: space-between;
        font-size: 0.82rem; font-weight: 600; color:#455a64;
        margin-bottom: 6px;
    }

    /* ---------- Section card ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.04) !important;
    }
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0d47a1;
        display:flex; align-items:center; gap:8px;
        margin-bottom: 4px;
    }
    .section-sub {
        font-size: 0.85rem;
        color: #78909c;
        margin-bottom: 14px;
    }
    .required { color: #e53935; }

    /* ---------- Inputs ---------- */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 12px !important;
    }
    .stTextInput input:focus {
        border-color: #3949ab !important;
        box-shadow: 0 0 0 2px rgba(57,73,171,0.15) !important;
    }

    /* ---------- Program chips (checkbox look) ---------- */
    .stCheckbox {
        background: #f7f9fc;
        border-radius: 12px;
        padding: 4px 10px;
        margin-bottom: 6px;
        border: 1px solid #e8eaf0;
        transition: all .15s ease;
    }
    .stCheckbox:hover { background: #eef2fb; }
    .stCheckbox label p { font-size: 0.98rem !important; color:#263238 !important; font-weight: 500; }

    /* ---------- Alerts ---------- */
    .hint-box {
        background: #e8f0fe;
        border-left: 4px solid #1e88e5;
        color: #0d47a1;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 0.85rem;
        margin-top: 6px;
    }
    .warn-box {
        background: #fff3e0;
        border-left: 4px solid #fb8c00;
        color: #e65100;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 0.85rem;
        margin-top: 6px;
    }
    .ok-box {
        background: #e8f5e9;
        border-left: 4px solid #43a047;
        color: #2e7d32;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 0.85rem;
        margin-top: 6px;
        font-weight: 600;
    }
    .muted-box {
        background: #f5f5f5;
        border-left: 4px solid #b0bec5;
        color: #607d8b;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 0.85rem;
    }

    /* ---------- Submit button ---------- */
    .stButton button {
        background: linear-gradient(135deg, #1a237e, #3949ab) !important;
        color: white !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        padding: 14px !important;
        border-radius: 14px !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0 8px 20px rgba(26,35,126,0.28) !important;
        transition: transform .15s ease, box-shadow .15s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 26px rgba(26,35,126,0.35) !important;
    }

    .footer-note {
        text-align: center;
        padding: 26px 0 6px 0;
        color: #90a4ae;
        font-size: 0.78rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <span class="emoji">🏫</span>
    <h1>Pendaftaran Kursus</h1>
    <p>📱 Isi data anaknya ya, Bu/Pak. Boleh pilih lebih dari 1 program.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# BAGIAN 1: DATA DIRI
# =========================================================
with st.container(border=True):
    st.markdown('<div class="section-title">👤 Data Diri Siswa</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Kolom bertanda <span class="required">*</span> wajib diisi</div>', unsafe_allow_html=True)

    nama = st.text_input("Nama Lengkap Siswa *", placeholder="Contoh: Ahmad Fauzi")
    nama_panggilan = st.text_input("Nama Panggilan (opsional)", placeholder="Contoh: Ahmad")
    orang_tua = st.text_input("Nama Orang Tua / Wali *", placeholder="Contoh: Bapak Slamet")

    col1, col2 = st.columns(2)
    with col1:
        wa = st.text_input("No. WhatsApp Orang Tua *", placeholder="81234567890")
    with col2:
        alamat = st.text_input("Alamat (RT / Dusun) *", placeholder="Contoh: RT 02, Krajan")

# =========================================================
# BAGIAN 2: DATA PENDUKUNG
# =========================================================
with st.container(border=True):
    st.markdown('<div class="section-title">📚 Data Pendukung</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Membantu kami menyesuaikan kelas</div>', unsafe_allow_html=True)

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

# =========================================================
# BAGIAN 3: PILIHAN PROGRAM
# =========================================================
with st.container(border=True):
    st.markdown('<div class="section-title">🎯 Pilih Program Kursus</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Centang semua program yang ingin diikuti</div>', unsafe_allow_html=True)

    cek_program_a = st.checkbox("💻 Program MATH DROP-IN")
    cek_program_b = st.checkbox("🎨 Program ENGLISH FOR KIDS")
    cek_program_c = st.checkbox("📖 Program ENGLISH FOR TEENS")
    cek_program_d = st.checkbox("✏️ Program PREMIUM MATH")

    programs = []
    if cek_program_a: programs.append("Program MATH DROP-IN")
    if cek_program_b: programs.append("Program ENGLISH FOR KIDS")
    if cek_program_c: programs.append("Program ENGLISH FOR TEENS")
    if cek_program_d: programs.append("Program PREMIUM MATH")

    if programs:
        st.markdown(f'<div class="ok-box">✅ {len(programs)} program dipilih</div>', unsafe_allow_html=True)

# =========================================================
# BAGIAN 4: JADWAL PROGRAM A (MUNCUL OTOMATIS)
# =========================================================
jadwal_a = []
if cek_program_a:
    with st.container(border=True):
        st.markdown('<div class="section-title">📅 Jadwal MATH DROP-IN</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Centang jadwal yang diinginkan (boleh lebih dari 1)</div>', unsafe_allow_html=True)

        sesi_list = [
            ("🕐 Sesi 1 (Senin, 18.00–20.00)", "Sesi 1 (Senin, 18.00 - 20.00)"),
            ("🕑 Sesi 2 (Selasa, 18.00–20.00)", "Sesi 2 (Selasa, 18.00 - 20.00)"),
            ("🕒 Sesi 3 (Rabu, 18.00–20.00)", "Sesi 3 (Rabu, 18.00 - 20.00)"),
            ("🕓 Sesi 4 (Kamis, 18.00–20.00)", "Sesi 4 (Kamis, 18.00 - 20.00)"),
            ("🕔 Sesi 5 (Jumat, 18.00–20.00)", "Sesi 5 (Jumat, 18.00 - 20.00)"),
        ]
        for label, value in sesi_list:
            if st.checkbox(label):
                jadwal_a.append(value)

        if len(jadwal_a) == 0:
            st.markdown('<div class="warn-box">⚠️ Belum ada jadwal dipilih. Centang minimal 1.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ok-box">✅ {len(jadwal_a)} jadwal dipilih</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="muted-box">ℹ️ Bagian jadwal akan muncul otomatis jika Anda memilih Program MATH DROP-IN.</div>', unsafe_allow_html=True)

st.write("")

# =========================================================
# PROGRESS INDIKATOR (opsional, membantu pengguna)
# =========================================================
required_fields = [nama, orang_tua, wa, alamat]
filled = sum(1 for f in required_fields if f.strip())
if sekolah_kelas != "Pilih...":
    filled += 1
if programs:
    filled += 1
total_steps = len(required_fields) + 2
pct = int((filled / total_steps) * 100)

st.markdown(f"""
<div class="progress-wrap">
    <div class="progress-label"><span>Kelengkapan formulir</span><span>{pct}%</span></div>
</div>
""", unsafe_allow_html=True)
st.progress(pct / 100)

# =========================================================
# TOMBOL SUBMIT & SIMPAN DATA
# =========================================================
submitted = st.button("✅ Daftar Sekarang", type="primary", use_container_width=True)

if submitted:
    if not nama or not orang_tua or not wa or not alamat:
        st.error("❌ Mohon lengkapi semua data yang bertanda *.")
    elif sekolah_kelas == "Pilih...":
        st.error("❌ Pilih Sekolah & Kelas terlebih dahulu.")
    elif len(programs) == 0:
        st.error("❌ Pilih minimal 1 program kursus.")
    elif cek_program_a and len(jadwal_a) == 0:
        st.error("❌ Anda memilih Program MATH DROP-IN, tapi belum memilih jadwal. Centang minimal 1.")
    else:
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

        try:
            response = requests.post(SHEET_URL, json=data_pendaftar)
            if response.status_code in [200, 201]:
                st.success(f"✅ Pendaftaran **{nama}** berhasil! Data sudah tersimpan.")
                st.balloons()
            else:
                st.error(f"❌ Gagal simpan ke server. Status: {response.status_code}")
                st.json(data_pendaftar)
        except Exception as e:
            st.error(f"❌ Error koneksi: {e}")
            st.info("Data tidak tersimpan, berikut datanya (screenshot/catat):")
            st.json(data_pendaftar)

        with st.expander("📋 Lihat Ringkasan Data Pendaftaran"):
            st.write(f"**Nama:** {nama}")
            st.write(f"**WA:** {wa}")
            st.write(f"**Program:** {', '.join(programs)}")
            if jadwal_a:
                st.write(f"**Jadwal A:** {', '.join(jadwal_a)}")

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer-note">
    <hr style="border: none; border-top: 1px solid #dfe6ee; margin-bottom: 12px;">
    Made with ❤️ untuk warga kampung
</div>
""", unsafe_allow_html=True)
