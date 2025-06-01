import traci
import time

SUMO_BINARY = "sumo"  # atau "sumo-gui" jika ingin mode GUI
SUMO_CONFIG = "random.sumocfg"

def monitor_parking():
    traci.start([SUMO_BINARY, "-c", SUMO_CONFIG])
    print("Monitoring parking areas... (Ctrl+C to stop)")
    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            parking_status = {}
            for area in traci.parkingarea.getIDList():
                occupied = traci.parkingarea.getVehicleIDs(area)
                parking_status[area] = "Penuh" if occupied else "Kosong"
            # Tampilkan status real-time
            print(parking_status)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        traci.close()

if __name__ == "__main__":
    monitor_parking()
