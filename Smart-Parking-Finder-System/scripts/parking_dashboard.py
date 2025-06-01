from flask import Flask, jsonify, render_template_string
import traci
import threading
import time

app = Flask(__name__)
parking_status = {}

def sumo_thread():
    traci.start(["sumo", "-c", "data/map.sumocfg"])
    while traci.simulation.getMinExpectedNumber() > 0:
        for pa in traci.parkingarea.getIDList():
            parking_status[pa] = traci.parkingarea.getVehicleCount(pa)
        traci.simulationStep()
        time.sleep(0.1)
    traci.close()

@app.route("/")
def index():
    return render_template_string("""
    <h1>Parking Dashboard</h1>
    <div id="data"></div>
    <script>
    setInterval(function() {
        fetch('/status').then(r => r.json()).then(d => {
            document.getElementById('data').innerHTML = JSON.stringify(d);
        });
    }, 1000);
    </script>
    """)

@app.route("/status")
def status():
    return jsonify(parking_status)

if __name__ == "__main__":
    t = threading.Thread(target=sumo_thread, daemon=True)
    t.start()
    app.run(debug=True)
