import traci
import random
import numpy as np
import os
import csv

# Parameters
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.1
PHASES = [0, 2]  # assume 2 phases for simplicity
PHASE_DURATION = 10

LANE_NAMES = ["N", "S", "E", "W"]  # for logging

def get_lane_ids(tls_id):
    lanes = traci.trafficlight.getControlledLanes(tls_id)
    # Map lanes to directions (assumes lane naming convention)
    lane_map = {"N": [], "S": [], "E": [], "W": []}
    for lane in lanes:
        lname = lane.lower()
        if "north" in lname or lname.endswith("n"):
            lane_map["N"].append(lane)
        elif "south" in lname or lname.endswith("s"):
            lane_map["S"].append(lane)
        elif "east" in lname or lname.endswith("e"):
            lane_map["E"].append(lane)
        elif "west" in lname or lname.endswith("w"):
            lane_map["W"].append(lane)
    return lane_map

# State definition: we simplify it as [vehicles in N/S lanes, vehicles in E/W lanes]
def get_state(tls_id, lane_map):
    veh_counts = []
    waitings = []
    for d in LANE_NAMES:
        lanes = lane_map[d]
        count = sum([traci.lane.getLastStepVehicleNumber(lane) for lane in lanes])
        veh_counts.append(min(count, 10))
        # Average waiting time per lane
        if lanes:
            avg_wait = np.mean([traci.lane.getWaitingTime(lane) for lane in lanes])
        else:
            avg_wait = 0
        waitings.append(round(avg_wait, 1))
    phase = traci.trafficlight.getPhase(tls_id)
    # State: (veh_N, veh_S, veh_E, veh_W, wait_N, wait_S, wait_E, wait_W, phase)
    return tuple(veh_counts + waitings + [phase])

# Reward: reduction in total queue length
def get_reward(prev_state, new_state):
    # Negative reward for waiting time, penalty for long queues, bonus for reduction
    prev_wait = sum(prev_state[4:8])
    new_wait = sum(new_state[4:8])
    prev_queue = sum(prev_state[0:4])
    new_queue = sum(new_state[0:4])
    reward = (prev_wait - new_wait) - 0.5 * (new_queue)  # encourage reducing wait, penalize queue
    return reward

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
    lane_map = get_lane_ids(tls_id)
    print(f"Controlling traffic light: {tls_id}")

    step = 0
    prev_state = get_state(tls_id, lane_map)
    current_phase = PHASES[0]
    traci.trafficlight.setPhase(tls_id, current_phase)
    phase_timer = 0

    # Logging for analysis
    log_path = "traffic_signal_data.csv"
    with open(log_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["step"] + [f"veh_{d}" for d in LANE_NAMES] + [f"wait_{d}" for d in LANE_NAMES] + ["phase"])

        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            step += 1
            phase_timer += 1

            state = get_state(tls_id, lane_map)
            # Log data
            writer.writerow([step] + list(state[:-1]) + [state[-1]])

            if phase_timer >= PHASE_DURATION:
                new_state = get_state(tls_id, lane_map)
                reward = get_reward(prev_state, new_state)
                action = choose_action(prev_state, q_table)
                traci.trafficlight.setPhase(tls_id, action)
                update_q_table(q_table, prev_state, action, reward, new_state)
                prev_state = new_state
                phase_timer = 0

    traci.close()
    print("✅ Simulasi Q-Learning selesai. Data saved to traffic_signal_data.csv")

if __name__ == "__main__":
    run()
