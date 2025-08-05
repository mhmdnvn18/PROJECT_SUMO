# Mini-Project: Traffic Signal Optimization using Q-Learning and SUMO

## 1. Create a Simple Road Network

- Jaringan jalan dibuat menggunakan OpenStreetMap (OSM) atau netedit (SUMO’s network editor).
- Jaringan mencakup minimal satu persimpangan empat-arah (four-way intersection) dan minimal satu traffic light.
- Beberapa kendaraan IoT-enabled (connected vehicles) dimasukkan ke dalam simulasi.
- Contoh peta: area urban di Taiwan yang memenuhi syarat di atas.

## 2. Use OpenStreetMap (OSM) or netedit

- File `map.osm` tersedia sebagai basis jaringan.
- Jaringan dikonversi ke format SUMO (`map.net.xml`) menggunakan netconvert/netedit.
- Traffic light didefinisikan di persimpangan utama.

## 3. Define Traffic Flow

- File rute kendaraan (`map.rou.xml`) dibuat untuk mendefinisikan tipe kendaraan, waktu keberangkatan, dan rute.
- Minimal 10 kendaraan dengan rute berbeda.
- Tipe kendaraan bervariasi: IoT-enabled, emergency, bus, motor, car, dsb.

## 4. Simulate IoT-enabled Traffic Management

- Implementasi sistem traffic light adaptif berbasis IoT menggunakan TraCI (Traffic Control Interface).
- Script `1.adaptive_traffic_light.py` mengatur durasi lampu lalu lintas secara dinamis berdasarkan kepadatan kendaraan real-time.
- Kendaraan IoT berperan sebagai sensor untuk mendeteksi kemacetan dan membantu sistem menyesuaikan sinyal lampu.

## 5. Visualize and Analyze Results

- Simulasi dijalankan di SUMO-GUI untuk mengamati perilaku lalu lintas.
- Hasil simulasi (misal `tripinfo_adaptive.xml`) dianalisis menggunakan script `analyze_tripinfo.py` untuk melihat waktu tempuh dan waktu tunggu kendaraan.
- Visualisasi hasil (grafik) disimpan di `images/hasil_simulasi.png`.
- Diskusi dampak: sistem adaptif berbasis IoT terbukti mengurangi kemacetan dan waktu tunggu dibanding sistem statis.

---

## Traffic Signal Optimization using Q-Learning and SUMO

### Latar Belakang

Kemacetan lalu lintas adalah tantangan utama di kota pintar. Sinyal lalu lintas konvensional dengan waktu tetap kurang efisien pada kondisi lalu lintas dinamis. Mini-project ini mengimplementasikan agen Q-Learning untuk mengoptimalkan durasi lampu lalu lintas secara real-time.

### Lingkungan Simulasi

- Persimpangan dengan empat lajur masuk (Utara, Selatan, Timur, Barat).
- Arus lalu lintas bervariasi (peak/off-peak).
- Kedatangan kendaraan mengikuti distribusi probabilitas.

### State Representation

- Jumlah kendaraan di tiap lajur.
- Rata-rata waktu tunggu kendaraan.
- Fase lampu lalu lintas saat ini.
- (Bisa ditambah fitur lain sesuai skenario.)

### Action Space

- Mengubah fase lampu lalu lintas (misal: memperpanjang hijau, ganti merah, dst).

### Reward Function

- Penalti untuk waktu tunggu kendaraan.
- Penalti tambahan untuk antrian panjang.
- Reward positif untuk pengurangan kemacetan.

### Implementasi

- Script `3.q_learning_traffic_light.py` mengintegrasikan Q-Learning dengan SUMO melalui TraCI.
- Agen Q-Learning memutuskan perubahan fase lampu berdasarkan state dan reward.
- Dataset hasil simulasi (misal `traffic_signal_data.csv`) berisi: timestep, jumlah kendaraan per lajur, rata-rata waktu tunggu, fase lampu.

### Evaluasi

