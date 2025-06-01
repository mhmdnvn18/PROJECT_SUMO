# SUMO Parking Area Simulation

Simulasi area parkir menggunakan SUMO, mulai dari peta OSM, penambahan parking area, hingga analisis perilaku parkir kendaraan.

---

## Struktur File

- `map.osm` : Data peta dari OpenStreetMap
- `map.net.xml` : Jaringan jalan hasil konversi OSM
- `map.sumocfg` : Konfigurasi utama simulasi SUMO
- `map.rou.xml` : Rute dan kendaraan (termasuk perintah parkir)
- `parking.add.xml` : (Opsional) File tambahan untuk definisi parking area
- `tripinfo.xml` : Output statistik perjalanan
- `README.MD` : Dokumentasi dan petunjuk penggunaan

---

## Cara Menjalankan Simulasi Parking Area

### 1. Persiapan Data

- Ekspor area peta dari [openstreetmap.org](https://www.openstreetmap.org/export) dan simpan sebagai `map.osm`.

### 2. Konversi OSM ke SUMO Network

Jalankan perintah berikut untuk mengkonversi file OSM ke jaringan SUMO:

```bash
netconvert --osm-files map.osm -o map.net.xml
```

### 3. (Opsional) Tambahkan Poligon

Jika ingin menampilkan bangunan/taman:

```bash
polyconvert --net-file map.net.xml --osm-files map.osm -o map.poly.xml
```

### 4. Definisikan Parking Area

- Edit `map.net.xml` secara manual, atau gunakan netedit.
- Tambahkan elemen `<parkingArea>` pada lane yang diinginkan, misal:
  ```xml
  <parkingArea id="P1" lane="edge1_0" startPos="10" endPos="30" roadsideCapacity="5"/>
  ```
- Untuk parkir khusus/car park, gunakan atribut tambahan dan/atau `<space>`:
  ```xml
  <parkingArea id="ParkAreaB" lane="b_0" startPos="240" endPos="260" roadsideCapacity="0" width="5" length="10" angle="30">
      <space x="853" y="623"/>
      <!-- dst -->
  </parkingArea>
  ```
- Jika parking area diletakkan di file terpisah (`parking.add.xml`), tambahkan ke konfigurasi SUMO melalui parameter `--additional-files` di file `.sumocfg`.

### 5. Buat File Rute dan Kendaraan

- Buat file rute (`map.rou.xml`) yang mendefinisikan kendaraan dan rutenya.
- Tambahkan perintah stop di parking area:
  ```xml
  <vehicle id="veh1" route="r1">
      <stop parkingArea="P1" duration="60"/>
  </vehicle>
  ```

### 6. Buat File Konfigurasi SUMO

- Buat file `map.sumocfg` yang memuat file jaringan, rute, dan (jika perlu) additional files:
  ```xml
  <input>
      <net-file value="map.net.xml"/>
      <route-files value="map.rou.xml"/>
      <additional-files value="parking.add.xml"/>
  </input>
  ```

### 7. Jalankan Simulasi

Jalankan simulasi dengan SUMO-GUI:

```bash
sumo-gui -c map.sumocfg
```

### 8. Analisis dan Visualisasi

- Amati perilaku kendaraan saat parkir di SUMO-GUI.
- Analisis hasil simulasi (misal, jumlah kendaraan parkir, waktu parkir, dsb) dari file output seperti `tripinfo.xml`.

---

## Penjelasan Atribut Parking Area

- `id`: Identitas unik parking area.
- `lane`: Jalur (lane) tempat parking area berada.
- `startPos` & `endPos`: Posisi awal dan akhir parking area pada lane (meter).
- `roadsideCapacity`: Jumlah slot parkir di pinggir jalan.
- `angle`, `width`, `length`: Sudut dan ukuran slot parkir.
- `onRoad`, `lefthand`, `acceptedBadges`, `name`: Opsi tambahan.
- `<space>`: Definisi slot parkir individual (untuk car park).

---

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---------|----------|--------|
| Kendaraan tidak parkir | Salah penulisan id parking area atau tidak ada perintah `<stop parkingArea=...>` | Periksa id dan rute kendaraan |
| Parking area tidak muncul | Salah posisi/atribut di file .net.xml | Edit ulang dengan netedit atau cek manual |
| Simulasi error | File belum terhubung di `.sumocfg` | Pastikan semua file sudah dicantumkan |

---

## Catatan

- Parking area harus dimasukkan ke konfigurasi SUMO melalui parameter `--additional-files`.
- Jika parking area penuh, kendaraan dapat menunggu atau melakukan reroute ke area lain secara otomatis.
- Untuk fitur lanjutan (reservasi, badge, dsb), lihat dokumentasi SUMO.

---

## Referensi

- [SUMO Parking Area Documentation](https://sumo.dlr.de/docs/Simulation/ParkingArea.html)
- [SUMO Networks from OSM](https://sumo.dlr.de/docs/Networks/Import/OpenStreetMap.html)
- [SUMO Tools](https://sumo.dlr.de/docs/Tools/)

