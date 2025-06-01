# Smart Parking Finder System (SUMO)

Sistem simulasi pencarian parkir pintar menggunakan SUMO (Simulation of Urban MObility) dan Python (TraCI) untuk mensimulasikan perilaku kendaraan dalam mencari tempat parkir di lingkungan perkotaan.

## Struktur Folder
```
Smart-Parking-Finder-System/
├── data/                  # Berisi file data simulasi
│   ├── map.osm            # Peta OpenStreetMap
│   ├── map.net.xml        # Jaringan SUMO hasil konversi
│   ├── map.sumocfg        # Konfigurasi utama simulasi
│   ├── map.rou.xml        # Rute dan kendaraan
│   ├── parking.add.xml    # Definisi parking area
│   ├── tripinfo.xml       # Output statistik perjalanan (dihasilkan saat simulasi)
│   └── map.poly.xml       # Poligon bangunan/taman
├── scripts/               # Skrip Python
│   ├── run_simulation.py  # Skrip utama menjalankan simulasi
│   ├── analyze_tripinfo.py # Analisis hasil simulasi
│   └── parking_dashboard.py # Dashboard real-time (Flask)
├── images/                # Folder untuk menyimpan visualisasi hasil analisis
├── docs/                  # Dokumentasi tambahan
│   └── TODOLIST.MD        # Rencana pengembangan proyek
├── requirements.txt       # Dependensi Python
└── README.MD              # Dokumentasi utama
```

## Prasyarat

- **SUMO:** Instal SUMO versi terbaru dari situs resmi
- **Python 3.7+:** Pastikan Python versi terbaru terinstal

### Environment Variables

```bash
export SUMO_HOME="/path/ke/direktori/sumo"
export PATH="$SUMO_HOME/bin:$PATH"
```

## Instalasi Dependensi

```bash
pip install -r requirements.txt
```

Dependensi utama:
- traci (SUMO Python interface)
- pandas
- matplotlib
- flask (untuk dashboard)

## Menjalankan Simulasi

### 1. Konversi Peta OSM ke SUMO Net
```bash
netconvert --osm data/map.osm -o data/map.net.xml --roundabouts.guess --tls.guess-signals true
```

### 2. Jalankan Simulasi
```bash
python scripts/run_simulation.py
```

### 3. Analisis Hasil
```bash
python scripts/analyze_tripinfo.py
```

### 4. Dashboard Real-time (Opsional)
```bash
python scripts/parking_dashboard.py
```
Akses http://localhost:5000

## Generate Random Trips

Untuk menghasilkan file rute acak (`map.rou.xml`) dengan berbagai tipe kendaraan, jalankan perintah berikut dari root project:

```bash
python data/randomTrips.py -n data/map.net.xml -r data/map.rou.xml \
  --passenger 70 --truck 20 --bus 10 --emergency 5 \
  -b 0 -e 3600
```

Pastikan file `randomTrips.py` ada di folder `data`.

## Troubleshooting

| Masalah                        | Solusi                                                                 |
|---------------------------------|------------------------------------------------------------------------|
| Parking area tidak muncul       | Pastikan file parking.add.xml tercantum di map.sumocfg                 |
| Error lane tidak ditemukan      | Verifikasi ID lane di net.xml menggunakan netedit                      |
| GUI terlalu cepat               | Tambahkan `time.sleep(0.1)` di loop TraCI                              |

## Catatan Penting
- Parking area harus didefinisikan di file tambahan (.add.xml)
- Kendaraan akan mencari slot parkir otomatis jika rute mengandung `<stop>`
- Gunakan sumo-gui untuk simulasi interaktif