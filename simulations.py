"""
Nava Set vs Baseline Human Aging Simulation
Author: William Nava
Year: 2025
License: MIT

Simulates biological system health over time using:
1. Baseline decay
2. Nava Set energy distribution
3. Hostile world conditions

Requires: numpy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Create figures directory if it doesn't exist
os.makedirs("../figures", exist_ok=True)

# Constants
max_years = 500
num_subsystems = 6
death_threshold = 0.25

# Baseline decay rates for each subsystem
base_decay = np.array([0.01, 0.007, 0.006, 0.005, 0.008, 0.007])

# Nava Set modifier (slows decay)
nava_modifier = np.array([0.2, 0.3, 0.3, 0.4, 0.25, 0.3])

# External stress (used in hostile model)
def external_stress():
    return np.random.normal(0.002, 0.0015, size=num_subsystems)

# Helper function to simulate lifespan
def simulate(human_type, hostile=False):
    health = np.ones((max_years, num_subsystems))
    modifier = nava_modifier if human_type == "nava" else np.ones(num_subsystems)

    for year in range(1, max_years):
        decay = base_decay * modifier
        if hostile:
            decay += external_stress() if human_type == "baseline" else external_stress() * 0.5
        health[year] = np.clip(health[year - 1] - decay, 0, 1)

    avg_health = health.mean(axis=1)
    lifespan = np.argmax(avg_health < death_threshold)
    if lifespan == 0:
        lifespan = max_years
    return avg_health, lifespan

# Run simulations
normal_health, normal_life = simulate("baseline")
nava_health, nava_life = simulate("nava")
hostile_normal, hostile_normal_life = simulate("baseline", hostile=True)
hostile_nava, hostile_nava_life = simulate("nava", hostile=True)

# Plot 1: Normal vs Nava Set
plt.figure(figsize=(10, 6))
plt.plot(normal_health, label=f"Normal Human ({normal_life} yrs)")
plt.plot(nava_health, label=f"Nava Set Human ({nava_life} yrs)")
plt.axhline(death_threshold, color='red', linestyle='--', label='Death Threshold')
plt.title("System Health: Baseline vs Nava Set")
plt.xlabel("Age (Years)")
plt.ylabel("Average System Health")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../figures/baseline_vs_nava.png")

# Plot 2: Hostile Environment
plt.figure(figsize=(10, 6))
plt.plot(hostile_normal, label=f"Normal Human in Hostile World ({hostile_normal_life} yrs)")
plt.plot(hostile_nava, label=f"Nava Set Human in Hostile World ({hostile_nava_life} yrs)")
plt.axhline(death_threshold, color='red', linestyle='--', label='Death Threshold')
plt.title("System Health Under Environmental Stress")
plt.xlabel("Age (Years)")
plt.ylabel("Average System Health")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../figures/hostile_environment.png")

print(f"Baseline lifespan: {normal_life} years")
print(f"Nava Set lifespan: {nava_life} years")
print(f"Hostile Normal lifespan: {hostile_normal_life} years")
print(f"Hostile Nava lifespan: {hostile_nava_life} years")
