import streamlit as st
import traci
import time
import folium
from streamlit_folium import folium_static
import sqlite3
from datetime import datetime
import pandas as pd
import logging
import traceback

SUMO_BINARY = "sumo-gui"
SUMO_CONFIG = "random.sumocfg"
logging.basicConfig(filename='parking_system.log', level=logging.ERROR)

def get_db_connection():
    return sqlite3.connect('parking.db', check_same_thread=False)

def init_database():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS parking_log(
            id INTEGER PRIMARY KEY,
            area TEXT, 
            status TEXT, 
            time TEXT,
            sim_time REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS reservation(
            id INTEGER PRIMARY KEY,
            area TEXT, 
            user_id TEXT, 
            time TEXT,
            status TEXT DEFAULT 'active'
        )
    ''')
    conn.commit()
    conn.close()

def get_coords(area):
    try:
        pos = traci.parkingarea.getStartPos(area)
        return [pos[1], pos[0]]  # [lat, lon]
    except Exception as e:
        logging.error(f"Coordinate error for {area}: {e}")
        return [-6.2, 106.8]

def get_parking_status():
    status = {}
    for area in traci.parkingarea.getIDList():
        try:
            if area in st.session_state.get('reservations', {}):
                status[area] = "Direservasi"
            elif traci.parkingarea.getVehicleCount(area) > 0:
                status[area] = "Penuh"
            else:
                status[area] = "Kosong"
        except Exception as e:
            logging.error(f"Status error for {area}: {e}")
            status[area] = "Error"
    return status

def start_simulation():
    try:
        try:
            traci.getVersion()
            st.info("Simulasi sudah berjalan")
            return
        except:
            pass
        traci.start([SUMO_BINARY, "-c", SUMO_CONFIG])
        st.session_state.simulation_running = True
        st.session_state.traci_connected = True
        st.toast("Simulasi SUMO berhasil dimulai!", icon="✅")
    except Exception as e:
        st.error(f"Gagal memulai simulasi: {e}")

def stop_simulation():
    try:
        traci.close()
        st.session_state.simulation_running = False
        st.toast("Simulasi dihentikan", icon="⏹️")
    except Exception as e:
        st.warning(f"Error saat menghentikan: {e}")

def run_simulation(sim_speed):
    try:
        while st.session_state.simulation_running:
            if traci.simulation.getMinExpectedNumber() <= 0:
                st.toast("Simulasi selesai secara alami", icon="🏁")
                st.session_state.simulation_running = False
                break
            try:
                traci.simulationStep()
            except traci.exceptions.FatalTraCIError as e:
                st.error(f"Koneksi TraCI terputus: {e}")
                st.session_state.simulation_running = False
                return
            status = get_parking_status()
            sim_time = traci.simulation.getTime()
            conn = get_db_connection()
            c = conn.cursor()
            for area, stat in status.items():
                c.execute('''
                    INSERT INTO parking_log (area, status, time, sim_time) 
                    VALUES (?,?,?,?)
                ''', (area, stat, datetime.now().isoformat(), sim_time))
            conn.commit()
            conn.close()
            st.session_state.parking_status = status
            yield status
            time.sleep(0.5 / sim_speed)
    except Exception as e:
        st.error(f"Error simulasi: {e}")
        logging.error(f"Simulation error: {e}\n{traceback.format_exc()}")
    finally:
        st.session_state.simulation_running = False

def show_parking_map(status):
    try:
        first_coords = get_coords(next(iter(status.keys())))
        m = folium.Map(location=first_coords, zoom_start=15)
        for area, stat in status.items():
            color = "green" if stat == "Kosong" else "red" if stat == "Penuh" else "blue"
            icon = "car" if stat == "Kosong" else "ban" if stat == "Penuh" else "flag"
            folium.Marker(
                location=get_coords(area),
                popup=f"{area}: {stat}",
                tooltip=f"Klik untuk detail",
                icon=folium.Icon(color=color, icon=icon, prefix='fa')
            ).add_to(m)
        folium_static(m, width=700, height=400)
    except Exception as e:
        st.error(f"Map error: {e}")

def show_occupancy_trend_chart():
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM parking_log", conn)
        conn.close()
        if df.empty:
            st.info("Belum ada data historis.")
            return
        df['sim_time'] = df['sim_time'].astype(float)
        df['occupied'] = (df['status'] == "Penuh").astype(int)
        df['time_bin'] = pd.cut(df['sim_time'], bins=20)
        df_agg = df.groupby(['area', 'time_bin'])['occupied'].mean().reset_index()
        import plotly.express as px
        fig = px.line(df_agg, x="time_bin", y="occupied", color="area", 
                     title="Tren Okupansi Parkir", labels={'occupied': 'Persentase Terisi'})
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Analytics error: {e}")

def make_reservation(area, user_id):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO reservation (area, user_id, time) 
            VALUES (?,?,?)
        ''', (area, user_id, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        if 'reservations' not in st.session_state:
            st.session_state.reservations = {}
        st.session_state.reservations[area] = {
            'user_id': user_id,
            'time': datetime.now()
        }
        try:
            traci.parkingarea.setReservation(area, vehicleID=user_id)
        except AttributeError:
            pass
        return True
    except Exception as e:
        logging.error(f"Reservation error: {e}\n{traceback.format_exc()}")
        return False

def show_driver_interface(user_id):
    st.header("🔍 Cari & Reservasi Parkir")
    if 'parking_status' in st.session_state and st.session_state.parking_status:
        status = st.session_state.parking_status
        available = [a for a, s in status.items() if s == "Kosong"]
        if available:
            selected = st.selectbox("Pilih Area Parkir", available)
            coords = get_coords(selected)
            st.map(pd.DataFrame({'lat': [coords[0]], 'lon': [coords[1]]}), zoom=15)
            if st.button("🚘 Reservasi Sekarang"):
                if make_reservation(selected, user_id):
                    st.success(f"Berhasil reservasi {selected}!")
                else:
                    st.error("Gagal melakukan reservasi")
            st.link_button("🧭 Navigasi ke Lokasi", 
                          f"https://www.google.com/maps/dir/?api=1&destination={coords[0]},{coords[1]}")
        else:
            st.warning("Tidak ada area parkir yang tersedia saat ini")
    else:
        st.info("Mulai simulasi untuk melihat ketersediaan parkir")

def show_operator_interface():
    st.header("📋 Manajemen Parkir")
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM reservation ORDER BY time DESC LIMIT 10", conn)
        conn.close()
        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("Belum ada data reservasi")
    except Exception as e:
        st.error(f"Database error: {e}")

def show_government_interface():
    st.header("📈 Analisis Dampak Sistem")
    show_occupancy_trend_chart()
    st.subheader("Statistik Penggunaan")
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT area, status, COUNT(*) as count FROM parking_log GROUP BY area, status", conn)
        conn.close()
        if not df.empty:
            import plotly.express as px
            fig = px.bar(df, x="area", y="count", color="status", barmode="group")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Belum ada data statistik")
    except Exception as e:
        st.error(f"Statistik error: {e}")

def main():
    init_database()
    session_defaults = {
        'simulation_running': False,
        'reservations': {},
        'parking_status': {},
        'traci_connected': False
    }
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    st.title("🚗 Smart Parking Finder Dashboard")
    st.write("Sistem real-time pencarian parkir berbasis AIoT")

    with st.sidebar:
        st.header("Konfigurasi Sistem")
        user_type = st.selectbox("Peran Pengguna", ["Pengendara", "Operator Parkir", "Pemerintah"])
        user_id = st.text_input("ID Pengguna", value="user_123")
        st.header("Kontrol Simulasi")
        sim_speed = st.slider("Kecepatan Simulasi", 0.1, 2.0, 0.5, step=0.1)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Mulai Simulasi", 
                         disabled=st.session_state.simulation_running,
                         use_container_width=True):
                start_simulation()
        with col2:
            if st.button("⏹️ Hentikan Simulasi", 
                         disabled=not st.session_state.simulation_running,
                         use_container_width=True):
                stop_simulation()

    if st.session_state.simulation_running:
        try:
            status_container = st.empty()
            map_container = st.empty()
            for _ in run_simulation(sim_speed):
                status = st.session_state.parking_status
                with status_container.container():
                    st.subheader("📊 Status Parkir Real-time")
                    cols = st.columns(min(4, len(status)))
                    for i, (area, stat) in enumerate(status.items()):
                        with cols[i % len(cols)]:
                            st.metric(
                                label=area, 
                                value=stat,
                                help=f"Status terkini: {stat}"
                            )
                    try:
                        current_time = traci.simulation.getTime()
                        end_time = traci.simulation.getEndTime() or 3600
                        progress = current_time / end_time
                        st.progress(min(progress, 1.0), text=f"Progress: {progress*100:.1f}%")
                    except:
                        st.progress(0)
                with map_container:
                    show_parking_map(status)
        except Exception as e:
            st.error(f"Error: {e}")

    if user_type == "Pengendara":
        show_driver_interface(user_id)
    elif user_type == "Operator Parkir":
        show_operator_interface()
    elif user_type == "Pemerintah":
        show_government_interface()

if __name__ == "__main__":
    main()
