# Smart Parking Finder System
Memanfaatkan AIoT untuk Deteksi dan Pencarian Tempat Parkir secara Real-Time

## Cara Menjalankan

Jalankan perintah berikut agar dashboard otomatis menjalankan simulasi SUMO dan menampilkan status parkir:
```bash
streamlit run dashboard.py
```

> **Catatan:** Tidak perlu menjalankan SUMO secara manual saat menjalankan dashboard.

## Checklist File
- [x] README.md (file ini)
- [x] dashboard.py (masih kosong, perlu implementasi)
- [x] random.sumocfg, random.net.xml, parkingArea.add.xml, parkingAreaRerouters.add.xml, busStops.add.xml, basic.vType.xml (beberapa file masih kosong)
- [x] rou/commercial.rou.xml, rou/passenger.rou.xml, rou/ptw.rou.xml, rou/buses.flows.xml
- [x] .gitignore

**Catatan:**  
Beberapa file konfigurasi SUMO dan dashboard.py masih kosong dan perlu diisi sesuai kebutuhan simulasi dan dashboard.

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
- `parking_monitor.py`  
  Skrip Python untuk monitoring status parkir via TraCI.
- `dashboard.py`  
  Dashboard Streamlit untuk visualisasi status parkir real-time.

---

## Cara Penggunaan

1. **Instalasi SUMO**  
   Unduh dan instal SUMO dari [https://www.eclipse.org/sumo/](https://www.eclipse.org/sumo/).

2. **Instalasi Dependensi Python**  
   ```
   pip install streamlit sumolib traci
   ```

3. **Menjalankan Simulasi Monitoring Parkir**  
   ```
   python parking_monitor.py
   ```

4. **Menjalankan Dashboard Real-Time**  
   ```
   streamlit run dashboard.py
   ```

5. **Menjalankan Simulasi SUMO Manual**  
   ```
   sumo-gui -c random.sumocfg
   ```
   atau untuk mode command-line:
   ```
   sumo -c random.sumocfg
   ```

---
