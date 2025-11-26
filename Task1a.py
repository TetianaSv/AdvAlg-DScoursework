"""
TASK 1b – Empirical Measurement and Application
(Reuses code from Task 1a)
------------------------------------------------------------
This version keeps the same build_station_table() and
check_station_status() functions from 1a, but adds:

1. Empirical performance measurement
2. Plotting of average lookup time vs dataset size n
3. Application using real London Underground data
------------------------------------------------------------
"""

import random
import time
import matplotlib.pyplot as plt
import pandas as pd
from chained_hashtable import ChainedHashTable
from hash_functions import hashpjw

# ------------------------------------------------------------
# Reuse functions from Task 1a
# ------------------------------------------------------------
def build_station_table(stations, m=10):
    table = ChainedHashTable(m=m, hash_func=hashpjw)
    for station in stations:
        table.insert(station)
    return table

def check_station_status(table, name):
    return "Operational" if table.search(name) else "Non-operational"

# ------------------------------------------------------------
# Part 1 – Empirical Performance Measurement
# ------------------------------------------------------------
def measure_lookup_time(n: int, num_queries: int = 1000) -> float:
    """Builds a ChainedHashTable of n stations and times lookup operations."""
    stations = [f"Station_{i}" for i in range(n)]
    table = build_station_table(stations, m=n * 2)  # larger table to reduce collisions

    queries = random.sample(stations, num_queries)
    start = time.time()
    for q in queries:
        _ = table.search(q)
    end = time.time()
    avg_time = (end - start) / num_queries
    return avg_time

sizes = [1000, 5000, 10000, 25000, 50000]
avg_times = []

print("Empirical performance test (Task 1b)\n")
for n in sizes:
    t = measure_lookup_time(n)
    avg_times.append(t)
    print(f"n = {n:<6} | Avg lookup time = {t:.8f} seconds")

# ------------------------------------------------------------
# Part 2 – Plot Results
# ------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(sizes, avg_times, marker='o', color='blue')
plt.title("Average Lookup Time vs Dataset Size n")
plt.xlabel("Number of Stations (n)")
plt.ylabel("Average Lookup Time (seconds)")
plt.grid(True)
plt.tight_layout()
plt.show()

print("\nTheoretical complexity: O(1) average lookup time.")
print("Small variations are expected due to system and Python overhead.\n")

# ------------------------------------------------------------
# Part 3 – Application with Real London Underground Data
# ------------------------------------------------------------
excel_file = "London Underground data.xlsx"
df = pd.read_excel(excel_file, header=None)
df.columns = ["StationA", "StationB", "Time"]

# Combine both columns into one set of unique station names
stations_real = set(df["StationA"]).union(set(df["StationB"]))
table_real = build_station_table(stations_real, m=len(stations_real) * 2)

print(f"Total unique stations loaded from Excel: {len(stations_real)}\n")

# ------------------------------------------------------------
# Part 4 – Demonstration of Status Checks (for screenshots)
# ------------------------------------------------------------
def test_real_stations():
    tests = ["Victoria", "Paddington", "Paddinton"]  # misspelled last one
    for name in tests:
        status = check_station_status(table_real, name)
        print(f"{name}: {status}")

print("--- London Underground Operational Status Check ---")
test_real_stations()

