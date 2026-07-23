import streamlit as st
from datetime import datetime
import base64
import os
from supabase import create_client, Client

# =========================================================
# KONFIGURASI SUPABASE (DARI SECRETS)
# =========================================================
# Ambil dari secrets.toml (Streamlit Cloud) atau environment variables
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except:
    # Fallback untuk development lokal (gunakan .env)
    import os
    from dotenv import load_dotenv
    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# =========================================================
# KONFIGURASI LAINNYA
# =========================================================
LOGO_PATH = "logo.png"
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
    return f"{dt.day:02d} {BULAN_ID[dt.month - 1]} {dt.year} {dt.strftime('%H:%M:%S')}"

def normalisasi_teks(s):
    return " ".join((s or "").strip().lower().split())

# =========================================================
# FUNGSI SUPABASE
# =========================================================
@st.cache_resource
def init_supabase():
    """Inisialisasi koneksi Supabase"""
    try:
        if not SUPABASE_URL or not SUPABASE_KEY:
            st.error("❌ SUPABASE_URL atau SUPABASE_KEY tidak ditemukan!")
            return None
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase
    except Exception as e:
        st.error(f"❌ Gagal konek ke Supabase: {e}")
        return None

supabase = init_supabase()

def cek_data_existing(nama_lengkap, no_wa):
    """Cek ke Supabase apakah kombinasi Nama + No. WA sudah pernah terdaftar."""
    if not supabase:
        return None
    
    try:
        response = supabase.table('pendaftaran')\
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
        st.warning(f"⚠️ Gagal cek data: {e}")
        return None

def simpan_data_baru(data_pendaftar):
    """Simpan data baru ke Supabase"""
    if not supabase:
        return None, "Supabase tidak terkoneksi"
    
    try:
        data_pendaftar['created_at'] = datetime.now().isoformat()
        
        response = supabase.table('pendaftaran')\
            .insert(data_pendaftar)\
            .execute()
        
        if response.data:
            return response, None
        else:
            return None, "Gagal menyimpan data"
    except Exception as e:
        return None, str(e)

def update_data_lama(nama_lengkap, no_wa, data_pendaftar):
    """Update data lama di Supabase"""
    if not supabase:
        return None, "Supabase tidak terkoneksi"
    
    try:
        response = supabase.table('pendaftaran')\
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
# CSS (SAMA SEPERTI SEBELUMNYA)
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
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
if poster_data_uri:
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
        <p>📱 Isi data pendaftar. Boleh pilih lebih dari 1 program.</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# CEK KONEKSI SUPABASE
# =========================================================
if not supabase:
    st.error("❌ Tidak dapat terhubung ke Supabase. Periksa URL dan Key Anda di Secrets.")
    st.info("""
    📌 **Cara Setup Secrets di Streamlit Cloud:**
    1. Buka dashboard Streamlit Cloud
    2. Pilih app Anda
    3. Klik menu "Settings" → "Secrets"
    4. Tambahkan:
""")
st.stop()