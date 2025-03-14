#include <iostream>
#include <vector>
using namespace std;

class Task {
public:
    int id, workload, frequency;
    Task(int id, int workload) : id(id), workload(workload), frequency(1000) {}

    void adjustFrequency() {
        if (workload > 50) frequency = 2000;
        else if (workload > 20) frequency = 1500;
        else frequency = 1000;
    }

    void execute() {
        adjustFrequency();
        cout << "Task " << id << " executing at " << frequency << " MHz\n";
    }
};

int main() {
    vector<Task> tasks = { {1, 30}, {2, 60}, {3, 15} };
    for (auto &task : tasks) task.execute();
    return 0;
}
