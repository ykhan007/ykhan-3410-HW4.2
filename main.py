# Homework 4.2 – Weighted Graphs & Dijkstra

import math
import heapq

# 1) Coordinates (lat, lon) in decimal degrees

def build_coordinates():
    # From public coordinate sources listed in the table above
    coords = {
        "Gilroy":    (37.005783, -121.568275),
        "Cheyenne":  (41.161079, -104.805450),
        "Fargo":     (46.877186,  -96.789803),
        "Zanesville":(39.940345,  -82.013192),
        "Worcester": (42.271389,  -71.798889),
        "Tupelo":    (34.257607,  -88.703386),
        "Lubbock":   (33.576698, -101.855072),
    }
    return coords

# -----------------------------
# 2) Directed graph: only allowed edges
# From the PDF:
# - Lubbock -> Gilroy, Fargo, Zanesville
# - Gilroy -> Cheyenne
# - Cheyenne -> Fargo, Lubbock
# - Fargo -> Zanesville
# - Tupelo -> Lubbock, Zanesville
# - Zanesville -> Worcester
# - Worcester -> Tupelo
# -----------------------------
def build_graph():
    graph = {
        "Gilroy":    ["Cheyenne"],
        "Cheyenne":  ["Fargo", "Lubbock"],
        "Fargo":     ["Zanesville"],
        "Zanesville":["Worcester"],
        "Worcester": ["Tupelo"],
        "Tupelo":    ["Lubbock", "Zanesville"],
        "Lubbock":   ["Gilroy", "Fargo", "Zanesville"],
    }
    return graph

# 3) Haversine distance (miles)

def haversine(a_lat, a_lon, b_lat, b_lon):
    # Earth radius in miles 
    R = 3958.7613
    phi1 = math.radians(a_lat)
    phi2 = math.radians(b_lat)
    dphi = math.radians(b_lat - a_lat)
    dlmb = math.radians(b_lon - a_lon)

    s = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlmb/2.0)**2
    c = 2 * math.atan2(math.sqrt(s), math.sqrt(1 - s))
    return R * c

# 4) Dijkstra's algorithm

def dijkstra(graph, coords, start):
    dist = {v: math.inf for v in graph}
    parent = {v: None for v in graph}
    dist[start] = 0.0

    pq = [(0.0, start)]

    while pq:
        cur_d, u = heapq.heappop(pq)
        if cur_d > dist[u]:
            continue  # stale entry

        # explore neighbors
        for v in graph[u]:
            # weight = haversine distance between u and v
            (ulat, ulon) = coords[u]
            (vlat, vlon) = coords[v]
            w = haversine(ulat, ulon, vlat, vlon)

            new_d = cur_d + w
            if new_d < dist[v]:
                dist[v] = new_d
                parent[v] = u
                heapq.heappush(pq, (new_d, v))

    return dist, parent

# 5) Reconstruct path from parent map

def reconstruct(parent, start, goal):
    if parent.get(goal) is None and start != goal:
        return None
    path = [goal]
    while path[-1] != start:
        prev = parent[path[-1]]
        if prev is None:
            return None
        path.append(prev)
    path.reverse()
    return path

# 6) Run required queries

def run_query(graph, coords, a, b):
    dist, parent = dijkstra(graph, coords, a)
    path = reconstruct(parent, a, b)
    print(f"Query: {a} -> {b}")
    if path is None or math.isinf(dist[b]):
        print("No path\n")
    else:
        miles = dist[b]
        pretty = " -> ".join(path)
        print(f"Path: {pretty}")
        print(f"Distance: {miles:.2f} miles\n")

def main():
    coords = build_coordinates()
    graph = build_graph()

    # Required outputs:
    run_query(graph, coords, "Gilroy",   "Lubbock")
    run_query(graph, coords, "Gilroy",   "Zanesville")
    run_query(graph, coords, "Tupelo",   "Fargo")
    run_query(graph, coords, "Worcester","Gilroy")

if __name__ == "__main__":
    main()