- Bandingkan performa Q-Learning dengan strategi fixed-timing (tradisional).
- Analisis hasil menggunakan `analyze_tripinfo.py` dan visualisasi grafik.

---

## Cara Menjalankan Simulasi

1. **Simulasi traffic light adaptif berbasis IoT:**
   ```
   python 1.adaptive_traffic_light.py
   ```
   Output: `tripinfo_adaptive.xml`

2. **Simulasi traffic light Q-Learning:**
   ```
   python 3.q_learning_traffic_light.py
   ```
   Output: `tripinfo_qlearning.xml`, `traffic_signal_data.csv`

3. **Analisis hasil simulasi:**
   ```
   python analyze_tripinfo.py
   ```
   Pilih file tripinfo yang ingin dianalisis.

---

## Deliverables

- Implementasi Python Q-Learning dengan SUMO.
- Laporan penjelasan pendekatan, hasil, dan perbandingan dengan fixed-timing.
- Grafik/plot pengurangan kemacetan dari waktu ke waktu.

---

## Struktur File

- `map.osm` : Peta OSM asli.
- `map.sumocfg` : Konfigurasi simulasi SUMO.
- `map.rou.xml` : Definisi rute dan kendaraan.
- `1.adaptive_traffic_light.py` : Script traffic light adaptif berbasis IoT.
- `3.q_learning_traffic_light.py` : Script traffic light berbasis Q-Learning.
- `analyze_tripinfo.py` : Analisis hasil simulasi.
- `traffic_signal_data.csv` : Dataset hasil simulasi Q-Learning.
- `images/hasil_simulasi.png` : Visualisasi hasil analisis.

---

## Catatan

- Pastikan SUMO dan TraCI sudah terinstall.
- Untuk menambah/mengedit jaringan, gunakan netedit atau OSM.
- Semua script dapat dijalankan langsung dari terminal/command prompt.

# Evaluasi Mini-Project SUMO: IoT-based Adaptive Traffic Light

## Checklist Kriteria

1. **Create a Simple Road Network**
   - Jaringan jalan sudah ada (`map.net.xml`, `test.net.xml`, `map.osm`).
   - Empat simpang (four-way intersection): Sudah ada pada peta OSM Taiwan.
   - Minimal satu traffic light: Sudah ada, dapat dicek di netedit/SUMO-GUI.

2. **Use OpenStreetMap (OSM) or netedit**
   - Menggunakan OSM: File `map.osm` tersedia.
   - Jaringan hasil OSM/netedit: Sudah dikonversi ke SUMO.

3. **Define Traffic Flow**
   - File route (.rou.xml) tersedia: `map.rou.xml`
   - Minimal 10 kendaraan, rute berbeda: Sudah ada minimal 10 kendaraan dengan rute berbeda di `map.rou.xml`.
   - Tipe kendaraan IoT-enabled: Sudah ditambahkan `<vType id="iot" ...>` dan beberapa kendaraan dengan `type="iot"` di file route.
   - Variasi kendaraan: Sudah ada kendaraan IoT, emergency, bus, motor, dan car.

4. **Simulate IoT-enabled Traffic Management**
   - Implementasi adaptive traffic light: Ada di `1.adaptive_traffic_light.py` (menggunakan TraCI).
   - Deteksi kendaraan IoT: Sudah ada logika deteksi kendaraan IoT di script.
   - Penyesuaian traffic light berbasis density: Sudah diimplementasikan.

5. **Visualize and Analyze Results**
   - Simulasi dapat dijalankan di SUMO-GUI: Sudah.
   - Analisis tripinfo.xml: Ada script `analyze_tripinfo.py` untuk analisis.
   - Diskusi dampak IoT-based adaptive traffic control: Sudah ditambahkan di bawah.

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

- **Use Case:** Pengelolaan lampu lalu lintas adaptif berbasis IoT di persimpangan padat kota Taiwan.
- **Scenario:** Kendaraan IoT-enabled mengirim data ke pusat kontrol, lampu lalu lintas menyesuaikan waktu hijau/mati secara dinamis untuk mengurangi kemacetan.

