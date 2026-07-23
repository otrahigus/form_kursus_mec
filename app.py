import streamlit as st
from datetime import datetime
import base64
import os
from supabase import create_client, Client

# =========================================================
# KONFIGURASI SUPABASE (DARI SECRETS)
# =========================================================
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except:
    SUPABASE_URL = None
    SUPABASE_KEY = None

# =========================================================
# KONFIGURASI HEADER
# =========================================================
LOGO_PATH = "logo.png"
POSTER_PATH = "poster.png"

def get_logo_base64(path):
    """Baca file gambar & ubah ke base64"""
    if path and os.path.exists(path):
        try:
            with open(path, "rb") as f:
                data = f.read()
            ext = path.split(".")[-1].lower()
            mime = "image/png" if ext == "png" else "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"
            return f"data:{mime};base64,{base64.b64encode(data).decode()}"
        except:
            return None
    return None

logo_exists = os.path.exists(LOGO_PATH)
poster_exists = os.path.exists(POSTER_PATH)

logo_data_uri = get_logo_base64(LOGO_PATH) if logo_exists else None
poster_data_uri = get_logo_base64(POSTER_PATH) if poster_exists else None

BULAN_ID = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

def format_tanggal_indonesia(dt):
    return f"{dt.day:02d} {BULAN_ID[dt.month - 1]} {dt.year} {dt.strftime('%H:%M:%S')}"

def normalisasi_teks(s):
    return " ".join((s or "").strip().lower().split())

# =========================================================
# FUNGSI SUPABASE
# =========================================================
@st.cache_resource
def init_supabase():
    try:
        if not SUPABASE_URL or not SUPABASE_KEY:
            return None, "SUPABASE_URL atau SUPABASE_KEY tidak ditemukan!"
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase, None
    except Exception as e:
        return None, str(e)

supabase, error_msg = init_supabase()

def cek_data_existing(nama_lengkap, no_wa):
    if not supabase:
        return None
    try:
        response = supabase.table('form_kursus_mec')\
            .select('*')\
            .eq('no_wa', str(no_wa))\
            .execute()
        if not response.data:
            return None
        target_nama = normalisasi_teks(nama_lengkap)
        for row in response.data:
            if normalisasi_teks(row.get('nama_lengkap', '')) == target_nama:
                return row
        return None
    except Exception as e:
        return None

def simpan_data_baru(data_pendaftar):
    if not supabase:
        return None, "Supabase tidak terkoneksi"
    try:
        data_pendaftar['created_at'] = datetime.now().isoformat()
        response = supabase.table('form_kursus_mec')\
            .insert(data_pendaftar)\
            .execute()
        if response.data:
            return response, None
        else:
            return None, "Gagal menyimpan data"
    except Exception as e:
        return None, str(e)

def update_data_lama(nama_lengkap, no_wa, data_pendaftar):
    if not supabase:
        return None, "Supabase tidak terkoneksi"
    try:
        response = supabase.table('form_kursus_mec')\
            .update(data_pendaftar)\
            .eq('no_wa', str(no_wa))\
            .eq('nama_lengkap', nama_lengkap)\
            .execute()
        if response.data:
            return response, None
        else:
            return None, "Gagal update data"
    except Exception as e:
        return None, str(e)

