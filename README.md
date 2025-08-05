# PROJECT_SUMO

Kumpulan mini-project dan studi kasus simulasi lalu lintas berbasis SUMO (Simulation of Urban MObility) dan integrasi Python (TraCI, Streamlit, AI/IoT).

## Daftar Sub-Proyek

- **Traffic Signal Optimization using Q-Learning and SUMO**  
  Optimasi lampu lalu lintas menggunakan Q-Learning dan simulasi SUMO.  
  [Lihat detail](./Traffic-Signal-Optimization-using-Q-Learning-and-SUMO/README.MD)

- **Smart Parking Finder System**  
  Sistem pencarian parkir cerdas berbasis simulasi SUMO dan dashboard real-time.  
  [Lihat detail](./Smart-Parking-Finder-System/README.md)

- **Basic Vehicle Color Animation in SUMO**  
  Contoh animasi perubahan warna kendaraan di SUMO menggunakan TraCI.  
  [Lihat detail](./.BACKUP/BASIC/README.MD)

## Fitur Umum

- Simulasi lalu lintas dengan jaringan jalan nyata (OSM/netedit)
- Kontrol lampu lalu lintas adaptif (rule-based & AI)
- Analisis hasil simulasi (waktu tempuh, waktu tunggu, visualisasi)
- Integrasi IoT/AI untuk smart city (parkir, traffic light)
- Dashboard real-time (Streamlit) & visualisasi peta (Folium)

## Cara Umum Menjalankan

1. **Instalasi SUMO dan Python**  
   Pastikan SUMO dan Python 3.x sudah terpasang di sistem Anda.

2. **Instalasi Dependensi Python**  
   Jalankan:
   ```
   pip install traci sumolib matplotlib streamlit folium plotly pandas
   ```

3. **Masuk ke folder sub-proyek**  
   Ikuti README masing-masing subfolder untuk instruksi detail.

## Struktur Folder

- `Traffic-Signal-Optimization-using-Q-Learning-and-SUMO/`  
  Studi kasus optimasi lampu lalu lintas (Q-Learning, adaptive, analisis).
- `Smart-Parking-Finder-System/`  
  Simulasi dan dashboard sistem parkir cerdas.
- `.BACKUP/BASIC/`  
  Contoh animasi warna kendaraan SUMO.
- File SUMO: `.sumocfg`, `.net.xml`, `.rou.xml`, dll.

## Lisensi

MIT License © 2025 Muhammad Novian

---

> Lihat README di masing-masing subfolder untuk detail penggunaan, dependensi, dan penjelasan tiap studi kasus.
