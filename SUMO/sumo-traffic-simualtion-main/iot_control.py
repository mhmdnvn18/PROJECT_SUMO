import os
import sys
import traci
import time
from sumolib import net
import pandas as pd
import xml.etree.ElementTree as ET
import traci.exceptions
import traceback

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
communication_range = 100.0
congestion_threshold = 5
adjustment_step = 5
max_green_duration = 50
min_green_duration = 10
min_time_between_adjustments = 5
ev_type_id = "emergency" 
ev_clearance_check_edge_prefix = "gneE"

approach_edges = {
    "754598165#2": "north",
    "1053267667#3": "south",
    "749662140#0": "east",
    "885403818#2": "west",
}

def get_phase_index_for_direction(net_obj, tls_id, target_direction, current_program_logic):
    for i, phase in enumerate(current_program_logic.phases):
        phase_green_directions = get_phase_state_directions(net_obj, tls_id, phase.state)
        if target_direction in phase_green_directions:
            return i
    print(f"Warning: Could not find a green phase for direction '{target_direction}' in TLS '{tls_id}' logic.")
    return None

def get_phase_state_directions(net_obj, tls_id, phase_state_str):
    green_directions = set()
    try:
        controlled_links = traci.trafficlight.getControlledLinks(tls_id)
        if not controlled_links:
            return green_directions
        for i, state_char in enumerate(phase_state_str):
            if state_char.lower() == 'g':
                if i < len(controlled_links) and controlled_links[i]:
                    first_link_tuple = controlled_links[i][0]
                    if first_link_tuple:
                        from_lane_id = first_link_tuple[0]
                        try:
                            from_lane = net_obj.getLane(from_lane_id)
                            if from_lane:
                                from_edge = from_lane.getEdge()
                                from_edge_id = from_edge.getID()
                                if from_edge_id in approach_edges:
                                    green_directions.add(approach_edges[from_edge_id])
                        except KeyError:
                             print(f"Warning: Lane ID '{from_lane_id}' not found in network object during phase mapping.")
                        except Exception as e_inner:
                             print(f"Warning: Error processing lane {from_lane_id} in get_phase_state_directions: {e_inner}")

    except traci.exceptions.TraCIException as e:
        pass
    except Exception as e:
        print(f"Error mapping phase state to directions for TLS '{tls_id}': {e}")
    return green_directions


