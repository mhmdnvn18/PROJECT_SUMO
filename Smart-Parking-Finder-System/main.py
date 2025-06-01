import os
import sys
import traci

SUMO_BINARY = "sumo"  # atau "sumo-gui" jika ingin GUI
SUMO_CONFIG = "data/map.sumocfg"

def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        # Ambil status parkir
        parking_areas = traci.parkingarea.getIDList()
        for pid in parking_areas:
            occupied = traci.parkingarea.getVehicleCount(pid)
            capacity = traci.parkingarea.getCapacity(pid)
            print(f"Step {step} | ParkingArea {pid}: {occupied}/{capacity} occupied")
        step += 1
    traci.close()

if __name__ == "__main__":
    if "SUMO_HOME" in os.environ:
        tools = os.path.join(os.environ["SUMO_HOME"], "tools")
        sys.path.append(tools)
    else:
        sys.exit("Please declare environment variable 'SUMO_HOME'")

    sumo_cmd = [SUMO_BINARY, "-c", SUMO_CONFIG, "--start", "--quit-on-end"]
    traci.start(sumo_cmd)
    run()
