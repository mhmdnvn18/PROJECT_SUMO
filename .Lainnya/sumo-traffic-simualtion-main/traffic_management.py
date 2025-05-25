import os
import sys
import traci
import time
from sumolib import net
import pandas as pd
import xml.etree.ElementTree as ET

try:
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
        from sumolib import checkBinary
    else:
        sys.exit("SUMO_HOME not found!")
except ImportError as e:
    sys.exit(f"Error importing SUMO tools: {e}")

sumo_binary = checkBinary('sumo-gui')
sumo_config = "osm.sumocfg"
route = "bsdroute.rou.xml"
net_file = "osm.net.xml"

traffic_light_id = 'joinedS_6421159832_cluster_3639980474_3640024452_3640024453_6421159827_#4more_cluster_6421159831_7129012339'
congestion_threshold = 5
adjustment_step = 5
max_green_duration = 50
min_green_duration = 10
detector_position_offset = 5

edges_for_detectors = {
    "754598165#2": "north",
    "1053267667#3": "south",
    "749662140#0": "east",
    "885403818#2": "west",
}

def get_approach_lanes(net_obj, edge_mapping):
    approach_lanes = {direction: [] for direction in edge_mapping.values()}
    lane_to_approach = {}

    for edge_id, direction in edge_mapping.items():
        edge = net_obj.getEdge(edge_id)
        if edge is None:
            print(f"Warning: Edge '{edge_id}' not found in network.")
            continue 
        if edge.getFunction() != 'internal':
            for lane in edge.getLanes():
                lane_id = lane.getID()
                approach_lanes[direction].append(lane_id)
                lane_to_approach[lane_id] = direction
        else:
            print(f"Warning: Edge '{edge_id}' is an internal edge. Detectors should be on approach edges. Skipping.")
    return approach_lanes, lane_to_approach

def create_additional_file(filename, net_obj, lane_to_approach_map):
    with open(filename, "w") as f:
        f.write('<additional>\n')
        detector_count = 0
        for lane_id in lane_to_approach_map.keys():
            try:
                lane = net_obj.getLane(lane_id)
                if lane is None:
                    print(f"Warning: Lane '{lane_id}' not found while creating detectors. Skipping.")
                    continue
                length = lane.getLength()
                position = max(0.1, length - detector_position_offset)
                detector_id = f"det_{lane_id}"
                f.write(f'  <inductionLoop id="{detector_id}" lane="{lane_id}" pos="{position:.2f}" freq="1" file="detectors_output.xml"/>\n')
                detector_count += 1
            except Exception as e:
                print(f"Error processing lane {lane_id} for detector creation: {e}")
        f.write('</additional>\n')
        print(f"Generated {detector_count} induction loops.")

def get_phase_state_directions(net_obj, tls_id, phase_state_str):
    green_directions = set()
    try:
        controlled_links = traci.trafficlight.getControlledLinks(tls_id)
        if not controlled_links:
            print(f"Warning: No controlled links found for TLS '{tls_id}'. Cannot map phase states to directions.")
            return green_directions
        for i, state_char in enumerate(phase_state_str):
            if state_char.lower() == 'g':
                if i < len(controlled_links) and controlled_links[i]:
                    first_link_tuple = controlled_links[i][0]
                    if first_link_tuple:
                        from_lane_id = first_link_tuple[0]
                        from_lane = net_obj.getLane(from_lane_id)
                        if from_lane:
                            from_edge = from_lane.getEdge()
                            for edge_id, direction in edges_for_detectors.items():
                                if from_edge.getID() == edge_id:
                                    green_directions.add(direction)
                                    break
                        else:
                            print(f"Warning: Lane '{from_lane_id}' (from controlled link) not found in network.")
                else:
                     print(f"Warning: Mismatch between phase state length and controlled links for TLS '{tls_id}' at index {i}.")

    except traci.exceptions.TraCIException as e:
        print(f"TraCI Error getting controlled links for '{tls_id}': {e}")
    except Exception as e:
        print(f"Error mapping phase state to directions for TLS '{tls_id}': {e}")
    return green_directions

