"""
Ciklų aptikimas orientuotame grafe (Cycle Detection in Directed Graph)
Šiame module realizuoti du pagrindiniai ciklų aptikimo algoritmai:
1. DFS metodas su spalvavimo schema (White-Gray-Black)
2. Topologinis rūšiavimas (Topological Sort)
"""

from collections import defaultdict
from typing import List, Tuple, Set


class DirectedGraph:
    """Orientuoto grafo klasė su ciklų aptikimo metodais"""
    
    def __init__(self, vertices_count: int):
        """
        Inicijalizuoja orientuotą grafą
        
        Args:
            vertices_count: Viršūnių skaičius grafe
        """
        self.vertices_count = vertices_count
        self.graph = defaultdict(list)
        self.vertices = list(range(vertices_count))
    
    def add_edge(self, u: int, v: int) -> None:
        """
        Prideda briauną iš viršūnės u į viršūnę v
        
        Args:
            u: Pradžios viršūnė
            v: Galinė viršūnė
        """
        if u < self.vertices_count and v < self.vertices_count:
            self.graph[u].append(v)
        else:
            raise ValueError(f"Viršūnės numeriai turi būti nuo 0 iki {self.vertices_count - 1}")
    
    def has_cycle_dfs(self) -> bool:
        """
        Tikrina ar grafe yra ciklas naudojant DFS algoritmą.
        Spalvavimo schema:
        - Balta (0): Viršūnė dar neapie šalta
        - Pilka (1): Viršūnė šiuo metu apdorojama (DFS stakle)
        - Juoda (2): Viršūnė jau baigta apdoroti
        
        Jei surandame briauną į pilką viršūnę, randame ciklą.
        
        Returns:
            True jei grafe yra ciklas, False priešingu atveju
        """
        color = [0] * self.vertices_count  # 0 - balta, 1 - pilka, 2 - juoda
        
        def dfs_visit(vertex: int) -> bool:
            """
            Nerekursyvus DFS apsilankymas su stack'u
            """
            color[vertex] = 1  # Pažymime kaip pilką
            
            for neighbor in self.graph[vertex]:
                if color[neighbor] == 1:  # Briaua į pilką viršūnę = ciklas
                    return True
                if color[neighbor] == 0:  # Balta viršūnė - aplankome ją
                    if dfs_visit(neighbor):
                        return True
            
            color[vertex] = 2  # Pažymime kaip juodą
            return False
        
        # Patikrinti kiekvieną viršūnę
        for vertex in range(self.vertices_count):
            if color[vertex] == 0:
                if dfs_visit(vertex):
                    return True
        
        return False
    
    def has_cycle_dfs_stack(self) -> bool:
        """
        Tikrina ar grafe yra ciklas naudojant iteracinį DFS (stack'u)
        
        Returns:
            True jei grafe yra ciklas, False priešingu atveju
        """
        color = [0] * self.vertices_count
        
        for start in range(self.vertices_count):
            if color[start] != 0:
                continue
            
            stack = [start]
            color[start] = 1
            
            while stack:
                vertex = stack[-1]
                found_unvisited = False
                
                for neighbor in self.graph[vertex]:
                    if color[neighbor] == 1:  # Ciklas surastas
                        return True
                    if color[neighbor] == 0:  # Negrąžinta viršūnė
                        color[neighbor] = 1
                        stack.append(neighbor)
                        found_unvisited = True
                        break
                
                if not found_unvisited:
                    color[vertex] = 2
                    stack.pop()
        
        return False
    
    def find_cycle_dfs(self) -> List[int]:
        """
        Randa ciklą grafe naudojant DFS algoritmą.
        
        Returns:
            Ciklo viršūnių sąrašas arba tuščias sąrašas jei ciklo nėra
        """
        color = [0] * self.vertices_count
        parent = [-1] * self.vertices_count
        cycle_start = -1
        cycle_end = -1
        
        def dfs_find_cycle(vertex: int) -> bool:
            nonlocal cycle_start, cycle_end
            color[vertex] = 1
            
            for neighbor in self.graph[vertex]:
                if color[neighbor] == 1:
                    cycle_start = neighbor
                    cycle_end = vertex
                    return True
                if color[neighbor] == 0:
                    parent[neighbor] = vertex
                    if dfs_find_cycle(neighbor):
                        return True
            
            color[vertex] = 2
            return False
        
        for vertex in range(self.vertices_count):
            if color[vertex] == 0:
                if dfs_find_cycle(vertex):
                    # Statome ciklą iš cycle_start iki cycle_end
                    cycle = []
                    current = cycle_end
                    while current != cycle_start:
                        cycle.append(current)
                        current = parent[current]
                    cycle.append(cycle_start)
                    return cycle[::-1]
        
        return []
    
    def topological_sort_with_cycle_check(self) -> Tuple[bool, List[int]]:
        """
        Bandoma atlikti topologinį rūšiavimą naudojant Kahn algoritmą.
        Jei ciklas egzistuoja, rūšiavimas nepavyks.
        
        Returns:
            (has_cycle, topological_order)
        """
        in_degree = [0] * self.vertices_count
        
        # Skaičiuojame įeinančių briaunų skaičius kiekvienai viršūnei
        for vertex in range(self.vertices_count):
            for neighbor in self.graph[vertex]:
                in_degree[neighbor] += 1
        
        # Pradedame nuo viršūnių su 0 įeinančių briaunų
        queue = [v for v in range(self.vertices_count) if in_degree[v] == 0]
        topological_order = []
        
        while queue:
            vertex = queue.pop(0)
            topological_order.append(vertex)
            
            for neighbor in self.graph[vertex]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Jei topological_order turi mažiau viršūnių nei grafe,
        # tai reiškia kad yra ciklas
        has_cycle = len(topological_order) != self.vertices_count
        
        return has_cycle, topological_order
    
    def print_graph(self) -> None:
        """Išspausdina grafo reprezentaciją"""
        print("Grafo reprezentacija (sąrašų pavidalu):")
        for vertex in range(self.vertices_count):
            print(f"Viršūnė {vertex}: {self.graph[vertex]}")


