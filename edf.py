import tkinter as tk
from tkinter import scrolledtext 
from heapq import heappush, heappop

class Task:
    def __init__(self, name, executionTime, deadline, period):
        self.name = name
        self.executionTime = executionTime
        self.deadline = deadline
        self.period = period
        self.arrivalTime = 0
        self.responseTime = -1

    def __lt__(self, other):
        return self.deadline < other.deadline

    def __str__(self):
        return self.name

class Main:
    def __init__(self):
        self.outputArea = None

    def main(self):
        self.setupGUI()

    def setupGUI(self):
        root = tk.Tk()
        root.title("EDF Scheduling Simulation")

        outputFrame = tk.Frame(root)
        outputFrame.pack(fill=tk.BOTH, expand=True)

        self.outputArea = scrolledtext.ScrolledText(outputFrame, width=70, height=30)
        self.outputArea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.outputArea.configure(state="disabled")

        simulateButton = tk.Button(root, text="Simulate", command=self.simulateEDF)
        simulateButton.pack(side=tk.BOTTOM)

        authorLabel = tk.Label(root, text="Feras Al-khuzai")
        copyrightLabel = tk.Label(root, text="©")

        authorLabel.pack(side=tk.LEFT)
        tk.Label(root, text=" | ").pack(side=tk.LEFT)
        tk.Label(root, text=" | ").pack(side=tk.LEFT)
        copyrightLabel.pack(side=tk.LEFT)

        root.mainloop()

    def simulateEDF(self):
        tasks = [
            Task("Task 1", 1, 7, 9),
            Task("Task 2", 2, 9, 16),
            Task("Task 3", 6, 8, 14),
            
        ]
      

        taskQueue = []
        for task in tasks:
            heappush(taskQueue, (task.arrivalTime + task.deadline, task))
        currentTime = 0
        simulationTime = max(task.period for task in tasks)
        
        totalWaitingTime = 0
        totalResponseTime = 0
        cpuIdleTime = 0

        while currentTime < simulationTime:
            
            if not taskQueue:
                self.appendOutput("CPU is idle at time " + str(currentTime))
                currentTime += 1
                cpuIdleTime += 1
                continue

            _, task = heappop(taskQueue)
            if task.arrivalTime > currentTime:
                cpuIdleTime += task.arrivalTime - currentTime
                currentTime = task.arrivalTime

            totalWaitingTime += currentTime - task.arrivalTime
            if task.responseTime == -1:
                task.responseTime = currentTime - task.arrivalTime
                totalResponseTime += task.responseTime
            self.appendOutput("At time " + str(currentTime) + ": Processing " + str(task))
            currentTime += task.executionTime
            self.appendOutput("At time " + str(currentTime) + ": Finished processing " + str(task))

            task.arrivalTime += task.period
            task.deadline = task.arrivalTime + task.period
            heappush(taskQueue, (task.deadline, task))

        averageWaitingTime = totalWaitingTime / len(tasks)
        averageResponseTime = totalResponseTime / len(tasks)
        cpuUtilization = (currentTime - cpuIdleTime) / currentTime

        self.appendOutput("-----------------------------------------------")
        self.appendOutput("Average waiting time: " + str(averageWaitingTime))
        self.appendOutput("Average response time: " + str(averageResponseTime))
        self.appendOutput("CPU Utilization: " + str(cpuUtilization))
        self.appendOutput("LCM : " + str(simulationTime))

        self.appendOutput("                                    ")
        
        self.appendOutput("Simulation completed.")
        self.appendOutput("                                    ")
    def appendOutput(self, message):
        self.outputArea.configure(state="normal")
        self.outputArea.insert(tk.END, message + "\n")
        self.outputArea.configure(state="disabled")
        self.outputArea.see(tk.END)


if __name__ == "__main__":
    app = Main()
    app.main()

    
