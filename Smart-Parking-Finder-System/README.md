# Smart Parking Finder System  
Oleh: STEVEN ADI

## Latar Belakang

Di banyak wilayah perkotaan, peningkatan pesat jumlah kendaraan telah menyebabkan masalah ketersediaan tempat parkir yang semakin terbatas. Pengemudi sering menghabiskan banyak waktu berputar-putar untuk mencari tempat parkir kosong, yang tidak hanya menyebabkan frustrasi tetapi juga berkontribusi terhadap kemacetan lalu lintas, pemborosan bahan bakar, dan emisi karbon yang lebih tinggi. Sistem yang tidak efisien ini menyoroti perlunya solusi yang lebih cerdas dan real-time yang dapat membantu pengemudi menemukan tempat parkir yang tersedia dengan cepat dan efisien.

## Permasalahan yang Diangkat

- **Ketersediaan Tempat Parkir Terbatas:**  
  Kepadatan kendaraan yang tinggi dan infrastruktur parkir yang terbatas menyebabkan kekurangan tempat parkir.
- **Waktu dan Bahan Bakar Terbuang:**  
  Pengemudi menghabiskan waktu berlebihan untuk mencari parkir, yang menyebabkan konsumsi bahan bakar dan hilangnya produktivitas.  
  Rata-rata pencarian parkir bisa memakan waktu 15-20 menit di kota padat.  
  Peningkatan konsumsi bahan bakar dan emisi karbon.
- **Kemacetan Lalu Lintas:**  
  Kendaraan yang berputar-putar mencari parkir berkontribusi signifikan terhadap kemacetan lalu lintas di dalam kota.
- **Kurangnya Informasi Real-Time:**  
  Pengemudi tidak mengetahui terlebih dahulu di mana parkir tersedia, membuat prosesnya tidak dapat diprediksi.  
  Tidak ada sistem informasi parkir yang terintegrasi dan real-time.

## Pengguna Proyek di Masa Depan

- **Pengendara (Drivers):**  
  Pengguna utama Sistem Pencari Parkir. Mereka akan menggunakan sistem untuk menemukan tempat parkir yang tersedia secara real-time dengan cepat, mengurangi waktu yang dihabiskan untuk mencari dan membantu mereka mencapai tujuan lebih efisien. Ini meningkatkan pengalaman berkendara secara keseluruhan dan menghemat bahan bakar.  
  *Kebutuhan:* Mencari tempat parkir dengan cepat.

- **Manajemen Area Parkir (Parking Area Management):**  
  Operator dan manajer tempat parkir dapat menggunakan sistem untuk memantau okupansi, mengelola ketersediaan ruang, dan mengoptimalkan operasi parkir. Sistem ini membantu mereka mengumpulkan data, meningkatkan layanan pelanggan, dan meningkatkan pendapatan dengan membuat fasilitas mereka lebih mudah diakses dan efisien.  
  *Kebutuhan:* Memantau dan mengoptimalkan penggunaan slot parkir.

- **Pemerintah (Government):**  
  Pemerintah kota dapat mengadopsi sistem untuk mengurangi kemacetan lalu lintas, menurunkan emisi, dan mendukung inisiatif kota pintar (smart city). Dengan menganalisis data parkir, mereka dapat membuat keputusan yang tepat tentang perencanaan kota, meningkatkan kebijakan transportasi, dan menyempurnakan infrastruktur publik.  
  *Kebutuhan:* Mengurangi kemacetan dan polusi, serta mendukung inisiatif Smart City.

## Cara Kerja Sistem

**Deskripsi Umum:**  
Sistem Pencari Parkir menggunakan sensor, GPS, dan aplikasi atau situs web untuk menunjukkan ketersediaan parkir secara real-time. Sistem ini mendeteksi tempat kosong, memperbarui data di server pusat, dan menampilkannya di peta untuk pengguna. Fitur mungkin termasuk navigasi, reservasi, dan opsi pembayaran.

**Komponen:**
- **Sensor:**  
  Mendeteksi apakah tempat parkir terisi atau kosong.  
  Jenis:  
  - Sensor inframerah  
  - Sensor ultrasonik  
  - Sensor magnetik  
  - Kamera dengan AI  
  Lokasi: Dipasang di setiap ruang parkir atau di titik masuk/keluar.
- **Server (Sistem Pusat):**  
  Mengumpulkan data dari sensor, memproses informasi ketersediaan, menyimpan data historis, dan menyediakan antarmuka untuk aplikasi pengguna agar dapat mengakses status parkir secara real-time.
- **Aplikasi Seluler (atau Aplikasi Web):**  
  Antarmuka bagi pengguna untuk mengakses informasi dan layanan parkir.  
  Fitur:  
  - Peta Langsung  
  - Pencarian dan Filter  
  - Navigasi  
  - Reservasi dan Pembayaran  
  - Notifikasi
- **Pengguna (Users):**  
  Pengguna akhir yang mencari tempat parkir.  
  Tindakan:  
  - Mengunduh dan membuka aplikasi  
  - Mencari parkir terdekat  
  - Melihat ketersediaan secara real-time  
  - Memesan atau membayar tempat jika diperlukan  
  - Menavigasi ke area parkir yang dipilih  
  Manfaat:  
  - Menghemat waktu dan bahan bakar  
  - Mengurangi stres dan kemacetan lalu lintas  
  - Menawarkan opsi pembayaran dan reservasi yang nyaman

