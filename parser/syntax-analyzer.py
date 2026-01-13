unos_linija = []
try:
    while True:
        linija = input()
        if linija == "":
            break
        else:
            unos_linija.append(linija)
except EOFError:
    pass

program = "\n".join(unos_linija).split("\n")

ulazni_niz = []
for i in range(len(program)):
    ulazni_niz.append(program[i].split(" ")[0])

class SintaksnaAnalizaPJ:
    def __init__(self, ulazni_niz, program):
        self.ulazni_niz = ulazni_niz
        self.program = program  
        self.pozicija = 0  
        self.stog = [("<program>", 0)]
        self.ispis = ""
        
    def parse(self):
        while self.stog:
            simbol, dubina = self.stog.pop()

            if ulazni_niz[0] not in ["IDN", "KR_ZA"]:
                self.greska(ulazni_niz[0])
                break

            if simbol not in ["KR_DO", "KR_AZ", "L_ZAGRADA", "D_ZAGRADA"]:
                self.ispisi_cvor(simbol, dubina)

            if simbol == "<program>":
                self.stog.append(("<lista_naredbi>", dubina + 1))
            elif simbol == "<lista_naredbi>":
                if self.pogledaj_ulaz() in ["IDN", "KR_ZA"]:
                    self.stog.append(("<lista_naredbi>", dubina + 1))
                    self.stog.append(("<naredba>", dubina + 1))
                else:
                    self.ispisi_cvor("$", dubina + 1)
            elif simbol == "<naredba>":
                if self.pogledaj_ulaz() == "IDN":
                    self.stog.append(("<naredba_pridruzivanja>", dubina + 1))
                elif self.pogledaj_ulaz() == "KR_ZA":
                    self.stog.append(("<za_petlja>", dubina + 1))
                else:
                    self.greska("naredba")
                    return
            elif simbol == "<naredba_pridruzivanja>":
                self.procesiraj_znak("IDN", dubina + 1)
                self.procesiraj_znak("OP_PRIDRUZI", dubina + 1)
                self.stog.append(("<E>", dubina + 1))
            elif simbol == "<za_petlja>":
                self.procesiraj_znak("KR_ZA", dubina + 1)
                self.procesiraj_znak("IDN", dubina + 1)
                self.procesiraj_znak("KR_OD", dubina + 1)
                self.stog.append(("KR_AZ", dubina + 1))
                self.stog.append(("<lista_naredbi>", dubina + 1))
                self.stog.append(("<E>", dubina + 1))
                self.stog.append(("KR_DO", dubina + 1))
                self.stog.append(("<E>", dubina + 1))
            elif simbol == "<E>":
                self.stog.append(("<E_lista>", dubina + 1))
                self.stog.append(("<T>", dubina + 1))
            elif simbol == "<E_lista>":
                if self.pogledaj_ulaz() == "OP_PLUS":
                    self.procesiraj_znak("OP_PLUS", dubina + 1)
                    self.stog.append(("<E>", dubina + 1))
                elif self.pogledaj_ulaz() == "OP_MINUS":
                    self.procesiraj_znak("OP_MINUS", dubina + 1)
                    self.stog.append(("<E>", dubina + 1))
                else:
                    self.ispisi_cvor("$", dubina + 1)
            elif simbol == "<T>":
                self.stog.append(("<T_lista>", dubina + 1))
                self.stog.append(("<P>", dubina + 1))
            elif simbol == "<T_lista>":
                if self.pogledaj_ulaz() == "OP_PRIDRUZI":
                    self.greska(simbol)
                    break
                if self.pogledaj_ulaz() == "OP_PUTA":
                    self.procesiraj_znak("OP_PUTA", dubina + 1)
                    self.stog.append(("<T>", dubina + 1))
                elif self.pogledaj_ulaz() == "OP_DIJELI":
                    self.procesiraj_znak("OP_DIJELI", dubina + 1)
                    self.stog.append(("<T>", dubina + 1))
                else:
                    self.ispisi_cvor("$", dubina + 1)
            elif simbol == "<P>":
                if self.pogledaj_ulaz() == "OP_PLUS":
                    self.procesiraj_znak("OP_PLUS", dubina + 1)
                    self.stog.append(("<P>", dubina + 1))
                elif self.pogledaj_ulaz() == "OP_MINUS":
                    self.procesiraj_znak("OP_MINUS", dubina + 1)
                    self.stog.append(("<P>", dubina + 1))
                elif self.pogledaj_ulaz() == "L_ZAGRADA":
                    self.procesiraj_znak("L_ZAGRADA", dubina + 1)
                    self.stog.append(("D_ZAGRADA", dubina + 1))
                    self.stog.append(("<E>", dubina + 1))
                elif self.pogledaj_ulaz() == "IDN":
                    self.procesiraj_znak("IDN", dubina + 1)
                elif self.pogledaj_ulaz() == "BROJ":
                    self.procesiraj_znak("BROJ", dubina + 1)
                else:
                    self.greska("<P>")
                    return
            elif simbol == "KR_DO":
                self.procesiraj_znak("KR_DO", dubina)
            elif simbol == "KR_AZ":
                self.procesiraj_znak("KR_AZ", dubina)
            elif simbol == "D_ZAGRADA":
                self.procesiraj_znak("D_ZAGRADA", dubina)
            else:
                self.greska(simbol)
                return

    def ispisi_cvor(self, naziv, dubina):
        self.ispis += (" " * dubina + naziv + "\n")

    def procesiraj_znak(self, ocekivani, dubina):
        if self.pogledaj_ulaz() == ocekivani:
            self.ispis += (" " * dubina + self.program[self.pozicija] + "\n")
            self.pozicija += 1
        else:
            self.greska(ocekivani)

    def pogledaj_ulaz(self):
        if self.pozicija < len(self.ulazni_niz):
            return self.ulazni_niz[self.pozicija]
        return None

    def greska(self, ocekivani):
        if self.pozicija < len(self.program):
            print(f"err {self.program[self.pozicija]}")
            self.ispis = ""
        else:
            print("err kraj")
            self.ispis = ""
        self.stog.clear()
    def print(self):
        print(self.ispis)

analizator = SintaksnaAnalizaPJ(ulazni_niz, program)
analizator.parse()
analizator.print()
