# Sistem Pencari Parkir Pintar - Skenario SUMO

Direktori ini berisi skenario SUMO (Simulation of Urban MObility) untuk simulasi Sistem Pencari Parkir Pintar pada jaringan grid acak.

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

- `rou/buses.flows.xml`  
  Definisi alur dan rute bus.

## Cara Penggunaan

1. **Instalasi SUMO**  
   Unduh dan instal SUMO dari [https://www.eclipse.org/sumo/](https://www.eclipse.org/sumo/).

2. **Menjalankan Simulasi**  
   Buka terminal pada direktori ini dan jalankan:
   ```
   sumo-gui -c random.sumocfg
   ```
   atau untuk mode command-line:
   ```
   sumo -c random.sumocfg
   ```

3. **Deskripsi Skenario**  
   - Skenario ini mensimulasikan berbagai tipe kendaraan (komersial, penumpang, PTW, bus) yang bergerak di jaringan grid.
   - Kendaraan mencari area parkir, berinteraksi dengan rerouter, dan bus mengikuti rute serta halte yang telah ditentukan.

## Kustomisasi

- Edit file `.xml` untuk mengubah jaringan, tipe kendaraan, rute, area parkir, atau halte bus.
- Tambahkan atau modifikasi alur pada direktori `rou/` untuk pola lalu lintas yang berbeda.

## Kebutuhan

- Disarankan menggunakan SUMO versi 1.8.0 atau lebih baru.
- Python (opsional, untuk scripting lanjutan atau pembuatan skenario).

## Lisensi

Skenario ini disediakan untuk keperluan akademik dan riset.
