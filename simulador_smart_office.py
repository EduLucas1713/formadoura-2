"""simulador_smart_office.py
Gera o arquivo smart_office_data.csv com 7 dias de dados (15-min intervalos) para sensores de temperatura, luminosidade e ocupação.

Uso:
    python simulador_smart_office.py
"""
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def generate(start=datetime(2025,9,28,0,0,0), days=7, seed=42, out="smart_office_data.csv"):
    np.random.seed(seed)
    records = []
    sensor_id_map = {"temperature":"T-001","luminosity":"L-001","occupancy":"O-001"}
    periods = days * 24 * 4
    for i in range(periods):
        ts = start + timedelta(minutes=15*i)
        hour = ts.hour
        weekday = ts.weekday()
        day_factor = 6 * np.sin((hour / 24) * 2 * np.pi)
        temp_base = 22 + day_factor
        temperature = float(np.clip(temp_base + np.random.normal(0,0.5),16.0,30.0))
        if 6 <= hour <= 18:
            lux_base = 200 + 800 * np.sin(((hour - 6) / 12) * np.pi)
            luminosity = float(max(0, lux_base + np.random.normal(0,50)))
        else:
            luminosity = 0.0
        if weekday < 5 and 8 <= hour < 18:
            occ_prob = 0.7
        elif weekday < 5 and (7 <= hour < 8 or 18 <= hour < 20):
            occ_prob = 0.25
        else:
            occ_prob = 0.05
            if weekday >= 5 and np.random.rand() < 0.02:
                occ_prob = 0.4
        occupancy = int(np.random.rand() < occ_prob)
        records.append({"timestamp": ts.isoformat(sep=' '), "sensor_id": sensor_id_map["temperature"], "sensor_type":"temperature", "value": round(temperature,2)})
        records.append({"timestamp": ts.isoformat(sep=' '), "sensor_id": sensor_id_map["luminosity"], "sensor_type":"luminosity", "value": round(luminosity,1)})
        records.append({"timestamp": ts.isoformat(sep=' '), "sensor_id": sensor_id_map["occupancy"], "sensor_type":"occupancy", "value": occupancy})
    df = pd.DataFrame(records)
    df.to_csv(out, index=False)
    print(f"CSV gerado: {out} ({len(df)} linhas)")

if __name__ == "__main__":
    generate()
