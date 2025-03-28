import matplotlib.pyplot as plt
import random
from collections import deque
import copy

# Process class to store details about each process
class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.id = pid                 # Process ID (e.g., "P1")
        self.arrival_time = arrival  # Time at which process arrives
        self.burst_time = burst      # Time required to complete the process
        self.priority = priority     # Priority of the process (lower number = higher priority)

# Function to draw combined Gantt chart for all scheduling algorithms
def draw_combined_gantt_chart(all_timelines):
    fig, axs = plt.subplots(len(all_timelines), 1, figsize=(12, 2 * len(all_timelines)), sharex=True)
    colors = {}  # Dictionary to store unique colors for each process
    
    for i, (title, timeline) in enumerate(all_timelines.items()):
        ax = axs[i]
        ax.set_title(f"{title} Gantt Chart")
        ax.set_ylabel("Processes")
        ax.grid(True)

        process_labels = sorted(set(label for _, _, label in timeline))  # Unique process labels
        y_ticks = []
        y_labels = []

        # Draw each process as a colored bar in the timeline
        for j, label in enumerate(process_labels):
            y = j * 10  # Vertical position
            y_ticks.append(y + 5)
            y_labels.append(label)
            for start, duration, lbl in timeline:
                if lbl == label:
                    if lbl not in colors:
                        colors[lbl] = "#%06x" % random.randint(0, 0xFFFFFF)
                    ax.broken_barh([(start, duration)], (y, 9), facecolors=colors[lbl])
                    ax.text(start + duration / 2, y + 4.5, lbl, ha='center', va='center', color='white', fontsize=8)

        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        ax.set_ylim(0, len(process_labels) * 10)
        ax.set_xlim(0, max(start + dur for start, dur, _ in timeline) + 2)  # Auto-adjust x-axis

    axs[-1].set_xlabel("Time")  # Label x-axis at the bottom
    plt.tight_layout()
    plt.show()

# First Come First Serve Scheduling
def fcfs(processes):
    time = 0
    timeline = []
    # Sort by arrival time
    for p in sorted(processes, key=lambda x: x.arrival_time):
        if time < p.arrival_time:
            time = p.arrival_time  # CPU is idle till process arrives
        start = time
        time += p.burst_time
        timeline.append((start, p.burst_time, p.id))  # Log start, duration, and process ID
    return timeline

# Shortest Job First (Non-preemptive)
def sjf(processes):
    time = 0
    timeline = []
    ready = []
    processes.sort(key=lambda p: p.arrival_time)
    completed = []
    i = 0

    while len(completed) < len(processes):
        # Move all processes that have arrived into the ready queue
        while i < len(processes) and processes[i].arrival_time <= time:
            ready.append(processes[i])
            i += 1
        if ready:
            ready.sort(key=lambda x: x.burst_time)  # Pick shortest job
            p = ready.pop(0)
            start = time
            time += p.burst_time
            timeline.append((start, p.burst_time, p.id))
            completed.append(p)
        else:
            time += 1  # No ready process, CPU idle
    return timeline

# Round Robin Scheduling
def round_robin(processes, quantum):
    time = 0
    q = deque()
    timeline = []
    remaining = {p.id: p.burst_time for p in processes}  # Track remaining burst time
    arrival_map = {p.id: p.arrival_time for p in processes}
    completed = set()
    processes.sort(key=lambda p: p.arrival_time)
    i = 0
    queue_set = set()

    while len(completed) < len(processes):
        # Enqueue new processes that have arrived
        while i < len(processes) and processes[i].arrival_time <= time:
            if processes[i].id not in queue_set:
                q.append(processes[i])
                queue_set.add(processes[i].id)
            i += 1

        if q:
            p = q.popleft()
            queue_set.discard(p.id)
            exec_time = min(quantum, remaining[p.id])  # Execute for min(quantum, remaining)
            start = time
            time += exec_time
            timeline.append((start, exec_time, p.id))
            remaining[p.id] -= exec_time

            # Check if any new process has arrived during the current execution
            while i < len(processes) and processes[i].arrival_time <= time:
                if processes[i].id not in queue_set and processes[i].id not in completed:
                    q.append(processes[i])
                    queue_set.add(processes[i].id)
                i += 1

            # Requeue the process if it's not yet completed
            if remaining[p.id] > 0:
                q.append(p)
                queue_set.add(p.id)
            else:
                completed.add(p.id)
        else:
            time += 1  # CPU is idle

    return timeline

# Priority Scheduling (Non-preemptive)
def priority_scheduling(processes):
    time = 0
    timeline = []
    ready = []
    completed = []
    processes.sort(key=lambda p: p.arrival_time)
    i = 0

    while len(completed) < len(processes):
        # Add processes to ready queue that have arrived
        while i < len(processes) and processes[i].arrival_time <= time:
            ready.append(processes[i])
            i += 1
        if ready:
            ready.sort(key=lambda x: x.priority)  # Select highest priority (lowest number)
            p = ready.pop(0)
            start = time
            time += p.burst_time
            timeline.append((start, p.burst_time, p.id))
            completed.append(p)
        else:
            time += 1  # Idle time

    return timeline

# Main function to input process data and run all algorithms
def main():
    n = int(input("Enter number of processes: "))
    base_processes = []

    # Collect process details
    for _ in range(n):
        pid = input("Enter Process ID (e.g., P1): ")
        arrival = int(input(f"Arrival Time for {pid}: "))
        burst = int(input(f"Burst Time for {pid}: "))
        priority = int(input(f"Priority for {pid} (lower = higher): "))
        base_processes.append(Process(pid, arrival, burst, priority))

    quantum = int(input("Enter Time Quantum for Round Robin: "))

    # Run all scheduling algorithms on copies of the original process list
    all_timelines = {
        "FCFS": fcfs(copy.deepcopy(base_processes)),
        "SJF": sjf(copy.deepcopy(base_processes)),
        "Round Robin": round_robin(copy.deepcopy(base_processes), quantum),
        "Priority": priority_scheduling(copy.deepcopy(base_processes))
    }

    # Draw all Gantt charts in one figure
    draw_combined_gantt_chart(all_timelines)

# Entry point
if __name__ == "__main__":
    main()
