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

Sistem simulasi dan dashboard cerdas untuk manajemen parkir berbasis SUMO dan Streamlit.

## Fitur Utama

- **Simulasi SUMO**: Kendaraan penumpang, komersial, dan bus dengan rute dan area parkir realistis.
- **Dashboard Real-Time**: Visualisasi status parkir, progress simulasi, dan kontrol kecepatan.
- **Peta Interaktif**: Lokasi area parkir ditampilkan di peta (Folium), koordinat diambil dari data SUMO.
- **Reservasi Parkir**: Pengendara dapat melakukan booking slot parkir, terintegrasi dengan simulasi.
- **Prediksi AI**: Prediksi ketersediaan parkir berbasis data historis.
- **Analitik & Tren**: Grafik tren okupansi parkir dan dampak lingkungan untuk pemerintah/operator.
- **Penyimpanan Data Historis**: Log status parkir dan reservasi ke database SQLite.
- **Multi-Role Dashboard**: Tampilan berbeda untuk Pengendara, Operator Parkir, dan Pemerintah.
- **Notifikasi Real-Time**: Pemberitahuan perubahan status parkir.
- **Mobile Friendly**: Layout responsif.

## Arsitektur

- **SUMO**: Simulasi lalu lintas, area parkir, dan bus stop.
- **Python/Streamlit**: Dashboard interaktif, integrasi TraCI, visualisasi, backend reservasi, dan prediksi.
- **Folium**: Peta lokasi parkir.
- **Plotly**: Grafik analitik.
- **SQLite**: Penyimpanan data historis.

## Instalasi

1. **Kebutuhan Sistem**
   - Python 3.8+
   - SUMO (Simulator)
   - pip

2. **Instalasi Python Package**
   ```
   pip install streamlit traci folium streamlit-folium plotly pandas
   ```

3. **Jalankan SUMO dan Dashboard**
   - Pastikan file jaringan, rute, dan konfigurasi SUMO sudah lengkap.
   - **Penting:** Lengkapi file `parkingArea.add.xml` dan `busStops.add.xml` sesuai jaringan Anda.
   - Jalankan dashboard:
     ```
     streamlit run dashboard.py
     ```

## Cara Pakai

1. Pilih role pengguna: Pengendara, Operator Parkir, atau Pemerintah.
2. Mulai simulasi, atur kecepatan, dan pantau status parkir secara real-time.
3. Pengendara dapat melihat peta, prediksi, dan melakukan reservasi slot parkir.
4. Operator dapat melihat data reservasi terbaru dan statistik okupansi.
5. Pemerintah dapat melihat grafik tren okupansi dan analitik dampak lingkungan.

## Struktur Folder

- `dashboard.py` : Dashboard Streamlit & backend
- `random.sumocfg`, `random.net.xml` : Konfigurasi & jaringan SUMO
- `rou/` : File rute kendaraan
- `parkingArea.add.xml`, `busStops.add.xml` : Definisi area parkir & bus stop (**wajib diisi**)
- `basic.vType.xml` : Tipe kendaraan
- `parking.db` : Database SQLite (otomatis dibuat)

## Kriteria Proyek

- [x] Simulasi kendaraan dan area parkir (pastikan file area parkir terisi)
- [x] Visualisasi status parkir real-time
- [x] Peta lokasi parkir (koordinat dari SUMO)
- [x] Sistem reservasi parkir terintegrasi simulasi
- [x] Prediksi ketersediaan slot berbasis data historis
- [x] Analitik okupansi dan dampak lingkungan
- [x] Penyimpanan data historis
- [x] Multi-role dashboard
- [x] Notifikasi real-time

## Catatan

- **Isi file `parkingArea.add.xml` dan `busStops.add.xml` sesuai jaringan Anda agar simulasi berjalan sempurna.**
- Model prediksi dapat dikembangkan lebih lanjut.
- Pastikan semua file SUMO (.net.xml, .sumocfg, .rou.xml, dll) sudah lengkap dan konsisten.

## Lisensi

MIT License