#### Issues
- Kemacetan di persimpangan akibat pengaturan lampu lalu lintas statis.
- Kurangnya responsif terhadap volume kendaraan yang berubah-ubah.

#### Problem Statement
Bagaimana mengurangi waktu tunggu dan kemacetan di persimpangan dengan memanfaatkan data real-time dari kendaraan IoT?

#### Proposed Solution
Implementasi sistem lampu lalu lintas adaptif berbasis TraCI, yang menyesuaikan durasi lampu berdasarkan deteksi kendaraan IoT dan density kendaraan secara real-time.

---

## Smart City Use Case: Adaptive Traffic Signal Control in Smart Intersections using IoT and Q-Learning

### Scenario

Persimpangan sibuk di pusat kota Taipei sering mengalami kemacetan, terutama pada jam sibuk. Banyak kendaraan sudah dilengkapi perangkat IoT yang dapat mengirimkan data posisi dan status secara real-time ke sistem lalu lintas kota.

### Problem Statement

Lampu lalu lintas konvensional menggunakan siklus tetap atau hanya sedikit adaptif, sehingga tidak mampu merespons perubahan lalu lintas secara real-time. Akibatnya, terjadi penumpukan kendaraan dan waktu tunggu yang lama, terutama jika ada lonjakan kendaraan dari satu arah.

### Proposed Solution

Menggunakan sistem pengendalian lampu lalu lintas berbasis Q-Learning yang memanfaatkan data kendaraan IoT-enabled. Sistem ini:
- Mendeteksi jumlah kendaraan IoT di setiap lajur secara real-time.
- Mengadaptasi durasi lampu hijau/merah berdasarkan kepadatan dan distribusi kendaraan.
- Menggunakan algoritma Q-Learning untuk belajar pola lalu lintas dan mengoptimalkan waktu siklus lampu.
- Hasil simulasi menunjukkan penurunan waktu tempuh dan waktu tunggu rata-rata dibandingkan sistem konvensional.

---

## Implementasi

- Jaringan jalan dan lampu lalu lintas dibuat menggunakan OSM dan netedit.
- Kendaraan IoT-enabled didefinisikan dalam `map.rou.xml`.
- Dua skenario simulasi: adaptif berbasis aturan (`1.adaptive_traffic_light.py`) dan Q-Learning (`3.q_learning_traffic_light.py`).
- Analisis hasil simulasi menggunakan `analyze_tripinfo.py` dan visualisasi statistik.

---

## Struktur File

- `map.osm`, `map.net.xml`, `test.net.xml`: Jaringan jalan.
- `map.rou.xml`: Definisi rute dan kendaraan (termasuk IoT-enabled).
- `1.adaptive_traffic_light.py`: Traffic light adaptif berbasis density & IoT.
- `3.q_learning_traffic_light.py`: Traffic light adaptif berbasis Q-Learning.
- `analyze_tripinfo.py`: Analisis hasil simulasi dan visualisasi.
- `tripinfo_adaptive.xml`, `tripinfo_qlearning.xml`: Output hasil simulasi.
- `traffic_signal_data.csv`: Dataset hasil simulasi Q-Learning.
- `images/hasil_simulasi.png`: Visualisasi hasil analisis.

---

## Cara Menjalankan

1. **Simulasi traffic light adaptif berbasis IoT:**
   ```
   python 1.adaptive_traffic_light.py
   ```
2. **Simulasi traffic light Q-Learning:**
   ```
   python 3.q_learning_traffic_light.py
   ```
3. **Analisis hasil simulasi:**
   ```
   python analyze_tripinfo.py
   ```

---

## Catatan

- Pastikan SUMO dan TraCI sudah terinstall.
- Untuk menambah/mengedit jaringan, gunakan netedit atau OSM.
- Semua script dapat dijalankan langsung dari terminal/command prompt.

