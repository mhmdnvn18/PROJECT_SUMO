import streamlit as st
import traci
import time

SUMO_BINARY = "sumo-gui"  # Ganti ke "sumo-gui" agar GUI terbuka
SUMO_CONFIG = "random.sumocfg"

def get_parking_status():
    status = {}
    for area in traci.parkingarea.getIDList():
        occupied = traci.parkingarea.getVehicleIDs(area)
        status[area] = "Penuh" if occupied else "Kosong"
    return status

def main():
    st.title("Smart Parking Finder Dashboard")
    st.write("Status real-time area parkir dari simulasi SUMO")

    if st.button("Mulai Simulasi"):
        connected = False
        try:
            # Coba perintah TraCI sederhana untuk memeriksa koneksi
            traci.getVersion()
            connected = True
            st.text("TraCI sudah terhubung.")
        except Exception:
            st.text("TraCI tidak terhubung. Memulai TraCI...")
            traci.start([SUMO_BINARY, "-c", SUMO_CONFIG])
            connected = True
        st.text(f"Terhubung: {connected}")
        placeholder = st.empty()
        try:
            while traci.simulation.getMinExpectedNumber() > 0:
                traci.simulationStep()
                status = get_parking_status()
                with placeholder.container():
                    st.table([{"Area": k, "Status": v} for k, v in status.items()])
                time.sleep(0.5)
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            try:
                traci.close()
            except Exception:
                pass
            st.success("Simulasi selesai.")

if __name__ == "__main__":
    main()

# Pastikan import dan path file benar, serta tidak ada error runtime.
