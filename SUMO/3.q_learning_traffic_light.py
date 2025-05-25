import traci
import random
import numpy as np
import os

# Parameters
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.1
PHASES = [0, 2]  # assume 2 phases for simplicity
PHASE_DURATION = 10

# State definition: we simplify it as [vehicles in N/S lanes, vehicles in E/W lanes]
def get_state(tls_id):
    lanes = traci.trafficlight.getControlledLanes(tls_id)
    ns_lanes = [lane for lane in lanes if "north" in lane or "south" in lane]
    ew_lanes = [lane for lane in lanes if "east" in lane or "west" in lane]
    
    ns_density = sum([traci.lane.getLastStepVehicleNumber(lane) for lane in ns_lanes])
    ew_density = sum([traci.lane.getLastStepVehicleNumber(lane) for lane in ew_lanes])

    return (min(ns_density, 10), min(ew_density, 10))  # clip to 10

# Reward: reduction in total queue length
def get_reward(prev_state, new_state):
    return (sum(prev_state) - sum(new_state))

# Choose action using epsilon-greedy policy
def choose_action(state, q_table):
    if random.uniform(0, 1) < EPSILON or state not in q_table:
        return random.choice(PHASES)
    return max(q_table[state], key=q_table[state].get)

# Update Q-value
def update_q_table(q_table, state, action, reward, next_state):
    if state not in q_table:
        q_table[state] = {a: 0 for a in PHASES}
    if next_state not in q_table:
        q_table[next_state] = {a: 0 for a in PHASES}

    old_q = q_table[state][action]
    future_q = max(q_table[next_state].values())
    q_table[state][action] = old_q + ALPHA * (reward + GAMMA * future_q - old_q)

# Run simulation

def run():
    q_table = {}
    sumo_cmd = ["sumo-gui", "-c", "map.sumocfg", "--tripinfo-output", "tripinfo_qlearning.xml"]
    traci.start(sumo_cmd)

    tls_id = traci.trafficlight.getIDList()[0]
    print(f"Controlling traffic light: {tls_id}")

    step = 0
    prev_state = get_state(tls_id)
    current_phase = PHASES[0]
    traci.trafficlight.setPhase(tls_id, current_phase)
    phase_timer = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        # Deteksi kendaraan IoT-enabled di setiap edge (bisa dipakai sebagai state Q-Learning)
        iot_counts = {}
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
            iot_counts[edge] = iot_count
        # iot_counts dapat digunakan sebagai bagian dari state Q-Learning

        step += 1
        phase_timer += 1

        if phase_timer >= PHASE_DURATION:
            new_state = get_state(tls_id)
            reward = get_reward(prev_state, new_state)

            action = choose_action(prev_state, q_table)
            traci.trafficlight.setPhase(tls_id, action)

            update_q_table(q_table, prev_state, action, reward, new_state)

            prev_state = new_state
            phase_timer = 0

    traci.close()
    print("✅ Simulasi Q-Learning selesai")

if __name__ == "__main__":
    run()