---

# Smart Parking Finder System

## Judul Proyek
Smart Parking Finder System - Memanfaatkan AIoT untuk Deteksi dan Pencarian Tempat Parkir secara Real-Time

## Nama Kasus Penggunaan & Skenario

- **Nama Kasus Penggunaan:** Smart Parking Finder System
- **Skenario:** Di pusat kota yang padat, pengendara sering menghabiskan waktu hanya untuk mencari slot parkir yang kosong. Sistem ini akan membantu pengendara menemukan tempat parkir terdekat dan kosong secara real-time, menggunakan data dari sensor dan AI.

## Pekerjaan yang Sedang Berlangsung

- Pengumpulan data lokasi parkir dalam simulasi SUMO
- Implementasi sensor parkir dalam bentuk logika simulasi (misalnya: slot penuh/kosong)
- Visualisasi tempat parkir real-time di dashboard sederhana
- Rencana penggunaan AI sederhana untuk prediksi slot kosong di waktu sibuk

## Langkah Selanjutnya

- Integrasi dashboard dengan simulasi
- Evaluasi performa sistem pada skenario jam sibuk

---
## Daftar Isi

- [Cara Menjalankan](#cara-menjalankan)
- [Checklist File](#checklist-file)
- [Simulasi & Integrasi](#simulasi--integrasi)
- [Struktur Direktori](#struktur-direktori)
- [Cara Penggunaan](#cara-penggunaan)

---

## Cara Menjalankan

Jalankan perintah berikut agar dashboard otomatis menjalankan simulasi SUMO dan menampilkan status parkir:
```bash
streamlit run dashboard.py
```
> **Catatan:** Tidak perlu menjalankan SUMO secara manual saat menjalankan dashboard.

---

## Checklist File

- [x] `README.md` (file ini)
- [x] `dashboard.py` 
- [x] `random.sumocfg`, `random.net.xml`, `parkingArea.add.xml`, `parkingAreaRerouters.add.xml`, `busStops.add.xml`, `basic.vType.xml` 
- [x] `rou/commercial.rou.xml`, `rou/passenger.rou.xml`, `rou/ptw.rou.xml`, `rou/buses.flows.xml`
- [x] `.gitignore`

> **Catatan:**  
> Beberapa file konfigurasi SUMO dan `dashboard.py` masih kosong dan perlu diisi sesuai kebutuhan simulasi dan dashboard.

---

## Simulasi & Integrasi

### 1. Pengumpulan Data Lokasi Parkir di SUMO

- Pastikan file `parkingArea.add.xml` sudah terdefinisi dan terhubung di `random.sumocfg`.
- Jalankan simulasi SUMO dan gunakan TraCI untuk mengambil data status parkir secara real-time.

### 2. Implementasi Sensor Parkir (Logika Penuh/Kosong)

- Jalankan skrip berikut untuk memonitor status parkir:
  ```bash
  python parking_monitor.py
  ```
- Skrip akan menampilkan status penuh/kosong setiap area parkir secara real-time di terminal.

### 3. Visualisasi Dashboard Real-Time

- Jalankan dashboard Streamlit:
  ```bash
  streamlit run dashboard.py
  ```
- Dashboard akan menampilkan status area parkir secara real-time selama simulasi berjalan.

### 4. Rencana AI Prediksi Slot Kosong

- Kumpulkan data historis status parkir dari simulasi.
- Gunakan model machine learning sederhana (misal: regresi/logistic regression) untuk prediksi slot kosong pada jam sibuk.
- Integrasikan hasil prediksi ke dashboard.

---

## Struktur Direktori

- `random.sumocfg`  
  File konfigurasi utama SUMO.
- `random.net.xml`  
  Definisi jaringan jalan.
- `basic.vType.xml`  
  Tipe kendaraan yang digunakan dalam simulasi.
- `parkingArea.add.xml`  
  Definisi area parkir.
- `parkingAreaRerouters.add.xml`  
  Definisi rerouter untuk area parkir.
- `busStops.add.xml`  
  Definisi halte bus.
- `rou/`  
  Berisi file rute untuk berbagai tipe kendaraan:
  - `commercial.rou.xml`
  - `passenger.rou.xml`
  - `ptw.rou.xml`
  - `buses.flows.xml`
- `dashboard.py`  
  Dashboard Streamlit untuk visualisasi status parkir real-time.

---

## Cara Penggunaan

1. **Instalasi SUMO**  
   Unduh dan instal SUMO dari [https://www.eclipse.org/sumo/](https://www.eclipse.org/sumo/).

2. **Instalasi Dependensi Python**  
   ```bash
   pip install streamlit sumolib traci
   ```

3. **Menjalankan Dashboard Real-Time**  
   ```bash
   streamlit run dashboard.py
   ```

4. **Menjalankan Simulasi SUMO Manual**  
   ```bash
   sumo-gui -c random.sumocfg
   ```
   atau untuk mode command-line:
   ```bash
   sumo -c random.sumocfg
   ```

---
