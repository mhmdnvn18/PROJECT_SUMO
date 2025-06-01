# Smart Parking Finder System (SUMO)

Sistem ini merupakan simulasi pencarian parkir pintar menggunakan SUMO (Simulation of Urban MObility) dan Python (TraCI).

## Struktur Folder

- `data/` : berisi file jaringan, rute, dan parkir SUMO
- `main.py` : script utama untuk menjalankan simulasi dan monitoring parkir
- `requirements.txt` : dependensi Python

## Cara Menjalankan

1. **Install SUMO**  
   Pastikan SUMO sudah terinstall dan variabel lingkungan `SUMO_HOME` sudah di-set.

2. **Install dependensi Python**
   ```
   pip install -r requirements.txt
   ```

3. **Jalankan simulasi**
   ```
   python main.py
   ```

4. **Output**
   Status parkir akan tampil di terminal setiap step simulasi.

## Catatan

- File jaringan, rute, dan parkir dapat dimodifikasi pada folder `data/`.
- Untuk melihat simulasi secara visual, ubah `SUMO_BINARY` di `main.py` menjadi `sumo-gui`.

---

# Smart Parking Finder System

Sistem ini menggunakan SUMO (Simulation of Urban MObility) untuk mensimulasikan dan mencari tempat parkir secara cerdas.

## Instalasi

1. Install SUMO dan Python 3.x.
2. Install dependensi Python:
   ```
   pip install -r requirements.txt
   ```

## Menjalankan Simulasi

1. Jalankan SUMO dengan file jaringan dan rute yang tersedia di folder `data/`.
2. Jalankan skrip Python utama untuk menghubungkan ke SUMO dan mengelola simulasi parkir.

## Struktur Folder

- `data/` : berisi file jaringan, rute, dan poligon SUMO.
- `requirements.txt` : dependensi Python.
- `README.MD` : dokumentasi ini.

## Catatan

Pastikan SUMO sudah terinstall dan path-nya sudah ditambahkan ke environment variable.

---

# Smart Parking Finder System - Simulasi SUMO

Memanfaatkan AIoT untuk Deteksi dan Pencarian Tempat Parkir secara Real-Time

---

## Struktur File

```
Smart-Parking-Finder-System/
├── data/
│   ├── map.osm                  # Peta OpenStreetMap
│   ├── map.net.xml              # Jaringan SUMO hasil konversi
│   ├── map.sumocfg              # Konfigurasi utama simulasi
│   ├── map.rou.xml              # Rute dan kendaraan
│   ├── parking.add.xml          # Definisi parking area
│   ├── tripinfo.xml             # Output statistik perjalanan
│   └── map.poly.xml             # Poligon bangunan/taman
├── scripts/
│   ├── run_simulation.py        # Skrip utama menjalankan simulasi
│   ├── analyze_tripinfo.py      # Analisis hasil simulasi
│   └── parking_dashboard.py     # Dashboard real-time (Flask)
├── images/                      # Folder penyimpanan visualisasi
├── docs/
│   └── TODOLIST.MD              # Rencana proyek dan presentasi
├── README.MD                    # Dokumentasi utama
└── requirements.txt             # Dependensi Python
```

---

## Cara Menjalankan Simulasi

### 1. Persiapan

