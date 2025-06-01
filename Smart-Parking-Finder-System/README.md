# Smart Parking Finder System

## Judul Proyek
Smart Parking Finder System - Memanfaatkan AIoT untuk Deteksi dan Pencarian Tempat Parkir secara Real-Time

## Nama Kasus Penggunaan & Skenario

- **Nama Kasus Penggunaan:** Smart Parking Finder System
- **Skenario:** Di pusat kota yang padat, pengendara sering menghabiskan waktu hanya untuk mencari slot parkir yang kosong. Sistem ini akan membantu pengendara menemukan tempat parkir terdekat dan kosong secara real-time, menggunakan data dari sensor dan AI.

## Permasalahan yang Diangkat

- Waktu terbuang untuk mencari parkir (rata-rata 15-20 menit di kota padat)
- Menyebabkan kemacetan tambahan
- Meningkatkan emisi karbon dan konsumsi bahan bakar
- Tidak ada sistem informasi parkir yang real-time

## Pengguna Proyek di Masa Depan

- **Pengendara Kendaraan Pribadi:** Untuk mencari tempat parkir dengan cepat
- **Pengelola Area Parkir:** Untuk memantau dan mengoptimalkan penggunaan slot parkir
- **Pemerintah Kota:** Untuk mengurangi kemacetan dan polusi, dan mendukung Smart City

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
- [x] `dashboard.py` (masih kosong, perlu implementasi)
- [x] `random.sumocfg`, `random.net.xml`, `parkingArea.add.xml`, `parkingAreaRerouters.add.xml`, `busStops.add.xml`, `basic.vType.xml` (beberapa file masih kosong)
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
