import sys

class SemantickiAnalizator:
    def __init__(self, ulazni_redci):
        self.ulazni_redci = ulazni_redci
        self.varijable = {}  # {ime: (redak_definicije, je_globalna)}
        self.stog_blokova = []  # Stog za lokalne varijable unutar blokova

    def parsiraj_stablo(self):
        trenutni_blok = []
        for i, redak in enumerate(self.ulazni_redci):
            #print(trenutni_blok)
            tokeni = redak.strip().split()
            if not tokeni:  # Preskoči prazne redke
                continue

            prijasnji_tokeni = (
                self.ulazni_redci[i - 1].strip().split() if i > 0 else None
            )

            # Ako blok ima tačno 2 tokena, završava se blok (osim operatora)
            if len(trenutni_blok) == 2 and tokeni[0] not in [
                "OP_PLUS",
                "OP_MINUS",
                "OP_PUTA",
                "OP_DIJELI",
                "KR_ZA",
                "KR_OD",
                "KR_DO",
                "KR_AZ"
            ]:
                trenutni_blok.append(tokeni)
                self.obradi_blok(trenutni_blok)
                trenutni_blok = []
            else:
                trenutni_blok.append(tokeni)

        # Obradi preostali blok ako postoji
        if trenutni_blok:
            self.obradi_blok(trenutni_blok)

    def obradi_blok(self, blok):
        u_petlji = False
        iterator_var = None

        for i, tokeni in enumerate(blok):
            #print(self.varijable)
            tip = tokeni[0]
            redak = int(tokeni[1])
            ime_varijable = tokeni[2] if len(tokeni) > 2 else None

            if tip == "KR_ZA":
                u_petlji = True
                self.stog_blokova.append({})

            elif tip == "KR_AZ":
                
                u_petlji = False
                self.stog_blokova.pop()  # Završava blok

            elif tip == "KR_OD":
                if i > 0 and blok[i - 1][0] == "IDN":
                    iterator_var = blok[i - 1][2]
                    iterator_redak = int(blok[i - 1][1])
                    # Ako je iterator već definiran u trenutnom bloku, prijavi grešku
                    if iterator_var in self.stog_blokova[-1]:
                        self.prijavi_pogresku(iterator_redak, iterator_var)
                    self.stog_blokova[-1][iterator_var] = (iterator_redak, u_petlji)


            elif tip == "KR_DO":
                if ime_varijable in self.stog_blokova[-1]:
                    redak_definicije = self.stog_blokova[-1][ime_varijable][0]
                    if redak_definicije == redak:
                        self.prijavi_pogresku(redak, ime_varijable)

            elif tip == "IDN" and not blok[i - 1][0] == "KR_ZA":
                if self.je_definicija(blok, i):
                    # Definicija varijable
                    if ime_varijable not in self.varijable:
                        if u_petlji and ime_varijable in self.stog_blokova:
                            self.stog_blokova[-1][ime_varijable] = (redak, u_petlji)
                        else:
                            self.varijable[ime_varijable] = (redak, not u_petlji)
                else:
                    # Korištenje varijable
                    self.provjeri_koristenje_varijable(ime_varijable, redak)
            #print(self.varijable)
            print(self.stog_blokova)

    def je_definicija(self, blok, indeks):
        # Provjerava je li trenutni token definicija varijable
        if indeks < len(blok) - 1 and blok[indeks + 1][0] == "OP_PRIDRUZI":
            return True
        return False

    def provjeri_koristenje_varijable(self, ime_varijable, redak):
        for blok in reversed(self.stog_blokova):
            if ime_varijable in blok:
                redak_definicije = blok[ime_varijable][0]
                # Ako varijabla koristi samu sebe u definiciji, prijavi grešku
                if redak_definicije == redak:
                    self.prijavi_pogresku(redak, ime_varijable)
                print(f"{redak} {redak_definicije} {ime_varijable}")
                return
        # Ako nije u lokalnim blokovima, provjeri globalni kontekst
        if ime_varijable in self.varijable:
            redak_definicije, je_globalna = self.varijable[ime_varijable]
            print(f"{redak} {redak_definicije} {ime_varijable}")
        else:
            self.prijavi_pogresku(redak, ime_varijable)



    def prijavi_pogresku(self, redak, ime_varijable):
        print(f"err {redak} {ime_varijable}")
        sys.exit(1)

    def pokreni(self):
        self.parsiraj_stablo()



if __name__ == "__main__":
    ulazni_podaci = []
    try:
        while True:
            ulazni_redak = input().strip()
            if not ulazni_redak:
                break
            # Zadržavamo samo retke koji sadrže relevantne tokene
            ulazni_tokeni = ulazni_redak.split()
            if ulazni_tokeni and ulazni_tokeni[0] in {"IDN", "BROJ", "KR_ZA", "KR_OD", "KR_DO", "KR_AZ", "OP_PRIDRUZI", "OP_PLUS", "OP_MINUS", "OP_PUTA", "OP_DIJELI"}:
                ulazni_podaci.append(ulazni_redak)
    except EOFError:
        pass
    #print(ulazni_podaci)
    analizator = SemantickiAnalizator(ulazni_podaci)
    analizator.pokreni()
    
