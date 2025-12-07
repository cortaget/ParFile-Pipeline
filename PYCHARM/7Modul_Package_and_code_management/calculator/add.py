import sys

def add(a, b):
    return a + b

if __name__ == "__main__":

    if len(sys.argv) == 3:
        print("Použití: python add.py <číslo1> <číslo2>")

        num1 = float(sys.argv[1])

        num2 = float(sys.argv[2])
        result = add(num1, num2)
        print(f"Výsledek sčítání: {result}")
    else:
        num1 = float(input("Zadej první číslo: "))
        num2 = float(input("Zadej druhé číslo: "))
        result = add(num1, num2)
        print(f"Výsledek sčítání: {result}")
