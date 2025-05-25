import traci

def run():
    # Jalankan SUMO GUI dengan output tripinfo.xml
    sumo_cmd = ["sumo-gui", "-c", "map.sumocfg", "--tripinfo-output", "tripinfo.xml"]
    traci.start(sumo_cmd)

    tls_ids = traci.trafficlight.getIDList()

    if not tls_ids:
        print("❌ Tidak ditemukan lampu lalu lintas di jaringan. Tambahkan dulu lewat netedit.")
        traci.close()
        return

    print(f"✅ Ditemukan lampu lalu lintas: {tls_ids}")

    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step += 1

        for tls_id in tls_ids:
            lanes = traci.trafficlight.getControlledLanes(tls_id)
            lane_vehicle_counts = [traci.lane.getLastStepVehicleNumber(lane) for lane in lanes]
            total_vehicles = sum(lane_vehicle_counts)
            max_lane_vehicles = max(lane_vehicle_counts) if lane_vehicle_counts else 0

            # Update lebih sering, misal setiap 5 detik
            if step % 5 == 0:  # Setiap 5 detik simulasi
                print(f"[{step}s] {tls_id} total kendaraan: {total_vehicles}, antrean terpanjang: {max_lane_vehicles}")

                if max_lane_vehicles > 8:
                    # Jika antrean panjang, tambah durasi hijau lebih banyak
                    traci.trafficlight.setPhaseDuration(tls_id, 45)
                elif total_vehicles < 3:
                    # Jika sepi, kurangi durasi hijau
                    traci.trafficlight.setPhaseDuration(tls_id, 10)
                else:
                    # Normal
                    traci.trafficlight.setPhaseDuration(tls_id, 25)

    traci.close()
    print("✅ Simulasi selesai.")

if __name__ == "__main__":
    run()
