import xml.etree.ElementTree as ET

tree = ET.parse('tripinfo.xml')
root = tree.getroot()

durations, waits = [], []
for trip in root.findall('tripinfo'):
    durations.append(float(trip.get('duration')))
    waits.append(float(trip.get('waitingTime')))

if durations:
    avg_duration = sum(durations) / len(durations)
    avg_wait = sum(waits) / len(waits)
    print(f"Rata-rata waktu tempuh: {avg_duration:.2f}s")
    print(f"Rata-rata waktu tunggu: {avg_wait:.2f}s")
else:
    print("Tidak ada data tripinfo ditemukan.")
