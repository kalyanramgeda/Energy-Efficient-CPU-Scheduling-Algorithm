#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>

using namespace std;

// Structure to represent a Process
struct Process {
    int id, burstTime, arrivalTime, priority;
};

// Function for First Come First Serve (FCFS)
void fcfs(vector<Process> &processes) {
    int n = processes.size();
    int waitingTime = 0, turnaroundTime = 0, completionTime = 0;

    cout << "\nFCFS Scheduling:\n";
    cout << "Process\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\n";

    for (int i = 0; i < n; i++) {
        if (i == 0)
            completionTime = processes[i].arrivalTime + processes[i].burstTime;
        else
            completionTime += processes[i].burstTime;

        waitingTime = completionTime - processes[i].arrivalTime - processes[i].burstTime;
        turnaroundTime = completionTime - processes[i].arrivalTime;

        cout << processes[i].id << "\t" << processes[i].arrivalTime << "\t\t" 
             << processes[i].burstTime << "\t\t" << max(0, waitingTime) << "\t\t" 
             << turnaroundTime << endl;
    }
}

// Function for Shortest Job First (SJF)
void sjf(vector<Process> &processes) {
    sort(processes.begin(), processes.end(), [](Process a, Process b) {
        return a.burstTime < b.burstTime;
    });

    fcfs(processes); // After sorting by burst time, FCFS logic applies
}

// Function for Round Robin (RR)
void roundRobin(vector<Process> &processes, int quantum) {
    queue<Process> q;
    for (auto &p : processes) q.push(p);

    int time = 0;
    cout << "\nRound Robin Scheduling (Quantum = " << quantum << "):\n";
    cout << "Process\tBurst Time\tWaiting Time\tTurnaround Time\n";

    while (!q.empty()) {
        Process p = q.front(); q.pop();
        int executeTime = min(quantum, p.burstTime);
        time += executeTime;
        p.burstTime -= executeTime;

        if (p.burstTime > 0)
            q.push(p);
        else
            cout << p.id << "\t" << p.burstTime + executeTime << "\t\t" << time - executeTime << "\t\t" << time << endl;
    }
}

// Function for Priority Scheduling
void priorityScheduling(vector<Process> &processes) {
    sort(processes.begin(), processes.end(), [](Process a, Process b) {
        return a.priority < b.priority;
    });

    fcfs(processes); // After sorting by priority, FCFS logic applies
}

int main() {
    int n, choice, quantum;
    
    cout << "Enter number of processes: ";
    cin >> n;

    vector<Process> processes(n);
    for (int i = 0; i < n; i++) {
        cout << "Enter Process ID, Arrival Time, Burst Time, Priority: ";
        cin >> processes[i].id >> processes[i].arrivalTime >> processes[i].burstTime >> processes[i].priority;
    }

    cout << "\nSelect Scheduling Algorithm:\n";
    cout << "1 - FCFS\n2 - SJF\n3 - Round Robin\n4 - Priority Scheduling\n";
    cout << "Enter your choice: ";
    cin >> choice;

    switch (choice) {
        case 1: fcfs(processes); break;
        case 2: sjf(processes); break;
        case 3: 
            cout << "Enter time quantum: ";
            cin >> quantum;
            roundRobin(processes, quantum);
            break;
        case 4: priorityScheduling(processes); break;
        default: cout << "Invalid choice!\n";
    }

    return 0;
}