def run_simulation():
    net_obj = net.readNet(net_file)
    approach_lanes_map, lane_to_approach_map = get_approach_lanes(net_obj, edges_for_detectors)
    if not lane_to_approach_map:
        sys.exit("Error: No valid approach lanes found based on 'edges_for_detectors'. Cannot proceed.")

    additional_file = "detectors.add.xml"
    create_additional_file(additional_file, net_obj, lane_to_approach_map)
    
    sumo_cmd = [
        sumo_binary, "-c", sumo_config, 
        "--additional-files", additional_file, 
        "--tripinfo-output", "tripinfo.xml", 
        "--summary-output", "summary.xml", 
        "--no-step-log", "true", 
        "--time-to-teleport", "-1",
        "--duration-log.statistics",
        "--waiting-time-memory", "1000"
        ]
    traci.start(sumo_cmd)
    step = 0
    last_adjustment_time = -1
    min_time_between_adjustments = 10
    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            current_time = traci.simulation.getTime()
            traci.simulationStep()

            vehicle_counts = {direction: 0 for direction in edges_for_detectors.values()}
            for direction, lanes in approach_lanes_map.items():
                for lane_id in lanes:
                    detector_id = f"det_{lane_id}"
                    try:
                        count = traci.inductionloop.getLastStepVehicleNumber(detector_id)
                        vehicle_counts[direction] += count
                    except traci.exceptions.TraCIException as e:
                        print(f"Warning: TraCI error getting data for detector '{detector_id}': {e}. Skipping detector.")
                        pass
            congested_approaches = {approach for approach, count in vehicle_counts.items() if count >= congestion_threshold}
            try:
                time_to_switch = traci.trafficlight.getNextSwitch(traffic_light_id) - current_time
                logic_needs_update = False
                if time_to_switch <= 1.0 and (current_time - last_adjustment_time) > min_time_between_adjustments :
                    program_logic = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id)[0]
                    current_phase_index = traci.trafficlight.getPhase(traffic_light_id)
                    current_phase = program_logic.phases[current_phase_index]
                    current_phase_state = current_phase.state
                    current_green_directions = get_phase_state_directions(net_obj, traffic_light_id, current_phase_state)
                    is_current_phase_for_congested = any(d in congested_approaches for d in current_green_directions)
                    if 'g' in current_phase_state.lower():
                        if is_current_phase_for_congested:
                            original_duration = current_phase.duration
                            new_duration = min(original_duration + adjustment_step, max_green_duration)
                            if new_duration != original_duration:
                                print(f"Time {current_time:.1f}: Extending phase {current_phase_index} (Dirs: {current_green_directions}) for congestion in {congested_approaches}. Duration {original_duration} -> {new_duration}")
                                current_phase.duration = new_duration
                                logic_needs_update = True
                        elif congested_approaches:
                            original_duration = current_phase.duration
                            new_duration = max(original_duration - adjustment_step, min_green_duration)
                            if new_duration != original_duration:
                                print(f"Time {current_time:.1f}: Shortening phase {current_phase_index} (Dirs: {current_green_directions}) due to congestion elsewhere {congested_approaches}. Duration {original_duration} -> {new_duration}")
                                current_phase.duration = new_duration
                                logic_needs_update = True
                    for i, phase in enumerate(program_logic.phases):
                        if i == current_phase_index or 'g' not in phase.state.lower():
                            continue
                        phase_green_directions = get_phase_state_directions(net_obj, traffic_light_id, phase.state)
                        is_phase_for_congested = any(d in congested_approaches for d in phase_green_directions)
                        if not is_phase_for_congested and congested_approaches:
                            original_duration = phase.duration
                            new_duration = max(original_duration - adjustment_step, min_green_duration)
                            if new_duration != original_duration:
                                print(f"Time {current_time:.1f}: Shortening other green phase {i} (Dirs: {phase_green_directions}). Duration {original_duration} -> {new_duration}")
                                phase.duration = new_duration
                                logic_needs_update = True
                    if logic_needs_update:
                        traci.trafficlight.setProgramLogic(traffic_light_id, program_logic)
                        last_adjustment_time = current_time
            except traci.exceptions.TraCIException as e:
                print(f"Error during traffic light control at step {step}: {e}")
            if step % 20 == 0:
                print(f"Time: {current_time:.1f}, Counts: {vehicle_counts}, Congested: {congested_approaches}")
                try:
                    logic = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id)[0]
                    phase_idx = traci.trafficlight.getPhase(traffic_light_id)
                    print(f"  TLS Phase: {phase_idx}, State: {logic.phases[phase_idx].state}, Durations: {[p.duration for p in logic.phases]}")
                except traci.exceptions.TraCIException as e:
                    print(f"  Error getting TLS info: {e}")
            step += 1
    except traci.exceptions.FatalTraCIError as e:
        print(f"\nFatal TraCI Error during simulation: {e}")
        print("SUMO may have crashed. Check sumo_log.txt or run without GUI for more details.")
    except Exception as e:
         print(f"\nUnexpected Python error during simulation loop at step {step}: {e}")
         import traceback
         traceback.print_exc()
    finally:
        print("Closing TraCI connection.")
        traci.close()
        print("Simulation finished.")

