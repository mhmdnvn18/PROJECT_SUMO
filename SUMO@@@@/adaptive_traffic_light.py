import traci

# Mulai SUMO GUI dengan file konfigurasi dan output tripinfo
traci.start(["sumo-gui", "-c", "map.sumocfg", "--tripinfo-output", "tripinfo.xml"])

# Ambil daftar traffic light di jaringan
tls_ids = traci.trafficlight.getIDList()
if not tls_ids:
    print("Tidak ditemukan lampu lalu lintas. Silakan tambahkan lampu dengan Netedit.")
    traci.close()
    exit()

# Simulasi hingga selesai
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    for tls in tls_ids:
        lanes = traci.trafficlight.getControlledLanes(tls)
        for lane in lanes:
            num_veh = traci.lane.getLastStepVehicleNumber(lane)
            if num_veh > 5:
                # Tambah durasi hijau jika kendaraan banyak
                curr_duration = traci.trafficlight.getPhaseDuration(tls)
                traci.trafficlight.setPhaseDuration(tls, curr_duration + 5)
traci.close()