- **Instal SUMO:** Download dari [SUMO Download](https://sumo.dlr.de/docs/Downloads.html)
- **Instal dependensi Python:**
    ```bash
    pip install -r requirements.txt
    ```
    (Dependensi: traci, pandas, matplotlib, flask)

---

### 2. Konversi Peta OSM ke Jaringan SUMO

```bash
# Konversi file OSM ke format SUMO
netconvert --osm-files data/map.osm -o data/map.net.xml --roundabouts.guess --tls.guess-signals true
```

---

### 3. Tambahkan Parking Area

Buat file `data/parking.add.xml`:

```xml
<additional>
  <!-- Parking Area Pinggir Jalan -->
  <parkingArea id="P1" lane="edge1_0" startPos="10" endPos="30" roadsideCapacity="5"/>
  
  <!-- Car Park Terstruktur -->
  <parkingArea id="CarParkA" lane="b_0" startPos="240" endPos="260" width="5" length="10" angle="30">
    <space x="853" y="623"/>  <!-- Slot 1 -->
    <space x="860" y="620"/>  <!-- Slot 2 -->
  </parkingArea>
</additional>
```

---

### 4. Buat Rute Kendaraan

File `data/map.rou.xml`:

```xml
<routes>
  <vType id="car" accel="2.6" decel="4.5" length="5.0" minGap="2.5"/>
  
  <route id="r1" edges="edgeA edgeB edgeC"/>
  
  <vehicle id="v1" type="car" route="r1" depart="0">
    <stop parkingArea="P1" duration="60"/>  <!-- Parkir 60 detik -->
  </vehicle>
</routes>
```

---

### 5. Konfigurasi Simulasi

File `data/map.sumocfg`:

```xml
<configuration>
  <input>
    <net-file value="map.net.xml"/>
    <route-files value="map.rou.xml"/>
    <additional-files value="parking.add.xml"/>
  </input>
  <time>
    <begin value="0"/>
    <end value="3600"/>  <!-- Durasi simulasi: 1 jam -->
  </time>
  <output>
    <tripinfo-output value="tripinfo.xml"/>
  </output>
</configuration>
```

---

### 6. Jalankan Simulasi

```bash
python scripts/run_simulation.py
```
Skrip akan:
- Memulai simulasi SUMO-GUI
- Membaca status slot parkir setiap 5 detik
- Mencatat data ketersediaan parkir ke file log

---

### 7. Analisis Hasil Simulasi

```bash
python scripts/analyze_tripinfo.py
```
Output:
- Statistik rata-rata waktu pencarian parkir
- Grafik utilisasi slot parkir
- File `images/parking_analysis.png`

---

### 8. Dashboard Real-Time (Opsional)

```bash
python scripts/parking_dashboard.py
```
Buka [http://localhost:5000](http://localhost:5000) di browser untuk melihat:
- Peta live ketersediaan slot parkir
- Persentase utilisasi per area

---

## Penjelasan Skrip Utama

**scripts/run_simulation.py**
```python
import traci
import time
from datetime import datetime

# Inisialisasi simulasi
sumo_cmd = ["sumo-gui", "-c", "data/map.sumocfg"]
traci.start(sumo_cmd)

# File log status parkir
log_file = open("parking_log.csv", "w")
log_file.write("timestamp,parking_area,occupied_slots,total_slots\n")

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Pantau semua parking area
    for area_id in traci.parkingarea.getIDList():
        total_slots = traci.parkingarea.getRoadsideCapacity(area_id)
        occupied_slots = traci.parkingarea.getVehicleCount(area_id)
        log_file.write(f"{current_time},{area_id},{occupied_slots},{total_slots}\n")
    
    time.sleep(0.1)  # Perlambat simulasi untuk observasi

traci.close()
log_file.close()
```

**scripts/analyze_tripinfo.py**
```python
import pandas as pd
import matplotlib.pyplot as plt
from xml.etree import ElementTree as ET

# Analisis tripinfo.xml
tree = ET.parse('data/tripinfo.xml')
root = tree.getroot()

parking_data = []
for trip in root.findall('tripinfo'):
    if 'parking' in trip.attrib:
        parking_data.append({
            'vehicle': trip.get('id'),
            'parking_area': trip.get('parking'),
            'duration': float(trip.get('parkingDuration'))
        })

df = pd.DataFrame(parking_data)
print(f"Rata-rata waktu parkir: {df['duration'].mean():.2f} detik")

# Visualisasi
plt.figure(figsize=(10, 6))
df.groupby('parking_area')['duration'].mean().plot(kind='bar')
plt.title('Rata-rata Durasi Parkir per Area')
plt.ylabel('Detik')
plt.savefig('images/parking_duration.png')
```

**scripts/parking_dashboard.py**
```python
from flask import Flask, render_template
import traci
import threading

app = Flask(__name__)

def run_simulation():
    traci.start(["sumo", "-c", "data/map.sumocfg"])
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

@app.route('/')
def dashboard():
    parking_status = {}
    for area_id in traci.parkingarea.getIDList():
        total = traci.parkingarea.getRoadsideCapacity(area_id)
        occupied = traci.parkingarea.getVehicleCount(area_id)
        parking_status[area_id] = {
            'occupied': occupied,
            'total': total,
            'percentage': (occupied / total) * 100 if total > 0 else 0
        }
    return render_template('dashboard.html', parking=parking_status)

if __name__ == '__main__':
    threading.Thread(target=run_simulation).start()
    app.run(port=5000)
```

---

## Troubleshooting

| Masalah                      | Penyebab Umum                            | Solusi                                   |
|------------------------------|------------------------------------------|------------------------------------------|
| Parking area tidak terdeteksi | File tidak terdaftar di .sumocfg         | Tambahkan di `<additional-files>`        |
| Kendaraan tidak parkir        | Salah ID di `<stop>`                     | Verifikasi ID di rou.xml dan add.xml     |
| Simulasi terlalu cepat        | GUI SUMO tanpa delay                     | Tambahkan `time.sleep(0.1)` di loop      |
| Dashboard tidak update        | Tidak ada threading                      | Gunakan threading untuk simulasi background |

---

## Work in Progress & Next Steps

- **Integrasi Prediksi AI**
    - Tambahkan model LSTM untuk prediksi ketersediaan parkir  
      _File: scripts/parking_prediction.py_
- **Optimasi Parkir**
    - Algoritma penugasan slot berbasis jarak terdekat  
      _File: scripts/parking_optimizer.py_
- **Simulasi Jam Sibuk**
    - Generate 200+ kendaraan dengan randomTrips.py  
      _Parameter: --begin 300 --end 600_
- **Deploy Cloud**
    - Dockerize aplikasi  
      _File: Dockerfile dan docker-compose.yml_

---

## Referensi

- [SUMO Parking Area](https://sumo.dlr.de/docs/Simulation/ParkingArea.html)
- [Konversi OSM → SUMO](https://sumo.dlr.de/docs/Networks/Import/OpenStreetMap.html)
- [Netedit Tutorial](https://sumo.dlr.de/docs/NETEDIT.html)

---

## Catatan Penting

- Parking area harus didefinisikan sebagai additional element.
- Kendaraan otomatis reroute jika slot penuh (kecuali diatur `parking="true"` di rute).
- Gunakan `sumo --help` untuk opsi lanjutan (misal: `--device.parking.probability` untuk atur probabilitas parkir).