import tkinter as tk
from tkinter import scrolledtext
import heapq
import math

class Task:
    def __init__(self, name, execution_time, deadline, period):
        self.name = name
        self.execution_time = execution_time
        self.deadline = deadline
        self.period = period
        self.remaining_execution_time = execution_time
        self.wait_time = 0
        self.response_time = None

    def __lt__(self, other):
        priority_self = self.deadline - self.remaining_execution_time
        priority_other = other.deadline - other.remaining_execution_time
        if priority_self == priority_other:
            return self.deadline < other.deadline
        return priority_self < priority_other

def lcm(numbers):
    lcm = numbers[0]
    for i in numbers[1:]:
        lcm = lcm * i // math.gcd(lcm, i)
    return lcm

class Main:
    def __init__(self):
        self.outputArea = None

    def main(self):
        self.setupGUI()

    def setupGUI(self):
        root = tk.Tk()
        root.title("Least Slack Scheduling Simulation")

        outputFrame = tk.Frame(root)
        outputFrame.pack(fill=tk.BOTH, expand=True)

        self.outputArea = scrolledtext.ScrolledText(outputFrame, width=70, height=30)
        self.outputArea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.outputArea.configure(state="disabled")

        simulateButton = tk.Button(root, text="Simulate", command=self.simulate)
        simulateButton.pack(side=tk.BOTTOM)

        authorLabel = tk.Label(root, text="Feras Al-khuzai")
        copyrightLabel = tk.Label(root, text="©")

        authorLabel.pack(side=tk.LEFT)
        tk.Label(root, text=" | ").pack(side=tk.LEFT)
  
        copyrightLabel.pack(side=tk.LEFT)

        root.mainloop()

    def appendOutput(self, message):
        self.outputArea.configure(state="normal")
        self.outputArea.insert(tk.END, message + "\n")
        self.outputArea.configure(state="disabled")
        self.outputArea.see(tk.END)

    def simulate(self):
        tasks = [
            Task("Task 1", 1, 7, 9),
            Task("Task 2", 2, 9, 16),
            Task("Task 3", 6, 8, 14),
          
        ]

        pq = []
        heapq.heapify(pq)

        lcm_period = max(task.period for task in tasks)
        print(lcm_period)
        total_wait_time = 0
        total_response_time = 0
        total_execution_time = 0

        current_time = 0
        while current_time < lcm_period:
            new_arrivals = [task for task in tasks if task.period == 0 or (current_time % task.period) == 0]
            for task in new_arrivals:
                task.remaining_execution_time = task.execution_time
                task.wait_time = 0
                task.response_time = None
                heapq.heappush(pq, task)

            if pq:
                current_task = heapq.heappop(pq)
                self.appendOutput(f"At time {current_time}: Executing {current_task.name}")
                if current_task.response_time is None:
                    current_task.response_time = current_time
                    total_response_time += current_task.response_time
                current_task.remaining_execution_time -= 1
                total_execution_time += 1
                if current_task.remaining_execution_time > 0:
                    heapq.heappush(pq, current_task)
                else:
                    self.appendOutput(f"At time {current_time + 1}: Finished executing {current_task.name}")
                    total_wait_time += current_task.wait_time
            else:
                self.appendOutput(f"At time {current_time}: Idle")

            for task in pq:
                task.wait_time += 1

            current_time += 1

        self.appendOutput("Simulation completed.")

        avg_wait_time = total_wait_time / len(tasks)
        avg_response_time = total_response_time / len(tasks)
        cpu_utilization = total_execution_time / current_time

        self.appendOutput(f"Average waiting time: {avg_wait_time}")
        self.appendOutput(f"Average response time: {avg_response_time}")
        self.appendOutput(f"CPU Utilization: {cpu_utilization}")
        self.appendOutput("                                    ")
        
        self.appendOutput("Simulation completed.")
        self.appendOutput("                                    ")
if __name__ == "__main__":
    app = Main()
    app.main()
