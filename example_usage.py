"""Example usage for Distributed Deadlock Wait-For-Graph Detector."""
from client import DeadlockWaitForGraphDetector

if __name__ == "__main__":
    edges = [
        {"from": "T1", "to": "T2", "cost": 100},
        {"from": "T2", "to": "T3", "cost": 20},
        {"from": "T3", "to": "T1", "cost": 50}
    ]
    res = DeadlockWaitForGraphDetector.detect_deadlocks(edges)
    print("Deadlock detection result:", res)
