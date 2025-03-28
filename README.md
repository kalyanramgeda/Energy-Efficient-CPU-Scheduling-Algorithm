# 🧠 CPU Scheduling Algorithms with Gantt Chart Visualization

This Python project implements four classic **CPU Scheduling Algorithms**:
- First-Come, First-Served (FCFS)
- Shortest Job First (SJF)
- Round Robin (RR)
- Priority Scheduling

The results are visualized as **Gantt Charts** using `matplotlib`, making it easy to compare how different algorithms schedule processes over time.

---

## 📌 Features

- Simulates scheduling of user-defined processes with custom arrival time, burst time, and priority.
- Visualizes process execution order in colorful Gantt charts for all 4 algorithms.
- Supports **time quantum** input for Round Robin scheduling.
- Uses deep copies to avoid mutation issues between algorithm runs.
- Random color assignment for easy visual distinction of processes.

---

## 🚀 How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/cpu-scheduling-visualizer.git
   cd cpu-scheduling-visualizer
