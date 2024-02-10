# problem przy adresowaniu otwartym, co w sytuacji przepełnienia? ewentulanie gdy nie ma? czy
# musimy sprawdzać ręcznie?
# o co chodzi z funkcja hashujaca? chyba o to, aby można było dać coś inengo jako h`(k) zamiast modulo coś
# bardziej złożonego, ale to już innym razem

import re

def replace_single_element_lists(string):
    pattern = r'\[(\d+)\]'  # Regular expression pattern to match single-element lists

    def replace(match):
        return match.group(1)  # Return the matched number without the square brackets

    replaced_string = re.sub(pattern, replace, string)
    return replaced_string


class TablicaHahsujaca:
    rozmiar = None
    metoda_konfliktu = None
    tablica = []

    def __init__(self, m, metoda):
        self.rozmiar = m
        self.metoda_konfliktu = metoda
        if 1 == metoda:
            self.tablica = ['None' for _ in range(self.rozmiar)]
        else:
            self.tablica = [None for _ in range(self.rozmiar)]

    def funkcja_hash(self, element, i):
        if 2 == self.metoda_konfliktu:  # liniowe
            index = (element % self.rozmiar + i) % self.rozmiar
        if 3 == self.metoda_konfliktu:  # kwadratowe c1=c2=1
            index = (element % self.rozmiar + i + i * i) % self.rozmiar
        if 4 == self.metoda_konfliktu:  # dwukrotne  h1(key) = key mod m  h2(key) = (key mod (m − 1)) + 1
            index = (element % self.rozmiar + i * (element % max((self.rozmiar - 1), 1) + 1)) % self.rozmiar

        return index

    def insert(self, element):
        if 1 == self.metoda_konfliktu:  # Łańcuchowa
            index = element % self.rozmiar
            if 'None' == self.tablica[index]:  # jeśli jest pusty element
                self.tablica[index] = [element]
            else:
                self.tablica[index].insert(0, element)
            return 0
        else:
            for i in range(self.rozmiar):
                index = self.funkcja_hash(element, i)
                if None == self.tablica[index] or 'Deleted' == self.tablica[index]:  # jeśli jest wolne miejsce
                    self.tablica[index] = element
                    return 0
        return 1

    def delete(self, element):
        if 1 == self.metoda_konfliktu:
            index = element % self.rozmiar
            if 'None' != self.tablica[index]:  # jeśli pod indexem nie ma None
                if element in self.tablica[index]:  # czy element istnieje w tej podtablicy
                    self.tablica[index].remove(element)
                    if 0 == len(self.tablica[index]):
                        self.tablica[index] = 'None'
                    return 0
            return 1

        else:
            for i in range(self.rozmiar):
                index = self.funkcja_hash(element, i)
                if element == self.tablica[index]:
                    self.tablica[index] = 'Deleted'
                    return 0
            return 1

    def search(self, element):
        if 1 == self.metoda_konfliktu:
            index = element % self.rozmiar
            if 'None' != self.tablica[index]:
                if element in self.tablica[index]:
                    return index
        else:
            for i in range(self.rozmiar):
                index = self.funkcja_hash(element, i)
                if element == self.tablica[index]:
                    return index
        return None  # gdy się nie powiedzie

    def wyswietlanie(self):

        if 1 == self.rozmiar:
            if isinstance(self.tablica[0], list):  # jeśli jest listą
                if 1 == len(self.tablica[0]):
                    print(str(self.tablica[0]).replace("'", ""))
                else:
                    print(str(self.tablica).replace("'", ""))
            else:
                print(str(self.tablica).replace("'", ""))
        else:
            print(replace_single_element_lists(str(self.tablica).replace("'", "")))

        # print('[' + replace_single_element_lists(str(my_tab)[1:-1]) + ']')
        #print(wyjscie)


if __name__ == '__main__':
    setup = [int(i) for i in input().split()]
    m = setup[0]
    rodzaj = setup[1]
    tablica = setup[2:]

    my_tab = TablicaHahsujaca(m, rodzaj)
    for element in tablica:
        if my_tab.insert(element):
            print("None")

    my_tab.wyswietlanie()

    while (True):
        we = [int(i) for i in input().split()]

        if -1 == we[0]:  # wyjscie
            break

        if 0 == we[0]:  # dodawanie
            x = my_tab.insert(we[1])
            my_tab.wyswietlanie()
            if x:
                print("None")

        if 1 == we[0]:  # wyszukiwanie
            print(my_tab.search(we[1]))

        if 2 == we[0]:  # usuwanie
            x = my_tab.delete(we[1])
            if x:
                print("None")
            my_tab.wyswietlanie()