# =========================================================
# STREAMLIT CONFIG
# =========================================================
st.set_page_config(
    page_title="Pendaftaran Kursus",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
    .stApp {
        background: linear-gradient(160deg, #e6f1fb 0%, #e5f6ee 100%);
    }
    #MainMenu, footer {visibility: hidden;}
    div.block-container {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 640px;
    }
    html, body, [class^="css"], .stMarkdown, .stMarkdown p,
    div[data-testid="stMarkdownContainer"] p {
        color: #0f2436 !important;
    }
    .hero {
        background: linear-gradient(135deg, #0b3d91 0%, #0d6efd 55%, #00897b 100%);
        padding: 34px 24px 30px 24px;
        border-radius: 22px;
        text-align: center;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(11,61,145,0.3);
    }
    .hero .emoji { 
        font-size: 3.5rem; 
        display:block; 
        margin-bottom: 10px;
        line-height: 1;
    }
    .hero .logo {
        width: 80px;
        height: 80px;
        object-fit: contain;
        margin: 0 auto 12px auto;
        display: block;
        background: #ffffff;
        border-radius: 16px;
        padding: 10px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    }
    .poster-banner {
        width: 100%;
        border-radius: 22px;
        display: block;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(11,61,145,0.3);
        object-fit: cover;
        max-height: 300px;
    }
    .hero h1 {
        color: #ffffff !important;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0 0 8px 0;
        letter-spacing: -0.5px;
    }
    .hero p {
        color: #ffffff !important;
        font-size: 1rem;
        margin: 0;
        line-height: 1.5;
        opacity: 0.95;
    }
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
    div[data-testid="stWidgetLabel"] p {
        color: #0f2436 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }
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
    .file-info {
        background: #fff8e1;
        border-left: 4px solid #f9a825;
        padding: 10px 14px;
        border-radius: 8px;
        margin-top: 8px;
        font-size: 0.85rem;
        color: #5d4037 !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
try:
    if poster_data_uri:
        st.markdown(f"""
        <img src="{poster_data_uri}" class="poster-banner" alt="poster banner">
        """, unsafe_allow_html=True)
    else:
        if logo_data_uri:
            header_icon_html = f'<img src="{logo_data_uri}" class="logo" alt="logo">'
        else:
            header_icon_html = '<span class="emoji">🏫</span>'
            if not logo_exists:
                st.markdown(
                    '<div class="file-info">ℹ️ File <code>logo.png</code> tidak ditemukan. '
                    'Menggunakan emoji sebagai pengganti. Upload file logo.png untuk tampilan lebih baik.</div>',
                    unsafe_allow_html=True
                )

        st.markdown(f"""
        <div class="hero">
            {header_icon_html}
            <h1>Pendaftaran Kursus</h1>
            <p>📱 Isi data pendaftar. Boleh pilih lebih dari 1 program.</p>
        </div>
        """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error di header: {e}")

# =========================================================
# CEK KONEKSI SUPABASE (TAPI TIDAK MENGHENTIKAN APLIKASI)
# =========================================================
if not supabase:
    st.warning(f"⚠️ Koneksi ke Supabase: {error_msg if error_msg else 'Gagal terhubung'}")
    st.info("📌 Data akan tetap bisa diisi, tetapi tidak akan tersimpan ke database. Periksa konfigurasi Secrets di Streamlit Cloud.")

# =========================================================
# MULAI FORM
# =========================================================
try:
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
            horizontal=True,
            key="metode"
        )

    is_offline = metode == "Offline (Tatap Muka)"

    # =========================================================
    # BAGIAN 1: DATA DIRI
    # =========================================================
    with card():
        st.markdown('<div class="section-title">👤 Data Diri</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Kolom bertanda <span class="required">*</span> wajib diisi</div>', unsafe_allow_html=True)

        nama = st.text_input("Nama Lengkap *", placeholder="Contoh: Ahmad Fauzi", key="nama")
        nama_panggilan = st.text_input("Nama Panggilan (opsional)", placeholder="Contoh: Ahmad", key="nama_panggilan")
        
        if is_offline:
            sekolah_kelas = st.selectbox(
                "Sekolah & Kelas *",
                ["Pilih...", "SD Kelas 1", "SD Kelas 2", "SD Kelas 3", "SD Kelas 4", "SD Kelas 5", "SD Kelas 6",
                 "SMP Kelas 1", "SMP Kelas 2", "SMP Kelas 3", "SMA/SMK", "UMUM"],
                key="sekolah_kelas_offline"
            )
            is_umum = sekolah_kelas == "UMUM"
            is_diri_sendiri = False
            
            if is_umum:
                st.info("📌 Pendaftaran untuk umum (dewasa) - tidak perlu data orang tua")
                orang_tua = "-"
                
                col1, col2 = st.columns(2)
                with col1:
                    wa = st.text_input("No. WhatsApp *", placeholder="81234567890", key="wa_offline_umum")
                with col2:
                    alamat = st.text_input("Alamat (RT / Dusun) *", placeholder="Contoh: RT 02, Krajan", key="alamat_offline_umum")
            else:
                orang_tua = st.text_input("Nama Orang Tua / Wali *", placeholder="Contoh: Bapak Slamet", key="orang_tua_offline")
                
                col1, col2 = st.columns(2)
                with col1:
                    wa = st.text_input("No. WhatsApp Orang Tua *", placeholder="81234567890", key="wa_offline")
                with col2:
                    alamat = st.text_input("Alamat (RT / Dusun) *", placeholder="Contoh: RT 02, Krajan", key="alamat_offline")
            
        else:
            peserta = st.radio(
                "Pendaftaran untuk *",
                ["Anak", "Diri Sendiri"],
                index=0,
                horizontal=True,
                key="peserta"
            )
            
            if peserta == "Anak":
                sekolah_kelas = st.selectbox(
                    "Sekolah & Kelas *",
                    ["Pilih...", "SD Kelas 1", "SD Kelas 2", "SD Kelas 3", "SD Kelas 4", "SD Kelas 5", "SD Kelas 6",
                     "SMP Kelas 1", "SMP Kelas 2", "SMP Kelas 3", "SMA/SMK", "UMUM"],
                    key="sekolah_kelas_online_anak"
                )
                is_umum = sekolah_kelas == "UMUM"
                is_diri_sendiri = False
                
                if is_umum:
                    st.info("📌 Pendaftaran untuk umum (dewasa) - tidak perlu data orang tua")
                    orang_tua = "-"
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        wa = st.text_input("No. WhatsApp *", placeholder="81234567890", key="wa_online_anak_umum")
                    with col2:
                        alamat = st.text_input("Alamat (RT / Dusun) *", placeholder="Contoh: RT 02, Krajan", key="alamat_online_anak_umum")
                else:
                    orang_tua = st.text_input("Nama Orang Tua / Wali *", placeholder="Contoh: Bapak Slamet", key="orang_tua_online_anak")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        wa = st.text_input("No. WhatsApp Orang Tua *", placeholder="81234567890", key="wa_online_anak")
                    with col2:
                        alamat = st.text_input("Alamat (RT / Dusun) *", placeholder="Contoh: RT 02, Krajan", key="alamat_online_anak")
                
            else:
                is_diri_sendiri = True
                is_umum = True
                orang_tua = "-"
                
                sekolah_kelas = st.selectbox(
                    "Status / Pekerjaan *",
                    ["Pilih...", "Pelajar/Mahasiswa", "Karyawan", "Wiraswasta", "Ibu Rumah Tangga", "Lainnya"],
                    key="status_pekerjaan"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    wa = st.text_input("No. WhatsApp *", placeholder="81234567890", key="wa_diri")
                with col2:
                    alamat = st.text_input("Alamat (RT / Dusun) *", placeholder="Contoh: RT 02, Krajan", key="alamat_diri")

    # =========================================================
    # BAGIAN 2: DATA PENDUKUNG (HANYA UNTUK ANAK NON-UMUM)
    # =========================================================
    pekerjaan_ortu = None
    pekerjaan_ortu_lainnya = ""

    if not is_diri_sendiri and not is_umum:
        with card():
            st.markdown('<div class="section-title">📚 Data Pendukung</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">Membantu kami menyesuaikan kelas</div>', unsafe_allow_html=True)

            col3, col4 = st.columns(2)
            with col3:
                if sekolah_kelas and sekolah_kelas != "Pilih...":
                    st.markdown(f'<div class="muted-box">ℹ️ Sekolah/Kelas: {sekolah_kelas}</div>', unsafe_allow_html=True)
            
            with col4:
                pekerjaan_ortu = st.selectbox(
                    "Pekerjaan Orang Tua",
                    ["Pilih...", "Petani/Berkebun", "Buruh Tani", "Pedagang/Jualan", "Karyawan/PNS", "Ibu Rumah Tangga", "Lainnya"],
                    key="pekerjaan_ortu"
                )

            if pekerjaan_ortu == "Lainnya":
                pekerjaan_ortu_lainnya = st.text_input(
                    "Sebutkan pekerjaan orang tua *",
                    placeholder="Contoh: Tukang Ojek, Wiraswasta, dll.",
                    key="pekerjaan_ortu_lainnya"
                )

    # =========================================================
    # BAGIAN 3: PILIHAN PROGRAM
    # =========================================================
    with card():
        st.markdown('<div class="section-title">🎯 Pilih Program Kursus</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Centang semua program yang ingin diikuti</div>', unsafe_allow_html=True)

        cek_program_a = st.checkbox("💻 Program MATH DROP-IN", key="prog_a")
        cek_program_b = st.checkbox("🎨 Program ENGLISH FOR KIDS", key="prog_b")
        cek_program_c = st.checkbox("📖 Program ENGLISH FOR TEENS", key="prog_c")
        cek_program_d = st.checkbox("✏️ Program PREMIUM MATH", key="prog_d")
        cek_program_e = st.checkbox("📚 Program CALISTUNG", key="prog_e")
        cek_program_f = st.checkbox("🌍 Program GENERAL ENGLISH", key="prog_f")

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
    # BAGIAN 4: JADWAL MATH DROP-IN
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
            for idx, (label, value) in enumerate(sesi_list):
                if st.checkbox(label, key=f"jadwal_{idx}"):
                    jadwal_a.append(value)

            if len(jadwal_a) == 0:
                st.markdown('<div class="warn-box">⚠️ Belum ada jadwal dipilih. Centang minimal 1.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ok-box">✅ {len(jadwal_a)} jadwal dipilih</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="muted-box">ℹ️ Bagian jadwal akan muncul otomatis jika Anda memilih Program MATH DROP-IN.</div>', unsafe_allow_html=True)

    st.write("")

    # =========================================================
    # PROGRESS INDIKATOR
    # =========================================================
    required_fields = [nama, wa, alamat]

    if not is_umum and not is_diri_sendiri:
        required_fields.append(orang_tua)

    if sekolah_kelas and sekolah_kelas != "Pilih...":
        filled = sum(1 for f in required_fields if str(f).strip())
        filled += 1
    else:
        filled = sum(1 for f in required_fields if str(f).strip())

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
    # TOMBOL SUBMIT
    # =========================================================
    if "duplikat_data" not in st.session_state:
        st.session_state.duplikat_data = None

    submitted = st.button("✅ Daftar Sekarang", type="primary", use_container_width=True)

    if submitted:
        errors = []
        
        if not nama:
            errors.append("Nama Lengkap wajib diisi")
        if not wa:
            errors.append("Nomor WhatsApp wajib diisi")
        if not alamat:
            errors.append("Alamat wajib diisi")
        
        if not is_umum and not is_diri_sendiri:
            if not orang_tua or orang_tua == "-":
                errors.append("Nama Orang Tua/Wali wajib diisi")
        
        if not sekolah_kelas or sekolah_kelas == "Pilih...":
            errors.append("Pilih Sekolah/Kelas atau Status/Pekerjaan terlebih dahulu")
        
        if not is_diri_sendiri and not is_umum:
            if pekerjaan_ortu == "Pilih..." or not pekerjaan_ortu:
                errors.append("Pilih pekerjaan orang tua terlebih dahulu")
            if pekerjaan_ortu == "Lainnya" and not pekerjaan_ortu_lainnya.strip():
                errors.append("Mohon isi kolom pekerjaan orang tua lainnya")
        
        if len(programs) == 0:
            errors.append("Pilih minimal 1 program kursus")
        if cek_program_a and len(jadwal_a) == 0:
            errors.append("Anda memilih Program MATH DROP-IN, tapi belum memilih jadwal. Centang minimal 1.")
        
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            if is_diri_sendiri:
                pekerjaan_final = sekolah_kelas
            elif is_umum:
                pekerjaan_final = "UMUM"
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
                "jadwal_a": ", ".join(jadwal_a) if jadwal_a else "-",
                "tipe_pendaftar": "Diri Sendiri" if is_diri_sendiri else "Anak",
                "status_umum": "Ya" if is_umum else "Tidak"
            }

            # Cek Supabase connection
            if not supabase:
                st.error("❌ Tidak dapat menyimpan data. Supabase tidak terhubung.")
                st.info("📌 Data yang akan disimpan:")
                st.json(data_pendaftar)
            else:
                data_lama = cek_data_existing(nama, wa)

                if data_lama is None:
                    response, error = simpan_data_baru(data_pendaftar)
                    if error is None:
                        st.success(f"✅ Pendaftaran **{nama}** berhasil! Data sudah tersimpan.")
                        st.balloons()
                    else:
                        st.error(f"❌ Gagal simpan data: {error}")
                        st.json(data_pendaftar)
                else:
                    st.session_state.duplikat_data = {
                        "data_baru": data_pendaftar,
                        "nama_lama": data_lama.get("nama_lengkap", "-"),
                        "nama_lengkap": data_lama.get("nama_lengkap", nama),
                        "no_wa": data_lama.get("no_wa", wa)
                    }

    # =========================================================
    # KONFIRMASI DUPLIKAT
    # =========================================================
    if st.session_state.duplikat_data:
        dup = st.session_state.duplikat_data
        with card():
            st.markdown(
                f'<div class="warn-box">⚠️ Pendaftar <b>{dup["nama_lama"]}</b> dengan nomor WhatsApp ini sudah pernah '
                f'terdaftar sebelumnya. Data lama akan diganti (replace) jika Anda memilih "Update Data".</div>',
                unsafe_allow_html=True
            )
            colA, colB = st.columns(2)
            with colA:
                konfirmasi_update = st.button("🔄 Ya, Update Data", use_container_width=True)
            with colB:
                batal_update = st.button("✖️ Batal", use_container_width=True)

            if konfirmasi_update:
                response, error = update_data_lama(
                    dup["nama_lengkap"], 
                    dup["no_wa"], 
                    dup["data_baru"]
                )
                if error is None:
                    st.success(f"✅ Data **{dup['data_baru']['nama_lengkap']}** berhasil diperbarui.")
                    st.balloons()
                else:
                    st.error(f"❌ Gagal update data: {error}")
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

except Exception as e:
    st.error(f"❌ Terjadi error pada form: {str(e)}")
    st.info("""
    📌 **Cara Debug:**
    1. Cek logs di Streamlit Cloud dashboard
    2. Pastikan semua file sudah di-commit ke GitHub
    3. Periksa konfigurasi Secrets
    """)