def run_simulation():
    net_obj = net.readNet(net_file)
    sumo_cmd = [
        sumo_binary, "-c", sumo_config, 
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
    active_ev_priority = None 
    ev_priority_release_time = -1
    try:
        if traffic_light_id not in traci.trafficlight.getIDList():
             print(f"\nFATAL ERROR: Traffic light ID '{traffic_light_id}' not found.")
             print(f"Available TLS IDs: {traci.trafficlight.getIDList()}")
             traci.close()
             return
        while traci.simulation.getMinExpectedNumber() > 0:
            current_time = traci.simulation.getTime()
            traci.simulationStep()
            vehicles_near_intersection = {direction: [] for direction in approach_edges.values()}
            all_vehicle_ids = traci.vehicle.getIDList()
            detected_ev = None
            ev_approach_direction = None
            min_ev_distance = float('inf')
            for vehID in all_vehicle_ids:
                try:
                    road_id = traci.vehicle.getRoadID(vehID)
                    if road_id in approach_edges:
                        approach_direction = approach_edges[road_id]
                        lane_id = traci.vehicle.getLaneID(vehID)
                        lane_pos = traci.vehicle.getLanePosition(vehID)
                        lane_len = traci.lane.getLength(lane_id)
                        dist_to_intersection = lane_len - lane_pos
                        if 0 <= dist_to_intersection <= communication_range:
                            veh_type = traci.vehicle.getTypeID(vehID)
                            veh_data = {
                                'id': vehID,
                                'speed': traci.vehicle.getSpeed(vehID),
                                'distance': dist_to_intersection,
                                'type': veh_type
                            }
                            vehicles_near_intersection[approach_direction].append(veh_data)
                            if veh_type == ev_type_id:
                                if dist_to_intersection < min_ev_distance:
                                    min_ev_distance = dist_to_intersection
                                    detected_ev = veh_data
                                    ev_approach_direction = approach_direction
                except traci.exceptions.TraCIException as e:
                     print(f"TraCI Warning for vehicle {vehID}: {e}")
                     pass
                except Exception as e:
                     print(f"Unexpected error processing vehicle {vehID}: {e}")
                     traceback.print_exc()
            vehicle_counts = {approach: len(vehicles) for approach, vehicles in vehicles_near_intersection.items()}
            congested_approaches = {approach for approach, count in vehicle_counts.items() if count >= congestion_threshold}
            ev_priority_active_this_step = False
            if active_ev_priority:
                 try:
                    ev_road_id = traci.vehicle.getRoadID(active_ev_priority)
                    if ev_road_id not in approach_edges:
                        print(f"--- Time {current_time:.1f}: EV {active_ev_priority} seems to have cleared. Releasing priority. ---")
                        active_ev_priority = None
                 except traci.exceptions.TraCIException:
                    print(f"--- Time {current_time:.1f}: Prioritized EV {active_ev_priority} no longer found. Releasing priority. ---")
                    active_ev_priority = None
            if not active_ev_priority and detected_ev:
                print(f"!!! Time {current_time:.1f}: EV {detected_ev['id']} detected on {ev_approach_direction} ({detected_ev['distance']:.1f}m). Activating priority. !!!")
                active_ev_priority = detected_ev['id']
                ev_priority_release_time = current_time + max_green_duration
                try:
                    program_logic = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id)[0]
                    target_phase_index = get_phase_index_for_direction(net_obj, traffic_light_id, ev_approach_direction, program_logic)
                    if target_phase_index is not None:
                        current_phase_index = traci.trafficlight.getPhase(traffic_light_id)
                        if current_phase_index != target_phase_index:
                            print(f"    Switching TLS {traffic_light_id} to phase {target_phase_index} for EV.")
                            traci.trafficlight.setPhase(traffic_light_id, target_phase_index)
                        else:
                             print(f"    TLS {traffic_light_id} already in correct phase ({target_phase_index}) for EV.")
                        # Force this phase duration temporarily (optional, can just rely on setPhase)
                        # program_logic.phases[target_phase_index].duration = max_green_duration # Hold it
                        # traci.trafficlight.setProgramLogic(traffic_light_id, program_logic) # Apply hold
                    else:
                         print(f"    ERROR: Cannot find suitable green phase for EV direction {ev_approach_direction}!")

                except traci.exceptions.TraCIException as e:
                    print(f"    Error setting EV priority phase: {e}")
                except Exception as e:
                    print(f"    Unexpected error during EV priority logic: {e}")
                    traceback.print_exc()
            if active_ev_priority:
                ev_priority_active_this_step = True
            if not ev_priority_active_this_step:
                try:
                    time_to_switch = traci.trafficlight.getNextSwitch(traffic_light_id) - current_time
                    if time_to_switch <= 1.5 and (current_time - last_adjustment_time) > min_time_between_adjustments :
                        program_logic = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id)[0]
                        current_phase_index = traci.trafficlight.getPhase(traffic_light_id)
                        current_phase = program_logic.phases[current_phase_index]
                        current_phase_state = current_phase.state
                        logic_needs_update = False
                        current_green_directions = get_phase_state_directions(net_obj, traffic_light_id, current_phase_state)
                        is_current_phase_for_congested = any(d in congested_approaches for d in current_green_directions)
                        if 'g' in current_phase_state.lower():
                            if is_current_phase_for_congested:
                                original_duration = current_phase.duration
                                new_duration = min(original_duration + adjustment_step, max_green_duration)
                                if new_duration != original_duration:
                                    current_phase.duration = new_duration
                                    logic_needs_update = True
                            elif congested_approaches: # Current phase not for congested, but others are
                                original_duration = current_phase.duration
                                new_duration = max(original_duration - adjustment_step, min_green_duration)
                                if new_duration != original_duration:
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
                                    phase.duration = new_duration
                                    logic_needs_update = True
                        if logic_needs_update:
                            traci.trafficlight.setProgramLogic(traffic_light_id, program_logic)
                            last_adjustment_time = current_time 
                            if step % 50 == 0:
                                 print(f"Time: {current_time:.1f}, Updated Durations: {[p.duration for p in program_logic.phases]}")
                except traci.exceptions.TraCIException as e:
                     # Can happen if TLS is switched by EV logic just before this runs
                     # print(f"Warning: TraCI error during adaptive logic at step {step}: {e}")
                     pass
                except Exception as e:
                     print(f"Error during adaptive traffic light control at step {step}: {e}")
                     traceback.print_exc()
            if step % 50 == 0:
                print(f"Time: {current_time:.1f}, V2I Counts: {vehicle_counts}, Congested: {congested_approaches}, EV Active: {active_ev_priority or 'None'}")
                try:
                    current_phase_idx = traci.trafficlight.getPhase(traffic_light_id)
                    logic = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id)[0]
                    print(f"  TLS Phase: {current_phase_idx}, State: {logic.phases[current_phase_idx].state}, Durations: {[p.duration for p in logic.phases]}")
                except traci.exceptions.TraCIException as e:
                    print(f"  Error getting TLS info: {e}")
            step += 1
    except traci.exceptions.FatalTraCIError as e:
        print(f"\nFatal TraCI Error during simulation: {e}")
        print("SUMO likely closed or crashed. Check console output.")
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
    except Exception as e:
         print(f"\nUnexpected Python error during simulation loop at step {step}:")
         traceback.print_exc()
    finally:
        print("Closing TraCI connection.")
        traci.close()
        print("Simulation finished.")


def analyze_tripinfo(tripinfo_file_path):
    print(f"\n--- Analyzing Trip Info ({tripinfo_file_path}) ---")
    if not os.path.exists(tripinfo_file_path):
        print(f"Error: Tripinfo file '{tripinfo_file_path}' not found. Cannot analyze results.")
        return
    if os.path.getsize(tripinfo_file_path) == 0:
        print(f"Error: Tripinfo file '{tripinfo_file_path}' is empty.")
        return
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
             print(f"Warning: Skipped {missing_attrs} trips due to missing or invalid attributes in tripinfo file.")
        if not data:
            print("No valid trip data found in the file.")
            return
        df = pd.DataFrame(data)
        completed_trips = df[df['arrival'] > 0]
        if not completed_trips.empty:
            print(f"Total Trips Recorded: {len(df)}")
            print(f"Completed Trips Analysed: {len(completed_trips)}")
            print("\nStatistics for Completed Trips:")
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