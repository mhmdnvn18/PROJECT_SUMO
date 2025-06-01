import os
import sys
import traci

if 'SUMO_HOME' not in os.environ:
    sys.exit("Please set the SUMO_HOME environment variable.")

sumo_binary = "sumo"
sumo_config = "data/map.sumocfg"

def main():
    traci.start([sumo_binary, "-c", sumo_config])
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step += 1
    traci.close()

if __name__ == "__main__":
    main()
