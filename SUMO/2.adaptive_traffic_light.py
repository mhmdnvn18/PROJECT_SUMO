import traci

def run():
    # Jalankan SUMO GUI dengan output tripinfo_adaptive.xml
    sumo_cmd = ["sumo-gui", "-c", "map.sumocfg", "--tripinfo-output", "tripinfo_adaptive.xml"]
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

            # Evaluasi lebih sering (setiap 5 detik)
            if step % 5 == 0:
                print(f"[{step}s] {tls_id} total kendaraan: {total_vehicles}")

                # Jika ada lajur dengan antrian > 8, beri hijau lebih lama
                if max(lane_vehicle_counts) > 8:
                    traci.trafficlight.setPhaseDuration(tls_id, 25)
                # Jika semua lajur < 3, siklus cepat
                elif max(lane_vehicle_counts) < 3:
                    traci.trafficlight.setPhaseDuration(tls_id, 8)
                # Normal
                else:
                    traci.trafficlight.setPhaseDuration(tls_id, 15)

    traci.close()
    print("✅ Simulasi selesai.")

if __name__ == "__main__":
    run()
