"""Distributed Deadlock Wait-For-Graph Detector.
100% Python Standard Library.
"""

class DeadlockWaitForGraphDetector:
    """Real-time Tarjan SCC cycle detection on lock Wait-For-Graphs with minimal-cost victim transaction arbitrator."""

    @staticmethod
    def detect_deadlocks(dependencies: list) -> dict:
        graph = {}
        tx_costs = {}

        for edge in dependencies:
            u, v = edge["from"], edge["to"]
            if u not in graph: graph[u] = []
            if v not in graph: graph[v] = []
            graph[u].append(v)
            tx_costs[u] = edge.get("cost", 10)
            if v not in tx_costs: tx_costs[v] = edge.get("cost", 10)

        index = 0
        indices = {}
        lowlinks = {}
        on_stack = set()
        stack = []
        sccs = []

        def strongconnect(node):
            nonlocal index
            indices[node] = index
            lowlinks[node] = index
            index += 1
            stack.append(node)
            on_stack.add(node)

            for neighbor in graph.get(node, []):
                if neighbor not in indices:
                    strongconnect(neighbor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
                elif neighbor in on_stack:
                    lowlinks[node] = min(lowlinks[node], indices[neighbor])

            if lowlinks[node] == indices[node]:
                current_scc = []
                while True:
                    w = stack.pop()
                    on_stack.remove(w)
                    current_scc.append(w)
                    if w == node: break
                if len(current_scc) > 1 or (len(current_scc) == 1 and node in graph.get(node, [])):
                    sccs.append(current_scc)

        for node in list(graph.keys()):
            if node not in indices:
                strongconnect(node)

        victims = []
        for scc in sccs:
            victim = min(scc, key=lambda tx: tx_costs.get(tx, 999))
            victims.append(victim)

        return {
            "total_transactions": len(graph),
            "deadlocks_detected": len(sccs),
            "cycles": sccs,
            "recommended_victims": victims,
            "system_healthy": len(sccs) == 0
        }
