# 🏫 Form Pendaftaran Kursus

Link Akses : https://form-kursus-mec.streamlit.app

Aplikasi web sederhana berbasis **Streamlit** untuk pendaftaran kursus (MATH DROP-IN, English for Kids, English for Teens, Premium Math). Data pendaftar otomatis tersimpan ke **Google Sheets** lewat [sheet.best](https://sheet.best).

Dibuat untuk memudahkan warga kampung mendaftarkan anaknya lewat HP, tanpa perlu install aplikasi apa pun — cukup buka link di browser.

---

## ✨ Fitur

- 📝 Form pendaftaran dengan data diri siswa, data pendukung, dan pilihan program kursus
- ✅ Bisa memilih lebih dari 1 program sekaligus
- 📅 Jadwal sesi otomatis muncul jika memilih Program **MATH DROP-IN**
- ✍️ Kolom isian bebas otomatis muncul jika Pekerjaan Orang Tua memilih **"Lainnya"**
- 📊 Indikator progres kelengkapan formulir
- 🔁 **Deteksi duplikat pintar**: kombinasi *Nama Siswa + No. WhatsApp* dicek sebelum simpan
  - Kakak-adik yang memakai nomor WA orang tua yang sama tetap bisa daftar masing-masing
  - Pencocokan nama toleran terhadap huruf besar/kecil dan spasi berlebih
  - Jika terdeteksi sudah pernah daftar, muncul opsi **Update Data** (replace) atau **Batal**
- 🗓️ Format tanggal aman dari auto-convert Google Sheets (mis. `02 Juli 2026 14:23:11`)
- 🖼️ Mendukung logo & poster/banner kustom (opsional)
- 🎨 Tampilan responsif untuk HP, dengan tema warna biru–hijau–putih yang kontras dan mudah dibaca

---

## 📂 Struktur Project

```
.
├── form_pendaftaran.py    # Aplikasi utama Streamlit
├── requirements.txt        # Daftar dependency Python
├── logo.png                 # (opsional) logo, tampil di header
├── poster.png                # (opsional) poster/banner, menggantikan header biru
└── README.md
```

> File `logo.png` dan `poster.png` bersifat **opsional**. Jika tidak ada, aplikasi tetap berjalan normal dengan tampilan default (emoji 🏫 dan banner biru gradient).

---

## 🚀 Instalasi & Menjalankan Secara Lokal

### 1. Clone repo ini

```bash
git clone https://github.com/USERNAME/NAMA-REPO.git
cd NAMA-REPO
```

### 2. Buat virtual environment (opsional tapi disarankan)

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependency

```bash
pip install -r requirements.txt
```

### 4. Jalankan aplikasi

```bash
streamlit run form_pendaftaran.py
```

Aplikasi akan terbuka otomatis di browser pada `http://localhost:8501`.

---

## ⚙️ Konfigurasi

### Menghubungkan ke Google Sheets (sheet.best)

1. Buat Google Sheet baru dengan kolom-kolom berikut di baris pertama (header):

   | tanggal_daftar | nama_lengkap | nama_panggilan | orang_tua | no_wa | alamat | sekolah_kelas | pekerjaan_ortu | program_dipilih | jadwal_a |
   |---|---|---|---|---|---|---|---|---|---|

2. Daftar/masuk ke [sheet.best](https://sheet.best) dan hubungkan sheet tersebut untuk mendapatkan **Connection URL**.
3. Buka `form_pendaftaran.py`, ganti nilai `SHEET_URL` di bagian atas dengan URL milik Anda:

   ```python
   SHEET_URL = "https://api.sheetbest.com/sheets/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
   ```

4. **Penting:** di Google Sheets, klik kanan kolom `tanggal_daftar` → **Format cells** → pilih **Plain text**, agar tanggal tidak otomatis dikonversi/berantakan oleh Google Sheets.

### Menambahkan Logo

Simpan file gambar dengan nama `logo.png` (atau ubah `LOGO_PATH` di kode) di folder yang sama dengan `form_pendaftaran.py`. Logo akan tampil di kotak kecil pada header.

### Menambahkan Poster / Banner

Simpan file gambar dengan nama `poster.png` (atau ubah `POSTER_PATH` di kode) di folder yang sama. Poster ini akan **menggantikan** banner biru default. Disarankan rasio gambar sekitar 3:1 atau 4:1 (misal 1200×400 px).

---

## ☁️ Deploy ke Streamlit Community Cloud (gratis)

1. Push repo ini ke GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io), login dengan akun GitHub.
3. Klik **New app**, pilih repo ini, pilih branch, dan set **Main file path** ke `form_pendaftaran.py`.
4. Klik **Deploy**. Aplikasi akan mendapatkan link publik yang bisa dibagikan lewat WhatsApp.

---

## 🧩 Dependency

Lihat [`requirements.txt`](./requirements.txt):

```
streamlit>=1.28
requests>=2.31
```

---

## 📝 Catatan

- Endpoint update data (`PATCH`) menggunakan pola filter query parameter standar sheet.best (`?nama_lengkap=...&no_wa=...`). Jika akun sheet.best Anda menggunakan format API yang berbeda, sesuaikan fungsi `update_data_lama()` dan `cek_data_existing()` di `form_pendaftaran.py`.
- Aplikasi ini tidak menyimpan data secara lokal — semua data pendaftar langsung dikirim ke Google Sheets melalui sheet.best.

---

## ❤️ Kontribusi

Dibuat untuk warga kampung. Pull request dan masukan untuk perbaikan sangat diterima.
