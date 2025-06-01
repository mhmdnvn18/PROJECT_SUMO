import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import os

def parse_tripinfo(file):
    if not os.path.exists(file):
        print(f"❌ File {file} tidak ditemukan.")
        return [], []
    tree = ET.parse(file)
    root = tree.getroot()

    durations = []
    waitings = []

    for trip in root.findall('tripinfo'):
        durations.append(float(trip.get('duration')))
        waitings.append(float(trip.get('waitingTime')))

    return durations, waitings

def main():
    print("Pilih file tripinfo yang ingin dianalisis:")
    print("1. tripinfo_adaptive.xml (lampu adaptif)")
    print("2. tripinfo_control.xml (kontrol manual/otomatis)")
    print("3. tripinfo_qlearning.xml (Q-Learning)")
    pilihan = input("Masukkan nomor [1/2/3] (default 1): ").strip()
    if pilihan == "2":
        file = "tripinfo_control.xml"
    elif pilihan == "3":
        file = "tripinfo_qlearning.xml"
    else:
        file = "tripinfo_adaptive.xml"
    durations, waitings = parse_tripinfo(file)

    if not durations:
        print("❌ Tidak ada data dalam tripinfo.xml")
        return

    avg_duration = sum(durations) / len(durations)
    avg_waiting = sum(waitings) / len(waitings)

    print(f"✅ Rata-rata waktu tempuh: {avg_duration:.2f} detik")
    print(f"✅ Rata-rata waktu tunggu: {avg_waiting:.2f} detik")

    # Visualisasi
    labels = ['Rata-rata Waktu Tempuh', 'Rata-rata Waktu Tunggu']
    values = [avg_duration, avg_waiting]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=['skyblue', 'salmon'])
    plt.title("Statistik Hasil Simulasi")
    plt.ylabel("Detik")
    plt.tight_layout()
    os.makedirs("images", exist_ok=True)
    plt.savefig("images/hasil_simulasi.png")
    plt.show()

if __name__ == "__main__":
    main()
