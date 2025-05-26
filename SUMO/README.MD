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
- [x] **Minimal 10 kendaraan, rute berbeda**: Perlu dicek di `map.rou.xml`, pastikan sudah ada 10+ kendaraan dengan rute berbeda.
- [ ] **Tipe kendaraan IoT-enabled**: Pastikan ada kendaraan dengan `vtype="iot"` di file route.

### 4. Simulate IoT-enabled Traffic Management
- [x] **Implementasi adaptive traffic light**: Ada di `1.adaptive_traffic_light.py` (menggunakan TraCI).
- [x] **Deteksi kendaraan IoT**: Sudah ada logika deteksi kendaraan IoT di script.
- [x] **Penyesuaian traffic light berbasis density**: Sudah diimplementasikan.

### 5. Visualize and Analyze Results
- [x] **Simulasi dapat dijalankan di SUMO-GUI**: Sudah.
- [x] **Analisis tripinfo.xml**: Ada script `analyze_tripinfo.py` untuk analisis.
- [ ] **Diskusi dampak IoT-based adaptive traffic control**: Belum ada penjelasan/analisis tertulis, tambahkan di README atau file laporan.

---

## Saran Perbaikan

1. **Pastikan di file route (.rou.xml) sudah ada kendaraan IoT-enabled**  
   - Tambahkan `<vType id="iot" ...>` dan beberapa kendaraan dengan `type="iot"`.

2. **Pastikan minimal 10 kendaraan dengan rute berbeda**  
   - Cek dan tambahkan jika perlu di `map.rou.xml`.

3. **Tambahkan diskusi/analisis dampak**  
   - Tambahkan bagian di README atau file laporan (misal `RANGKUMAN.MD`) yang membahas hasil simulasi dan dampak pengendalian lampu lalu lintas berbasis IoT terhadap kemacetan.

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

**Catatan:**  
Jika sudah memenuhi semua checklist di atas, project sudah sesuai kriteria. Jika belum, lakukan perbaikan sesuai saran.
