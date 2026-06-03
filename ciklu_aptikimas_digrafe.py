"""
Ciklų aptikimas orientuotame grafe (Cycle Detection in Directed Graph)
Naudojamas DFS metodas su spalvavimo schema (White-Gray-Black)
"""

from collections import defaultdict
from typing import List


class DirectedGraph:
    """digrafo klasė su DFS ciklų aptikimo metodu"""
    
    def __init__(self, vertices_count: int):
        """
        Inicijuoja orientuotą grafą
        
            vertices_count: Viršūnių skaičius grafe
        """
        self.vertices_count = vertices_count
        self.graph = defaultdict(list)
        self.vertices = list(range(vertices_count))
    
    def add_edge(self, u: int, v: int) -> None:
        """
        Prideda briauną iš viršūnės u į viršūnę v
        
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
        - Pilka (1): Viršūnė šiuo metu apdorojama (DFS Stacke)
        - Juoda (2): Viršūnė jau baigta apdoroti
        
        Jei surandame briauną į pilką viršūnę, randame ciklą.
        
        Returns:
            True jei grafe yra ciklas, False priešingu atveju
        """
        color = [0] * self.vertices_count  # 0 - balta, 1 - pilka, 2 - juoda
        
        def dfs_visit(vertex: int) -> bool:
            """
            Nerekursyvus DFS "apsilankymas" su stack'u
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
    
    def print_graph(self) -> None:
        """Išspausdina grafo reprezentaciją"""
        print("Grafo reprezentacija (sąrašų pavidalu):")
        for vertex in range(self.vertices_count):
            print(f"Viršūnė {vertex}: {self.graph[vertex]}")


def main():
    """Interaktyvi programa ciklų aptikimui orientuotame grafe"""
    
    print("=" * 60)
    print("CIKLŲ APTIKIMAS ORIENTUOTAME GRAFE")
    print("=" * 60)
    
    # Gauti viršūnių skaičių
    while True:
        try:
            vertices_count = int(input("\nKiek viršūnių grafe? (skaičius >= 1): "))
            if vertices_count < 1:
                print("KLAIDA: Viršūnių skaičius turi būti daugiau nei 0!")
                continue
            break
        except ValueError:
            print("KLAIDA: Prašom įvesti sveikąjį skaičių!")
    
    # Sukurti grafą
    graph = DirectedGraph(vertices_count)
    
    # Gauti briaunų skaičių
    while True:
        try:
            edges_count = int(input(f"\nKiek briaunų? (maksimalus: {vertices_count * vertices_count}): "))
            if edges_count < 0:
                print("KLAIDA: Briaunų skaičius negali būti neigiamas!")
                continue
            break
        except ValueError:
            print("KLAIDA: Prašom įvesti sveikąjį skaičių!")
    
    # Įvesti briaunas
    print(f"\nĮveskite {edges_count} briaunas (formato: u v):")
    print(f"(viršūnės numeris nuo 0 iki {vertices_count - 1})")
    
    added_edges = 0
    while added_edges < edges_count:
        try:
            edge_input = input(f"Briauna {added_edges + 1}/{edges_count}: ").strip()
            if not edge_input:
                continue
            
            u, v = map(int, edge_input.split())
            
            if u < 0 or u >= vertices_count or v < 0 or v >= vertices_count:
                print(f"KLAIDA: Viršūnės turi būti nuo 0 iki {vertices_count - 1}")
                continue
            
            graph.add_edge(u, v)
            print(f"GERAI: Pridėta briauna: {u} -> {v}")
            added_edges += 1
            
        except ValueError:
            print("KLAIDA: Neteisingas formatas! Vėl bandykite (pvz: 0 1)")
        except Exception as e:
            print(f"KLAIDA: {e}")
    
    # Išspausdinti grafą
    print("\n" + "=" * 60)
    print("GRAFO REPREZENTACIJA")
    print("=" * 60)
    graph.print_graph()
    
    # Atlikti ciklų aptikimą
    print("\n" + "=" * 60)
    print("CIKLŲ APTIKIMO REZULTATAI (DFS)")
    print("=" * 60)
    
    # DFS metodas
    has_cycle_dfs = graph.has_cycle_dfs()
    print(f"\nAr grafe yra ciklas? {'TAIP' if has_cycle_dfs else 'NE'}")
    
    # Rasti konkretų ciklą
    cycle = graph.find_cycle_dfs()
    if cycle:
        print(f"Rastas ciklas: {' -> '.join(map(str, cycle))} -> {cycle[0]}")
    else:
        print("Ciklo nėra grafe")
    
    print("\n" + "=" * 60)
    print("Analizė baigta!")
    print("=" * 60)


if __name__ == "__main__":
    main()
