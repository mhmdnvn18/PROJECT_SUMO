# SUMO Vehicle Color Changing Simulation

This project demonstrates how to change and animate vehicle colors in SUMO (Simulation of Urban MObility) traffic simulation.

## Prerequisites

Before you start, make sure you have:

1. SUMO (Simulation of Urban MObility) installed - [Download SUMO](https://www.eclipse.org/sumo/)
2. Python 3.x installed
3. TraCI Python package (comes with SUMO installation)

## Setup

1. Ensure the SUMO_HOME environment variable is set:

   - **Windows**:
     ```cmd
     set SUMO_HOME=C:\path\to\sumo
     ```
   
   - **Linux/macOS**:
     ```bash
     export SUMO_HOME=/path/to/sumo
     ```

2. Verify all required files are in the directory:
   - `map.sumocfg` - Simulation configuration
   - `map.rou.xml` - Route definition with vehicle types
   - `map.poly.xml` - Polygons for visualization
   - `test.net.xml` - Road network file
   - `change_vehicle_colors.py` - Python script for dynamic color changes

## Running the Simulation

### Option 1: Static Colors

To run the simulation with static vehicle colors (defined in map.rou.xml):

1. Open SUMO-GUI:
   ```
   sumo-gui -c map.sumocfg
   ```

2. In the SUMO-GUI, click on the "View Settings" button (color wheel icon)
3. Go to "Vehicles" in the left panel
4. Under "Color", select "given/assigned vehicle color"
5. Start the simulation by clicking the Play button

### Option 2: Dynamic Color Changes

To run the simulation with dynamically changing vehicle colors:

1. Execute the Python script:
   ```
   python change_vehicle_colors.py
   ```

2. The script will:
   - Start SUMO-GUI with the proper configuration
   - Randomly assign colors to 30% of new vehicles
   - Change colors of 20% of vehicles every 100 simulation steps

## Understanding the Color Changing Logic

The color changing script (`change_vehicle_colors.py`) implements the following behaviors:

- For new vehicles entering the simulation:
  - 30% chance to assign a random color
  - 70% chance to keep the original color defined in the route file

- Every 100 simulation steps:
  - 20% of vehicles will get a new random color
  - 80% of vehicles remain unchanged

## Customizing the Behavior

You can modify the following parameters in `change_vehicle_colors.py`:

- `color_change_interval` - How frequently (in simulation steps) to change colors
- Color selection probability (0.3 and 0.2 values in the code)
- The `get_random_color()` function to use different color schemes

## Vehicle Types

The route file (`map.rou.xml`) defines several vehicle types with different colors:

- Regular cars with various colors (red, green, blue, yellow, cyan, magenta)
- Buses (green)
- Trucks (blue)
- Motorcycles (red)

Each vehicle type has different characteristics such as acceleration, deceleration, length, and maximum speed.

## Troubleshooting

- If you see an error about SUMO_HOME not being set, make sure to set this environment variable correctly.
- If vehicles don't change color, verify you're using the TraCI script and not just opening the simulation directly.
- For visualization issues, check the SUMO-GUI settings to ensure "given/assigned vehicle color" is selected.

## Additional Resources

- [SUMO Documentation](https://sumo.dlr.de/docs/)
- [TraCI Documentation](https://sumo.dlr.de/docs/TraCI.html)
- [Vehicle Type Parameters](https://sumo.dlr.de/docs/Definition_of_Vehicles,_Vehicle_Types,_and_Routes.html)
