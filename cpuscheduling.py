import matplotlib.pyplot as plt
import random
from collections import deque
import copy

class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.id = pid
        self.arrival_time = arrival
        self.burst_time = burst
        self.priority = priority

def draw_combined_gantt_chart(all_timelines):
    fig, axs = plt.subplots(len(all_timelines), 1, figsize=(12, 2 * len(all_timelines)), sharex=True)
    colors = {}
    
    for i, (title, timeline) in enumerate(all_timelines.items()):
        ax = axs[i]
        ax.set_title(f"{title} Gantt Chart")
        ax.set_ylabel("Processes")
        ax.grid(True)

        process_labels = sorted(set(label for _, _, label in timeline))
        y_ticks = []
        y_labels = []

        for j, label in enumerate(process_labels):
            y = j * 10
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
        ax.set_xlim(0, max(start + dur for start, dur, _ in timeline) + 2)

    axs[-1].set_xlabel("Time")
    plt.tight_layout()
    plt.show()

def fcfs(processes):
    time = 0
    timeline = []
    for p in sorted(processes, key=lambda x: x.arrival_time):
        if time < p.arrival_time:
            time = p.arrival_time
        start = time
        time += p.burst_time
        timeline.append((start, p.burst_time, p.id))
    return timeline

def sjf(processes):
    time = 0
    timeline = []
    ready = []
    processes.sort(key=lambda p: p.arrival_time)
    completed = []
    i = 0
    while len(completed) < len(processes):
        while i < len(processes) and processes[i].arrival_time <= time:
            ready.append(processes[i])
            i += 1
        if ready:
            ready.sort(key=lambda x: x.burst_time)
            p = ready.pop(0)
            start = time
            time += p.burst_time
            timeline.append((start, p.burst_time, p.id))
            completed.append(p)
        else:
            time += 1
    return timeline

def round_robin(processes, quantum):
    time = 0
    q = deque()
    timeline = []
    remaining = {p.id: p.burst_time for p in processes}
    arrival_map = {p.id: p.arrival_time for p in processes}
    completed = set()
    processes.sort(key=lambda p: p.arrival_time)
    i = 0
    queue_set = set()

    while len(completed) < len(processes):
        while i < len(processes) and processes[i].arrival_time <= time:
            if processes[i].id not in queue_set:
                q.append(processes[i])
                queue_set.add(processes[i].id)
            i += 1

        if q:
            p = q.popleft()
            queue_set.discard(p.id)
            exec_time = min(quantum, remaining[p.id])
            start = time
            time += exec_time
            timeline.append((start, exec_time, p.id))
            remaining[p.id] -= exec_time

            while i < len(processes) and processes[i].arrival_time <= time:
                if processes[i].id not in queue_set and processes[i].id not in completed:
                    q.append(processes[i])
                    queue_set.add(processes[i].id)
                i += 1

            if remaining[p.id] > 0:
                q.append(p)
                queue_set.add(p.id)
            else:
                completed.add(p.id)
        else:
            time += 1

    return timeline

def priority_scheduling(processes):
    time = 0
    timeline = []
    ready = []
    completed = []
    processes.sort(key=lambda p: p.arrival_time)
    i = 0

    while len(completed) < len(processes):
        while i < len(processes) and processes[i].arrival_time <= time:
            ready.append(processes[i])
            i += 1
        if ready:
            ready.sort(key=lambda x: x.priority)
            p = ready.pop(0)
            start = time
            time += p.burst_time
            timeline.append((start, p.burst_time, p.id))
            completed.append(p)
        else:
            time += 1

    return timeline

# Main function to run all and combine
def main():
    n = int(input("Enter number of processes: "))
    base_processes = []

    for _ in range(n):
        pid = input("Enter Process ID (e.g., P1): ")
        arrival = int(input(f"Arrival Time for {pid}: "))
        burst = int(input(f"Burst Time for {pid}: "))
        priority = int(input(f"Priority for {pid} (lower = higher): "))
        base_processes.append(Process(pid, arrival, burst, priority))

    quantum = int(input("Enter Time Quantum for Round Robin: "))

    all_timelines = {
        "FCFS": fcfs(copy.deepcopy(base_processes)),
        "SJF": sjf(copy.deepcopy(base_processes)),
        "Round Robin": round_robin(copy.deepcopy(base_processes), quantum),
        "Priority": priority_scheduling(copy.deepcopy(base_processes))
    }

    draw_combined_gantt_chart(all_timelines)

if __name__ == "__main__":
    main()
# Energy-Efficient CPU Scheduling Algorithm
