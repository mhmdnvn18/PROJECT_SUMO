import xml.etree.ElementTree as ET
import pandas as pd

tripinfo_path = "data/tripinfo.xml"

def analyze_tripinfo():
    tree = ET.parse(tripinfo_path)
    root = tree.getroot()
    trips = root.findall("tripinfo")
    data = []
    for trip in trips:
        data.append(trip.attrib)
    if data:
        df = pd.DataFrame(data)
        print(df.describe(include='all'))
    else:
        print("Tidak ada data tripinfo.")

if __name__ == "__main__":
    analyze_tripinfo()
