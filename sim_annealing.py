import tkinter as tk
import matplotlib.pyplot as plt
import random
import math
import numpy as np


def energia_potencjalna(q1, q2, r, k):
    Ep = k * ((q1 * q2) / r)
    return Ep


def optymalizacja(q1, q2, q1_x, q1_y, k, temperatura, liczba_iteracji):
    naj_pozycja = [random.uniform(0, 1000), random.uniform(0, 1000)]
    r = math.sqrt((q1_x - naj_pozycja[0]) ** 2 + (q1_y - naj_pozycja[1]) ** 2)
    naj_wynik = energia_potencjalna(q1, q2, r, k)
    obec_pozycja, obec_wynik = naj_pozycja, naj_wynik

    positions = [(obec_pozycja[0], obec_pozycja[1], obec_wynik)]

    for i in range(liczba_iteracji):
        kand_pozycja = [
            max(0, min(1000, obec_pozycja[0] + random.uniform(-0.5, 0.5))),
            max(0, min(1000, obec_pozycja[1] + random.uniform(-0.5, 0.5))),
        ]
        kand_r = math.sqrt((q1_x - kand_pozycja[0]) ** 2 + (q1_y - kand_pozycja[1]) ** 2)
        kand_wynik = energia_potencjalna(q1, q2, kand_r, k)

        if kand_wynik < naj_wynik:
            naj_pozycja, naj_wynik = kand_pozycja, kand_wynik

            diff = kand_wynik - obec_wynik
            t = temperatura / (i + 1)
            metropolis = np.exp(-diff / t)

            if diff < 0 or random.random() < metropolis:
                obec_pozycja, obec_wynik = kand_pozycja, kand_wynik

        positions.append((obec_pozycja[0], obec_pozycja[1], obec_wynik))
    print("Najlepszy wynik: ",naj_wynik)
    print("Najlepsza pozycja:",naj_pozycja)
    return naj_pozycja, naj_wynik, positions


def gui():
    k = 9*1000000000
    root = tk.Tk()
    root.title("Parametry")
    root.geometry("300x400")

    label = tk.Label(root, text="Podaj parametry", font=30)
    label.pack()

    q1lab = tk.Label(root, text="Wartość q1: ")
    q1lab.pack()
    q1 = tk.Entry(root)
    q1.pack()

    q2lab = tk.Label(root, text="Wartość q2: ")
    q2lab.pack()
    q2 = tk.Entry(root)
    q2.pack()

    xlab = tk.Label(root, text="Pozycja X [0,1000]: ")
    xlab.pack()
    x = tk.Entry(root)
    x.pack()

    ylab = tk.Label(root, text="Pozycja Y [0,1000]: ")
    ylab.pack()
    y = tk.Entry(root)
    y.pack()

    templab = tk.Label(root, text="Temperatura: ")
    templab.pack()
    temp = tk.Entry(root)
    temp.pack()

    itlab = tk.Label(root, text="Liczba iteracji: ")
    itlab.pack()
    it = tk.Entry(root)
    it.pack()

    actionButton = tk.Button(root, text="Uruchom", width=10,
                             command=lambda: run_optimization(float(q1.get()), float(q2.get()), float(x.get()),
                                                              float(y.get()), k, float(temp.get()),
                                                              int(it.get())))
    actionButton.pack()

    root.mainloop()


def run_optimization(q1, q2, q1_x, q1_y, k, temperatura, liczba_iteracji):
    naj_pozycja, naj_wynik, positions = optymalizacja(q1, q2, q1_x, q1_y, k, temperatura, liczba_iteracji)


    x_positions, y_positions, energies = zip(*positions)

    plt.figure()

    sc = plt.scatter(x_positions, y_positions, c=energies, cmap='viridis', marker='o')
    plt.colorbar(sc, label='Energia potencjalna')
    plt.xlim(0,1000)
    plt.ylim(0,1000)
    plt.scatter(naj_pozycja[0], naj_pozycja[1], color='red', marker='x', label='Optymalna pozycja')
    plt.scatter(q1_x,q1_y,color='blue',marker='x',label="Pozycja ładunku q1")
    plt.xlabel('Oś X')
    plt.ylabel('Oś Y')

    plt.title('Symulacja wyżarzania')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    gui()