def main():
    """Pagrindinė funkcija su pavyzdžiais"""
    
    print("=" * 60)
    print("CIKLŲ APTIKIMAS ORIENTUOTAME GRAFE")
    print("=" * 60)
    
    # Pavyzdys 1: Grafas BE CIKLO
    print("\n--- Pavyzdys 1: Grafas BE CIKLO ---")
    g1 = DirectedGraph(4)
    g1.add_edge(0, 1)
    g1.add_edge(0, 2)
    g1.add_edge(1, 3)
    g1.add_edge(2, 3)
    
    g1.print_graph()
    print(f"\nAr yra ciklas (DFS)? {g1.has_cycle_dfs()}")
    print(f"Ar yra ciklas (DFS Stack)? {g1.has_cycle_dfs_stack()}")
    has_cycle, topo_order = g1.topological_sort_with_cycle_check()
    print(f"Ar yra ciklas (Topologinis)? {has_cycle}")
    if not has_cycle:
        print(f"Topologinis rūšiavimas: {topo_order}")
    
    cycle = g1.find_cycle_dfs()
    if cycle:
        print(f"Rastas ciklas: {cycle}")
    else:
        print("Ciklo nėra")
    
    # Pavyzdys 2: Grafas SU CIKLU
    print("\n--- Pavyzdys 2: Grafas SU CIKLU ---")
    g2 = DirectedGraph(4)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    g2.add_edge(3, 1)  # Ciklas: 1 -> 2 -> 3 -> 1
    
    g2.print_graph()
    print(f"\nAr yra ciklas (DFS)? {g2.has_cycle_dfs()}")
    print(f"Ar yra ciklas (DFS Stack)? {g2.has_cycle_dfs_stack()}")
    has_cycle, topo_order = g2.topological_sort_with_cycle_check()
    print(f"Ar yra ciklas (Topologinis)? {has_cycle}")
    
    cycle = g2.find_cycle_dfs()
    if cycle:
        print(f"Rastas ciklas: {cycle}")
    else:
        print("Ciklo nėra")
    
    # Pavyzdys 3: Sudėtingesnis grafas SU CIKLU
    print("\n--- Pavyzdys 3: Sudėtingesnis grafas SU CIKLU ---")
    g3 = DirectedGraph(6)
    g3.add_edge(0, 1)
    g3.add_edge(1, 2)
    g3.add_edge(2, 0)  # Ciklas: 0 -> 1 -> 2 -> 0
    g3.add_edge(3, 4)
    g3.add_edge(4, 5)
    
    g3.print_graph()
    print(f"\nAr yra ciklas (DFS)? {g3.has_cycle_dfs()}")
    print(f"Ar yra ciklas (DFS Stack)? {g3.has_cycle_dfs_stack()}")
    
    cycle = g3.find_cycle_dfs()
    if cycle:
        print(f"Rastas ciklas: {cycle}")
    else:
        print("Ciklo nėra")
    
    # Pavyzdys 4: Interaktyvus testas
    print("\n--- Pavyzdys 4: Jūsų paties grafas ---")
    print("Sukurkime 5 viršūnių grafą:")
    g4 = DirectedGraph(5)
    
    edges = [
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 3),
        (3, 4)
    ]
    
    print("Pridedamos briaunos:")
    for u, v in edges:
        g4.add_edge(u, v)
        print(f"  {u} -> {v}")
    
    g4.print_graph()
    print(f"\nAr yra ciklas? {g4.has_cycle_dfs()}")


if __name__ == "__main__":
    main()
