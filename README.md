# 📚 Aplikasi Pendaftaran Kursus Online/Offline

Aplikasi pendaftaran kursus berbasis Streamlit dengan integrasi database Supabase. Mendukung pendaftaran online dan offline dengan form adaptif yang menyesuaikan jenis pendaftar (Anak/Diri Sendiri).

## ✨ Fitur

- 🌐 **Metode Pembelajaran**: Pilihan Online (Zoom/Google Meet) atau Offline (Tatap Muka)
- 👤 **Form Adaptif**: 
  - Untuk **Anak**: Menampilkan data orang tua dan sekolah/kelas
  - Untuk **Diri Sendiri**: Menampilkan status/pekerjaan tanpa data orang tua
  - Khusus **UMUM**: Data orang tua disembunyikan (untuk pendaftar dewasa)
- 📋 **Multi-Program**: Bisa memilih lebih dari 1 program kursus
- 📅 **Jadwal Fleksibel**: Pilihan jadwal untuk Program MATH DROP-IN
- 🔍 **Cek Duplikat**: Deteksi otomatis jika pendaftar sudah terdaftar
- 💾 **Database Supabase**: Penyimpanan data yang aman dan scalable
- 📊 **Progress Indicator**: Menampilkan kelengkapan formulir secara real-time
- 🎨 **Responsive Design**: Tampilan yang menarik di desktop dan mobile

## 🛠️ Teknologi yang Digunakan

- [Streamlit](https://streamlit.io/) - Framework Python untuk web app
- [Supabase](https://supabase.com/) - Backend as a Service (PostgreSQL)
- [Python 3.8+](https://python.org/) - Bahasa pemrograman
- HTML/CSS - Styling kustom

## 📋 Struktur Database Supabase

### Tabel: `pendaftaran`

| Kolom | Tipe | Keterangan |
|-------|------|------------|
| `id` | BIGSERIAL | Primary Key |
| `tanggal_daftar` | TEXT | Tanggal pendaftaran (format Indonesia) |
| `metode` | TEXT | Online/Offline |
| `nama_lengkap` | TEXT | Nama lengkap pendaftar |
| `nama_panggilan` | TEXT | Nama panggilan (opsional) |
| `orang_tua` | TEXT | Nama orang tua/wali (atau '-' untuk diri sendiri) |
| `no_wa` | TEXT | Nomor WhatsApp |
| `alamat` | TEXT | Alamat pendaftar |
| `sekolah_kelas` | TEXT | Sekolah/Kelas atau Status/Pekerjaan |
| `pekerjaan_ortu` | TEXT | Pekerjaan orang tua atau pekerjaan sendiri |
| `program_dipilih` | TEXT | Program kursus yang dipilih |
| `jadwal_a` | TEXT | Jadwal MATH DROP-IN yang dipilih |
| `tipe_pendaftar` | TEXT | "Anak" atau "Diri Sendiri" |
| `status_umum` | TEXT | "Ya" atau "Tidak" |
| `created_at` | TIMESTAMP | Waktu pembuatan data |

### SQL untuk Membuat Tabel

```sql
CREATE TABLE pendaftaran (
    id BIGSERIAL PRIMARY KEY,
    tanggal_daftar TEXT,
    metode TEXT,
    nama_lengkap TEXT,
    nama_panggilan TEXT,
    orang_tua TEXT,
    no_wa TEXT,
    alamat TEXT,
    sekolah_kelas TEXT,
    pekerjaan_ortu TEXT,
    program_dipilih TEXT,
    jadwal_a TEXT,
    tipe_pendaftar TEXT,
    status_umum TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Buat index untuk pencarian cepat
CREATE INDEX idx_no_wa ON pendaftaran(no_wa);
CREATE INDEX idx_nama_lengkap ON pendaftaran(nama_lengkap);