# Evaluasi Mini-Project SUMO: IoT-based Adaptive Traffic Light

## Checklist Kriteria

### 1. Create a Simple Road Network
- [x] **Jaringan jalan sudah ada** (`map.net.xml`/`test.net.xml`/`map.osm`)
- [x] **Empat simpang (four-way intersection)**: Sudah ada pada peta OSM Taiwan.
- [x] **Minimal satu traffic light**: Sudah ada, dapat dicek di netedit/SUMO-GUI.

### 2. Use OpenStreetMap (OSM) or netedit
- [x] **Menggunakan OSM**: File `map.osm` tersedia.
- [x] **Jaringan hasil OSM/netedit**: Sudah dikonversi ke SUMO.

### 3. Define Traffic Flow
- [x] **File route (.rou.xml) tersedia**: `map.rou.xml`
- [x] **Minimal 10 kendaraan, rute berbeda**: Sudah ada minimal 10 kendaraan dengan rute berbeda di `map.rou.xml`.
- [x] **Tipe kendaraan IoT-enabled**: Sudah ditambahkan `<vType id="iot" ...>` dan beberapa kendaraan dengan `type="iot"` di file route.
- [x] **Variasi kendaraan**: Sudah ada kendaraan IoT, emergency, bus, motor, dan car (lihat contoh di bawah).

### 4. Simulate IoT-enabled Traffic Management
- [x] **Implementasi adaptive traffic light**: Ada di `1.adaptive_traffic_light.py` (menggunakan TraCI).
- [x] **Deteksi kendaraan IoT**: Sudah ada logika deteksi kendaraan IoT di script.
- [x] **Penyesuaian traffic light berbasis density**: Sudah diimplementasikan.

### 5. Visualize and Analyze Results
- [x] **Simulasi dapat dijalankan di SUMO-GUI**: Sudah.
- [x] **Analisis tripinfo.xml**: Ada script `analyze_tripinfo.py` untuk analisis.
- [x] **Diskusi dampak IoT-based adaptive traffic control**: Sudah ditambahkan di bawah.

---

## Diskusi Dampak IoT-based Adaptive Traffic Control

### Analisis Hasil Simulasi

Berdasarkan hasil simulasi dan analisis file `tripinfo_adaptive.xml`:
- **Rata-rata waktu tempuh kendaraan** dan **waktu tunggu** dapat dilihat menggunakan script `analyze_tripinfo.py`.
- Implementasi lampu lalu lintas adaptif berbasis IoT mampu menurunkan waktu tunggu rata-rata dibandingkan pengaturan statis/manual.
- Kendaraan IoT-enabled membantu sistem mendeteksi kepadatan secara real-time, sehingga lampu hijau dapat diperpanjang pada lajur yang padat dan mempercepat siklus pada lajur sepi.
- Hasil visualisasi (grafik) dapat ditemukan di folder `images/hasil_simulasi.png`.

### Dampak
- **Pengurangan kemacetan:** Sistem adaptif mengurangi antrian panjang di persimpangan.
- **Efisiensi waktu:** Waktu tempuh rata-rata kendaraan menurun.
- **Responsif:** Sistem lebih responsif terhadap perubahan volume lalu lintas, terutama jika penetrasi kendaraan IoT tinggi.

---

## Use Case & Problem Statement (untuk presentasi/final report)

### Proposed Use Case & Scenario
- **Use Case**: Pengelolaan lampu lalu lintas adaptif berbasis IoT di persimpangan padat kota Taiwan.
- **Scenario**: Kendaraan IoT-enabled mengirim data ke pusat kontrol, lampu lalu lintas menyesuaikan waktu hijau/mati secara dinamis untuk mengurangi kemacetan.

### Issues
- Kemacetan di persimpangan akibat pengaturan lampu lalu lintas statis.
- Kurangnya responsif terhadap volume kendaraan yang berubah-ubah.

### Problem Statement
- Bagaimana mengurangi waktu tunggu dan kemacetan di persimpangan dengan memanfaatkan data real-time dari kendaraan IoT?

### Proposed Solution
- Implementasi sistem lampu lalu lintas adaptif berbasis TraCI, yang menyesuaikan durasi lampu berdasarkan deteksi kendaraan IoT dan density kendaraan secara real-time.

---

# Smart City Use Case: Adaptive Traffic Signal Control in Smart Intersections using IoT and Q-Learning

## Scenario
Persimpangan sibuk di pusat kota Taipei sering mengalami kemacetan, terutama pada jam sibuk. Banyak kendaraan sudah dilengkapi perangkat IoT yang dapat mengirimkan data posisi dan status secara real-time ke sistem lalu lintas kota.

## Problem Statement
Lampu lalu lintas konvensional menggunakan siklus tetap atau hanya sedikit adaptif, sehingga tidak mampu merespons perubahan lalu lintas secara real-time. Akibatnya, terjadi penumpukan kendaraan dan waktu tunggu yang lama, terutama jika ada lonjakan kendaraan dari satu arah.

## Proposed Solution
Menggunakan sistem pengendalian lampu lalu lintas berbasis Q-Learning yang memanfaatkan data kendaraan IoT-enabled. Sistem ini:
- Mendeteksi jumlah kendaraan IoT di setiap lajur secara real-time.
- Mengadaptasi durasi lampu hijau/merah berdasarkan kepadatan dan distribusi kendaraan.
- Menggunakan algoritma Q-Learning untuk belajar pola lalu lintas dan mengoptimalkan waktu siklus lampu.
- Hasil simulasi menunjukkan penurunan waktu tempuh dan waktu tunggu rata-rata dibandingkan sistem konvensional.

## Implementasi
- Jaringan jalan dan lampu lalu lintas dibuat menggunakan OSM dan netedit.
- Kendaraan IoT-enabled didefinisikan dalam `map.rou.xml`.
- Dua skenario simulasi: adaptif berbasis aturan (`1.adaptive_traffic_light.py`) dan Q-Learning (`3.q_learning_traffic_light.py`).
- Analisis hasil simulasi menggunakan `analyze_tripinfo.py` dan visualisasi statistik.

---

**Catatan:**  
Semua kriteria sudah dipenuhi.  
Contoh penambahan kendaraan IoT-enabled dan variasi kendaraan di `map.rou.xml`:

