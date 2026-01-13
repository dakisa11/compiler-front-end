class LeksickiAnalizatorPJ:
    def __init__(self, program):
        self.program=program
        self.pozicija = 0
        self.broj_retka = 1
        self.tokeni = []

    def je_praznina(self, znak):
        return znak in ' \t\n\r'

    def je_znamenka(self, znak):
        return znak is not None and '0' <= znak <= '9'

    def je_slovo(self, znak):
        return znak is not None and ('a' <= znak <= 'z' or 'A' <= znak <= 'Z')

    def sljedeci_znak(self):
        if self.pozicija < len(self.program):
            znak = self.program[self.pozicija ]
            self.pozicija+= 1
            if znak == '\n':
                self.broj_retka +=1
            return znak
        return None

    def pogledaj_znak(self):
        if self.pozicija < len(self.program ):
            return self.program[self.pozicija ]
        return None

    def dodaj_token(self, vrsta_tokena, vrijednost):
        self.tokeni.append((vrsta_tokena, self.broj_retka, vrijednost))

    def preskoci_praznine(self):
        while self.pogledaj_znak() and self.je_praznina(self.pogledaj_znak()):
            self.sljedeci_znak()

    def preskoci_komentar(self):
        while self.pogledaj_znak() and self.pogledaj_znak() != '\n':
            self.sljedeci_znak()

    def analiziraj(self):
        kljucne_rijeci = {"za": "KR_ZA", "od": "KR_OD", "do": "KR_DO", "az": "KR_AZ"}
        operatori = {'=': 'OP_PRIDRUZI', '+': 'OP_PLUS', '-': 'OP_MINUS', '*': 'OP_PUTA', '/': 'OP_DIJELI'}
        zagrade = {'(': 'L_ZAGRADA', ')': 'D_ZAGRADA'}

        while self.pozicija < len(self.program):
            self.preskoci_praznine()
            znak = self.pogledaj_znak()

            if znak is None:
                break

            if znak == '/':
                sljedeci_znak = self.program[self.pozicija + 1] if self.pozicija + 1 < len(self.program) else None
                if sljedeci_znak == '/':
                    self.preskoci_komentar()
                    continue

            if self.je_slovo(znak):
                pocetna_pozicija = self.pozicija
                while self.je_slovo(self.pogledaj_znak()) or self.je_znamenka(self.pogledaj_znak()):
                    self.sljedeci_znak()
                vrijednost = self.program[pocetna_pozicija:self.pozicija]
                if vrijednost in kljucne_rijeci:
                    self.dodaj_token(kljucne_rijeci[vrijednost], vrijednost)
                else:
                    self.dodaj_token('IDN', vrijednost)

            elif self.je_znamenka(znak):
                pocetna_pozicija = self.pozicija
                while self.je_znamenka(self.pogledaj_znak()):
                    self.sljedeci_znak()
                vrijednost = self.program[pocetna_pozicija:self.pozicija]
                self.dodaj_token('BROJ', vrijednost)

            elif znak in operatori:
                self.dodaj_token(operatori[znak], znak)
                self.sljedeci_znak()

            elif znak in zagrade:
                self.dodaj_token(zagrade[znak], znak)
                self.sljedeci_znak()

            else:
                raise SyntaxError(f"Nepoznati znak: {znak} u retku {self.broj_retka}")

    def ispisi_tokene(self):
        for token in self.tokeni:
            print(f"{token[0]} {token[1]} {token[2]}")

unos_linija = []
prazne_linije = 0
try:
    while True:
        linija = input()
        if linija == "":
            prazne_linije+=1     
        if prazne_linije == 2:
            break
        else:
            prazne_linije = 0
            unos_linija.append( linija )

except EOFError:
    pass

program = "\n".join(unos_linija)

analizator = LeksickiAnalizatorPJ(program)
analizator.analiziraj()
analizator.ispisi_tokene()
