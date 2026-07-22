import streamlit as st
import requests
from datetime import datetime
import base64
import os
import urllib.parse

# =========================================================
# KONFIGURASI
# =========================================================
SHEET_URL = "https://api.sheetbest.com/sheets/72f98a03-5ba2-434d-b486-b66320253153"

# Taruh file logo di folder yang sama dengan script ini, lalu ganti nama filenya di sini.
# Kosongkan / biarkan file tidak ada jika belum punya logo -> otomatis pakai emoji 🏫
LOGO_PATH = "logo.png"

# Taruh file poster/banner di folder yang sama, lalu ganti nama filenya di sini.
# Jika file ini ada, poster akan menggantikan kotak banner biru gradient.
# Jika tidak ada, banner biru default tetap dipakai.
POSTER_PATH = "poster.png"

def get_logo_base64(path):
    """Baca file gambar & ubah ke base64 agar bisa ditempel di dalam HTML/CSS."""
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        ext = path.split(".")[-1].lower()
        mime = "image/png" if ext == "png" else "image/jpeg" if ext in ("jpg", "jpeg") else "image/svg+xml" if ext == "svg" else "image/png"
        return f"data:{mime};base64,{base64.b64encode(data).decode()}"
    return None

logo_data_uri = get_logo_base64(LOGO_PATH)
poster_data_uri = get_logo_base64(POSTER_PATH)

BULAN_ID = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

def format_tanggal_indonesia(dt):
    """Format tanggal jadi teks 'DD Bulan YYYY HH:MM:SS' agar Google Sheets
    tidak otomatis mengonversinya jadi tanggal/angka (yang sering bikin berantakan)."""
    return f"{dt.day:02d} {BULAN_ID[dt.month - 1]} {dt.year} {dt.strftime('%H:%M:%S')}"

def normalisasi_teks(s):
    """Bersihkan teks untuk perbandingan: hilangkan spasi berlebih & abaikan huruf besar/kecil."""
    return " ".join((s or "").strip().lower().split())

def cek_data_existing(nama_lengkap, no_wa):
    """Cek ke sheet apakah kombinasi Nama Siswa + No. WA ini sudah pernah terdaftar.
    Menggunakan kombinasi (bukan No. WA saja) supaya kakak-adik yang memakai
    nomor WA orang tua yang sama tetap bisa mendaftar masing-masing.

    Pencocokan nama dibuat toleran: mengabaikan huruf besar/kecil dan spasi
    berlebih, karena orang tua bisa mengetik nama sedikit berbeda saat submit ulang.

    Catatan: sheet.best memfilter 1 kolom lewat URL path (bukan query param),
    contoh: SHEET_URL/no_wa/081234567890 -- jadi kita filter di server berdasarkan
    No. WA saja (exact match), lalu nama dibandingkan secara toleran di sisi kode.

    Mengembalikan data lama (dict, sesuai apa adanya di sheet) jika ada, atau None jika belum ada.
    """
    try:
        url = f"{SHEET_URL}/no_wa/{urllib.parse.quote(str(no_wa), safe='')}"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        rows = resp.json()
        target_nama = normalisasi_teks(nama_lengkap)
        for row in rows:
            if normalisasi_teks(row.get("nama_lengkap", "")) == target_nama:
                return row
        return None
    except Exception:
        # Jika gagal cek (mis. koneksi), anggap tidak ada duplikat agar tidak menghalangi pendaftaran
        return None

def simpan_data_baru(data_pendaftar):
    return requests.post(SHEET_URL, json=data_pendaftar, timeout=10)

def update_data_lama(nama_lengkap, no_wa, data_pendaftar):
    # Update berbasis gabungan 2 kolom -> pakai endpoint /search sesuai dokumentasi sheet.best
    # Gunakan nilai nama & WA PERSIS seperti yang tersimpan di sheet (bukan input baru)
    # agar filter update pasti cocok, walau penulisan huruf besar/kecil user berbeda.
    return requests.patch(
        f"{SHEET_URL}/search",
        params={"nama_lengkap": nama_lengkap, "no_wa": no_wa},
        json=data_pendaftar,
        timeout=10
    )

