def yra_pirminis(n):
    """Patikrina, ar skaičius yra pirminis"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def skaitmenų_suma(n):
    """Apskaičiuoja skaičiaus skaitmenų sumą"""
    return sum(int(skaitmas) for skaitmas in str(n))


def rasti_pirminius(a, b, n):
    """Randa pirminius skaičius intervale [a, b], kurių skaitmenų suma lygi n"""
    rezultatai = []
    for skaicius in range(a, b + 1):
        if yra_pirminis(skaicius) and skaitmenų_suma(skaicius) == n:
            rezultatai.append(skaicius)
    return rezultatai


# Pagrindinis programos kūnas
if __name__ == "__main__":
    print("Programa atspausdina pirminius skaičius, kurių skaitmenų suma lygi n")
    print()
    
    # Skaityti iš vartotojo
    a = int(input("Įveskite intervalo pradžią (a): "))
    b = int(input("Įveskite intervalo pabaigą (b): "))
    n = int(input("Įveskite norimą skaitmenų sumą (n): "))
    
    # Patikrinti, kad a <= b
    if a > b:
        a, b = b, a
    
    # Rasti ir atspausdinti rezultatus
    pirminiai = rasti_pirminius(a, b, n)
    
    print()
    if pirminiai:
        print(f"Pirminiai skaičiai intervale [{a}, {b}], kurių skaitmenų suma = {n}:")
        print(pirminiai)
    else:
        print(f"Intervale [{a}, {b}] nėra pirminių skaičių, kurių skaitmenų suma = {n}")