def analyze_tripinfo(tripinfo_file_path):
    try:
        tree = ET.parse(tripinfo_file_path)
        root = tree.getroot()
        data = []
        missing_attrs = 0
        for tripinfo in root.findall('tripinfo'):
            try:
                trip_data = {
                    'id': tripinfo.get('id'),
                    'depart': float(tripinfo.get('depart')),
                    'arrival': float(tripinfo.get('arrival', -1.0)),
                    'duration': float(tripinfo.get('duration', 0.0)),
                    'waitingTime': float(tripinfo.get('waitingTime', 0.0)),
                    'timeLoss': float(tripinfo.get('timeLoss', 0.0)),
                    'departLane': tripinfo.get('departLane'),
                    'arrivalLane': tripinfo.get('arrivalLane'),
                }
                data.append(trip_data)
            except (TypeError, ValueError) as e:
                missing_attrs +=1
                continue
        if missing_attrs > 0:
             print(f"Skipped {missing_attrs} trips due to missing or invalid attributes in tripinfo file.")
        if not data:
            print("No valid trip data found in the file.")
            return
        df = pd.DataFrame(data)
        completed_trips = df[df['arrival'] > 0]
        if not completed_trips.empty:
            print(f"Total Trips: {len(df)}")
            print(f"Completed Trips: {len(completed_trips)}")
            print(f"  Average Duration:     {completed_trips['duration'].mean():.2f} s")
            print(f"  Average Waiting Time: {completed_trips['waitingTime'].mean():.2f} s")
            print(f"  Average Time Loss:    {completed_trips['timeLoss'].mean():.2f} s")
            last_arrival = completed_trips['arrival'].max()
            if last_arrival > 0:
                throughput_per_hour = len(completed_trips) / (last_arrival / 3600)
                print(f"  Overall Throughput:   {throughput_per_hour:.2f} veh/hour (based on last arrival at {last_arrival:.1f}s)")
            total_duration = completed_trips['duration'].sum()
            total_waiting = completed_trips['waitingTime'].sum()
            if total_duration > 0:
                perc_waiting = (total_waiting / total_duration) * 100
                print(f"  Avg. % Time Waiting:  {perc_waiting:.2f}%")
            print("\nDistribution Summary (Completed Trips):")
            print(completed_trips[['duration', 'waitingTime', 'timeLoss']].describe())
        else:
             print("No completed trips found to analyze.")

    except FileNotFoundError:
        print(f"Error: File '{tripinfo_file_path}' not found during analysis.")
    except ET.ParseError as e:
        print(f"Error: Could not parse XML file '{tripinfo_file_path}'. It might be corrupted or incomplete. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_simulation()
    analyze_tripinfo("tripinfo.xml")