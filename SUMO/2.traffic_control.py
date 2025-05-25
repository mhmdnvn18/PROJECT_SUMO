import traci
import sumolib
import sys

# Path ke executable SUMO; bisa menggunakan sumo-gui atau sumo (non-gui)
SUMO_BINARY = "sumo-gui"  # atau "sumo"
net_file = "map.net.xml"
route_file = "map.rou.xml"
sumo_cmd = [SUMO_BINARY, "-n", net_file, "-r", route_file, "--start"]

def get_lane_density(lane_id):
    """
    Menghitung jumlah kendaraan pada lajur tertentu secara real-time.
    """
    return traci.lane.getLastStepVehicleNumber(lane_id)

def get_controlled_lanes(tls_id):
    """
    Mengambil list lajur (lane) yang masuk ke persimpangan di bawah kontrol tls_id.
    """
    controlled_links = traci.trafficlight.getControlledLinks(tls_id)
    lane_ids = []
    for phase_links in controlled_links:
        for tl_link in phase_links:
            from_edge = tl_link[0]
            via_lane = tl_link[2]
            lane_ids.append(f"{from_edge}_{via_lane}")
    return lane_ids

def run():
    sumo_cmd = ["sumo-gui", "-c", "map.sumocfg", "--tripinfo-output", "tripinfo_control.xml"]
    traci.start(sumo_cmd)
    tls_id = "tl_1"  # Ganti sesuai ID lampu lalu lintas di jaringan Anda
    step = 0

    default_green = 30
    min_green = 10
    max_green = 60

    # Atur durasi awal untuk dua fasa utama (misal NS dan EW)
    traci.trafficlight.setPhaseDuration(tls_id, default_green)  # fasa 0
    traci.trafficlight.setPhaseDuration(tls_id, default_green)  # fasa 1

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        # Contoh: deteksi kendaraan IoT-enabled di setiap edge
        for edge in traci.edge.getIDList():
            veh_ids = traci.edge.getLastStepVehicleIDs(edge)
            iot_count = 0
            for vid in veh_ids:
                try:
                    vtype = traci.vehicle.getTypeID(vid)
                    if vtype == "iot":
                        iot_count += 1
                except traci.TraCIException:
                    continue
            # Data iot_count dapat digunakan untuk logika kontrol lampu

        step += 1

        if step % 5 == 0:
            lane_ids = get_controlled_lanes(tls_id)
            # Misal phase 0: lajur 0-1, phase 1: lajur 2-3 (ubah sesuai topologi Anda)
            vehicles_phase0 = sum(get_lane_density(lid) for lid in lane_ids[0:2])
            vehicles_phase1 = sum(get_lane_density(lid) for lid in lane_ids[2:4])

            current_phase = traci.trafficlight.getPhase(tls_id)

            if current_phase == 0:
                new_duration = default_green
                if vehicles_phase0 > 5:
                    new_duration = min(default_green + 5, max_green)
                elif vehicles_phase0 < 2:
                    new_duration = max(default_green - 5, min_green)
                traci.trafficlight.setPhaseDuration(tls_id, new_duration)
            elif current_phase == 2:
                new_duration = default_green
                if vehicles_phase1 > 5:
                    new_duration = min(default_green + 5, max_green)
                elif vehicles_phase1 < 2:
                    new_duration = max(default_green - 5, min_green)
                traci.trafficlight.setPhaseDuration(tls_id, new_duration)

    traci.close()
    sys.stdout.flush()

if __name__ == "__main__":
    run()