st.set_page_config(
    page_title="Pendaftaran Kursus",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Fallback: st.container(border=True) hanya ada di Streamlit >= 1.28.
# Jika versi lebih lama, gunakan container biasa agar tidak error.
def card():
    try:
        return st.container(border=True)
    except TypeError:
        return st.container()

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
    .hero .logo {
        width: 72px;
        height: 72px;
        object-fit: contain;
        margin: 0 auto 10px auto;
        display: block;
        background: #ffffff;
        border-radius: 16px;
        padding: 8px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    }

    /* ---------- Poster banner (menggantikan hero jika ada) ---------- */
    .poster-banner {
        width: 100%;
        border-radius: 22px;
        display: block;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(11,61,145,0.3);
        object-fit: cover;
    }
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
    
    /* ---------- Radio button styling ---------- */
    .stRadio > div {
        gap: 12px;
    }
    .stRadio label {
        background: #f2f8fc;
        padding: 10px 20px;
        border-radius: 12px;
        border: 2px solid #d7e6f2;
        transition: all 0.2s ease;
        font-weight: 600 !important;
        color: #0f2436 !important;
    }
    .stRadio label:hover {
        background: #e6f1fb;
        border-color: #0d6efd;
    }
    .stRadio label[data-baseweb="radio"] {
        background: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
if poster_data_uri:
    # Poster menggantikan banner biru sepenuhnya
    st.markdown(f"""
    <img src="{poster_data_uri}" class="poster-banner" alt="poster">
    """, unsafe_allow_html=True)
else:
    if logo_data_uri:
        header_icon_html = f'<img src="{logo_data_uri}" class="logo" alt="logo">'
    else:
        header_icon_html = '<span class="emoji">🏫</span>'

    st.markdown(f"""
    <div class="hero">
        {header_icon_html}
        <h1>Pendaftaran Kursus</h1>
        <p>📱 Isi data anaknya ya, Bu/Pak. Boleh pilih lebih dari 1 program.</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PILIHAN ONLINE/OFFLINE
# =========================================================
with card():
    st.markdown('<div class="section-title">🌐 Metode Pembelajaran</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Pilih metode pembelajaran yang diinginkan</div>', unsafe_allow_html=True)
    
    metode = st.radio(
        "Pilih metode pembelajaran *",
        ["Online (Via Zoom/Google Meet)", "Offline (Tatap Muka)"],
        index=0,
        horizontal=True
    )

# =========================================================
# BAGIAN 1: DATA DIRI (ADAPTIF)
# =========================================================
with card():
    st.markdown('<div class="section-title">👤 Data Diri</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Kolom bertanda <span class="required">*</span> wajib diisi</div>', unsafe_allow_html=True)

    # Cek kondisi
    is_offline = metode == "Offline (Tatap Muka)"
    is_umum = False
    
    nama = st.text_input("Nama Lengkap *", placeholder="Contoh: Ahmad Fauzi")
    nama_panggilan = st.text_input("Nama Panggilan (opsional)", placeholder="Contoh: Ahmad")
    
    # Form adaptif berdasarkan mode
    if is_offline:
        # Offline mode - cek apakah memilih UMUM
        # Tampilkan pilihan sekolah/kelas dulu untuk menentukan
        sekolah_kelas_temp = st.selectbox(
            "Sekolah & Kelas *",
            ["Pilih...", "SD Kelas 1", "SD Kelas 2", "SD Kelas 3", "SD Kelas 4", "SD Kelas 5", "SD Kelas 6",
             "SMP Kelas 1", "SMP Kelas 2", "SMP Kelas 3", "SMA/SMK", "UMUM"],
            key="sekolah_temp"
        )
        is_umum = sekolah_kelas_temp == "UMUM"
        
        if is_umum:
            # UMUM - tidak perlu data orang tua
            st.info("📌 Pendaftaran untuk umum (dewasa) - tidak perlu data orang tua")
            orang_tua = "-"  # Tidak diperlukan
            
            col1, col2 = st.columns(2)
            with col1:
                wa = st.text_input("No. WhatsApp *", placeholder="81234567890")
            with col2:
                alamat = st.text_input("Alamat (RT / Dusun) *", placeholder="Contoh: RT 02, Krajan")
            
            # Simpan pilihan untuk digunakan di bagian selanjutnya
            sekolah_kelas = sekolah_kelas_temp
        else:
            # Bukan UMUM - tetap pakai data orang tua
            orang_tua = st.text_input("Nama Orang Tua / Wali *", placeholder="Contoh: Bapak Slamet")
            
            col1, col2 = st.columns(2)
            with col1:
                wa = st.text_input("No. WhatsApp Orang Tua *", placeholder="81234567890")
            with col2:
                alamat = st.text_input("Alamat (RT / Dusun) *", placeholder="Contoh: RT 02, Krajan")
            
            sekolah_kelas = sekolah_kelas_temp
    else:
        # Online mode
        peserta = st.radio(
            "Pendaftaran untuk *",
            ["Anak", "Diri Sendiri"],
            index=0,
            horizontal=True
        )
        
        if peserta == "Anak":
            orang_tua = st.text_input("Nama Orang Tua / Wali *", placeholder="Contoh: Bapak Slamet")
            col1, col2 = st.columns(2)
            with col1:
                wa = st.text_input("No. WhatsApp Orang Tua *", placeholder="81234567890")
            with col2:
                alamat = st.text_input("Alamat (RT / Dusun) *", placeholder="Contoh: RT 02, Krajan")
            
            # Pilih sekolah/kelas
            sekolah_kelas = st.selectbox(
                "Sekolah & Kelas *",
                ["Pilih...", "SD Kelas 1", "SD Kelas 2", "SD Kelas 3", "SD Kelas 4", "SD Kelas 5", "SD Kelas 6",
                 "SMP Kelas 1", "SMP Kelas 2", "SMP Kelas 3", "SMA/SMK", "UMUM"]
            )
            is_umum = sekolah_kelas == "UMUM"
        else:
            # Diri sendiri - tidak perlu data orang tua
            orang_tua = "-"  # Tidak diperlukan
            col1, col2 = st.columns(2)
            with col1:
                wa = st.text_input("No. WhatsApp *", placeholder="81234567890")
            with col2:
                alamat = st.text_input("Alamat (RT / Dusun) *", placeholder="Contoh: RT 02, Krajan")
            
            # Pilihan status untuk dewasa
            sekolah_kelas = st.selectbox(
                "Status *",
                ["Pilih...", "Pelajar/Mahasiswa", "Karyawan", "Wiraswasta", "Ibu Rumah Tangga", "Lainnya"]
            )
            is_umum = True  # Untuk dewasa, selalu dianggap "UMUM"

# =========================================================
# BAGIAN 2: DATA PENDUKUNG
# =========================================================
with card():
    st.markdown('<div class="section-title">📚 Data Pendukung</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Membantu kami menyesuaikan kelas</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        # Tampilkan kembali pilihan sekolah/kelas jika offline dan belum dipilih
        if is_offline and 'sekolah_kelas_temp' in locals():
            # Sudah dipilih di atas
            pass
        else:
            # Untuk online, sudah dipilih di atas
            pass
        
        # Untuk offline + UMUM, atau online + diri sendiri, status sudah dipilih
        if is_offline and is_umum:
            # Status sudah dipilih (UMUM) - tampilkan sebagai info
            st.markdown(f'<div class="muted-box">ℹ️ Status: {sekolah_kelas}</div>', unsafe_allow_html=True)
        elif not is_offline and peserta == "Diri Sendiri":
            st.markdown(f'<div class="muted-box">ℹ️ Status: {sekolah_kelas}</div>', unsafe_allow_html=True)
    
    with col4:
        # Pekerjaan adaptif
        if is_offline:
            if is_umum:
                # Offline + UMUM - pekerjaan sendiri
                pekerjaan_ortu = st.selectbox(
                    "Pekerjaan *",
                    ["Pilih...", "Pelajar/Mahasiswa", "Karyawan", "Wiraswasta", "Ibu Rumah Tangga", "Lainnya"]
                )
            else:
                # Offline + anak - pekerjaan orang tua
                pekerjaan_ortu = st.selectbox(
                    "Pekerjaan Orang Tua",
                    ["Pilih...", "Petani/Berkebun", "Buruh Tani", "Pedagang/Jualan", "Karyawan/PNS", "Ibu Rumah Tangga", "Lainnya"]
                )
        else:
            if peserta == "Anak":
                # Online untuk anak: pekerjaan orang tua
                pekerjaan_ortu = st.selectbox(
                    "Pekerjaan Orang Tua",
                    ["Pilih...", "Petani/Berkebun", "Buruh Tani", "Pedagang/Jualan", "Karyawan/PNS", "Ibu Rumah Tangga", "Lainnya"]
                )
            else:
                # Diri sendiri: pekerjaan sendiri
                pekerjaan_ortu = st.selectbox(
                    "Pekerjaan *",
                    ["Pilih...", "Pelajar/Mahasiswa", "Karyawan", "Wiraswasta", "Ibu Rumah Tangga", "Lainnya"]
                )

    pekerjaan_ortu_lainnya = ""
    if pekerjaan_ortu == "Lainnya":
        if is_offline and is_umum:
            label = "Sebutkan pekerjaan *"
        elif is_offline and not is_umum:
            label = "Sebutkan pekerjaan orang tua *"
        elif not is_offline and peserta == "Anak":
            label = "Sebutkan pekerjaan orang tua *"
        else:
            label = "Sebutkan pekerjaan *"
        
        pekerjaan_ortu_lainnya = st.text_input(
            label,
            placeholder="Contoh: Tukang Ojek, Wiraswasta, dll."
        )

# =========================================================
# BAGIAN 3: PILIHAN PROGRAM
# =========================================================
with card():
    st.markdown('<div class="section-title">🎯 Pilih Program Kursus</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Centang semua program yang ingin diikuti</div>', unsafe_allow_html=True)

    cek_program_a = st.checkbox("💻 Program MATH DROP-IN")
    cek_program_b = st.checkbox("🎨 Program ENGLISH FOR KIDS")
    cek_program_c = st.checkbox("📖 Program ENGLISH FOR TEENS")
    cek_program_d = st.checkbox("✏️ Program PREMIUM MATH")
    cek_program_e = st.checkbox("📚 Program CALISTUNG")
    cek_program_f = st.checkbox("🌍 Program GENERAL ENGLISH")  # Program baru

    programs = []
    if cek_program_a: programs.append("Program MATH DROP-IN")
    if cek_program_b: programs.append("Program ENGLISH FOR KIDS")
    if cek_program_c: programs.append("Program ENGLISH FOR TEENS")
    if cek_program_d: programs.append("Program PREMIUM MATH")
    if cek_program_e: programs.append("Program CALISTUNG")
    if cek_program_f: programs.append("Program GENERAL ENGLISH")

    if programs:
        st.markdown(f'<div class="ok-box">✅ {len(programs)} program dipilih</div>', unsafe_allow_html=True)

# =========================================================
# BAGIAN 4: JADWAL PROGRAM A (MUNCUL OTOMATIS)
# =========================================================
jadwal_a = []
if cek_program_a:
    with card():
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
# Tentukan field wajib berdasarkan mode
required_fields = [nama, wa, alamat]
if is_offline and is_umum:
    # Offline + UMUM: tidak perlu orang tua
    pass
elif is_offline and not is_umum:
    # Offline + anak: butuh orang tua
    required_fields.append(orang_tua)
elif not is_offline and peserta == "Anak":
    # Online + anak: butuh orang tua
    required_fields.append(orang_tua)
else:
    # Online + diri sendiri: tidak perlu orang tua
    pass

filled = sum(1 for f in required_fields if str(f).strip())
if sekolah_kelas != "Pilih..." and sekolah_kelas != "Pilih...":
    filled += 1
if programs:
    filled += 1
total_steps = len(required_fields) + 2
pct = int((filled / total_steps) * 100) if total_steps > 0 else 0

st.markdown(f"""
<div class="progress-wrap">
    <div class="progress-label"><span>Kelengkapan formulir</span><span>{pct}%</span></div>
</div>
""", unsafe_allow_html=True)
st.progress(pct / 100 if pct > 0 else 0)

# =========================================================
# TOMBOL SUBMIT & SIMPAN DATA
# =========================================================
if "duplikat_data" not in st.session_state:
    st.session_state.duplikat_data = None

submitted = st.button("✅ Daftar Sekarang", type="primary", use_container_width=True)

if submitted:
    # Validasi berdasarkan mode
    errors = []
    
    if not nama:
        errors.append("Nama Lengkap wajib diisi")
    if not wa:
        errors.append("Nomor WhatsApp wajib diisi")
    if not alamat:
        errors.append("Alamat wajib diisi")
    
    # Validasi orang tua (kecuali offline+UMUM atau online+diri sendiri)
    if is_offline and is_umum:
        # Tidak perlu orang tua
        pass
    elif is_offline and not is_umum:
        if not orang_tua or orang_tua == "-":
            errors.append("Nama Orang Tua/Wali wajib diisi")
    elif not is_offline and peserta == "Anak":
        if not orang_tua or orang_tua == "-":
            errors.append("Nama Orang Tua/Wali wajib diisi")
    
    if sekolah_kelas == "Pilih..." or not sekolah_kelas:
        errors.append("Pilih status/sekolah terlebih dahulu")
    if pekerjaan_ortu == "Pilih...":
        errors.append("Pilih pekerjaan terlebih dahulu")
    if pekerjaan_ortu == "Lainnya" and not pekerjaan_ortu_lainnya.strip():
        errors.append("Mohon isi kolom pekerjaan lainnya")
    if len(programs) == 0:
        errors.append("Pilih minimal 1 program kursus")
    if cek_program_a and len(jadwal_a) == 0:
        errors.append("Anda memilih Program MATH DROP-IN, tapi belum memilih jadwal. Centang minimal 1.")
    
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
    else:
        pekerjaan_final = pekerjaan_ortu_lainnya.strip() if pekerjaan_ortu == "Lainnya" else pekerjaan_ortu

        data_pendaftar = {
            "tanggal_daftar": format_tanggal_indonesia(datetime.now()),
            "metode": metode,
            "nama_lengkap": nama,
            "nama_panggilan": nama_panggilan if nama_panggilan else "-",
            "orang_tua": orang_tua if orang_tua else "-",
            "no_wa": wa,
            "alamat": alamat,
            "sekolah_kelas": sekolah_kelas,
            "pekerjaan_ortu": pekerjaan_final,
            "program_dipilih": ", ".join(programs),
            "jadwal_a": ", ".join(jadwal_a) if jadwal_a else "-"
        }

        # Cek apakah kombinasi Nama Siswa + No. WhatsApp ini sudah pernah terdaftar
        data_lama = cek_data_existing(nama, wa)

        if data_lama is None:
            # Belum pernah daftar -> simpan sebagai data baru
            try:
                response = simpan_data_baru(data_pendaftar)
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
        else:
            # Nama Siswa + No. WA sudah pernah terdaftar -> simpan sementara, minta konfirmasi update
            st.session_state.duplikat_data = {
                "data_baru": data_pendaftar,
                "nama_lama": data_lama.get("nama_lengkap", "-"),
                # Pakai nilai PERSIS dari sheet (bukan input form) agar filter update pasti cocok
                "nama_lengkap": data_lama.get("nama_lengkap", nama),
                "no_wa": data_lama.get("no_wa", wa)
            }

# ---------- Konfirmasi jika ditemukan data duplikat ----------
if st.session_state.duplikat_data:
    dup = st.session_state.duplikat_data
    with card():
        st.markdown(
            f'<div class="warn-box">⚠️ Siswa <b>{dup["nama_lama"]}</b> dengan nomor WhatsApp ini sudah pernah '
            f'terdaftar sebelumnya. Data lama akan diganti (replace) jika Anda memilih "Update Data".</div>',
            unsafe_allow_html=True
        )
        colA, colB = st.columns(2)
        with colA:
            konfirmasi_update = st.button("🔄 Ya, Update Data", use_container_width=True)
        with colB:
            batal_update = st.button("✖️ Batal", use_container_width=True)

        if konfirmasi_update:
            try:
                response = update_data_lama(dup["nama_lengkap"], dup["no_wa"], dup["data_baru"])
                if response.status_code in [200, 201]:
                    st.success(f"✅ Data **{dup['data_baru']['nama_lengkap']}** berhasil diperbarui.")
                    st.balloons()
                else:
                    st.error(f"❌ Gagal update data. Status: {response.status_code}")
                    st.json(dup["data_baru"])
            except Exception as e:
                st.error(f"❌ Error koneksi: {e}")
                st.json(dup["data_baru"])
            st.session_state.duplikat_data = None

        if batal_update:
            st.info("Pendaftaran dibatalkan. Data lama tidak diubah.")
            st.session_state.duplikat_data = None

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer-note">
    <hr style="border: none; border-top: 1px solid #dfe6ee; margin-bottom: 12px;">
    Made with ❤️ untuk warga kampung
</div>
""", unsafe_allow_html=True)