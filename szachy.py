import pygame
import os


def quit():
    import sys

    pygame.quit()
    sys.exit(0)


class Gra:

    def __init__(self):
        self.pola = {
            (0, 7): 'W', (1, 7): 'S', (2, 7): 'G', (3, 7): 'H', (4, 7): 'K',
            (5, 7): 'G', (6, 7): 'S', (7, 7): 'W', (0, 6): 'P', (1, 6): 'P',
            (2, 6): 'P', (3, 6): 'P', (4, 6): 'P', (5, 6): 'P', (6, 6): 'P',
            (7, 6): 'P', (0, 0): 'w', (1, 0): 's', (2, 0): 'g', (3, 0): 'h',
            (4, 0): 'k', (5, 0): 'g', (6, 0): 's', (7, 0): 'w', (0, 1): 'p',
            (1, 1): 'p', (2, 1): 'p', (3, 1): 'p', (4, 1): 'p', (5, 1): 'p',
            (6, 1): 'p', (7, 1): 'p'
        }

        self.symbol = {
            'W': '\u2656', 'S': '\u2658', 'G': '\u2657', 'H': '\u2655',
            'K': '\u2654', 'P': '\u2659', 'w': '\u265C', 's': '\u265E',
            'g': '\u265D', 'h': '\u265B', 'k': '\u265A', 'p': '\u265F'
        }

        self.wszystkie_figury = [list('HhWWwwGGggSSssPPPPPPPPpppppppp'), []]

        font = 'DejaVu Sans Mono 400.ttf'
        self.font22 = pygame.font.Font(font, 22)
        self.font25 = pygame.font.Font(font, 25)
        self.font30 = pygame.font.Font(font, 30)
        self.font40 = pygame.font.Font(font, 40)
        self.font50 = pygame.font.Font(font, 50)
        self.font100 = pygame.font.Font(font, 100)

        self.okno = pygame.display.set_mode((950, 800))

        self.krolowie_i_wieze = [
            (4, 7), (0, 7), (7, 7), (4, 0), (0, 0), (7, 0)
        ]
        self.mozliwosci_roszady = [0, 0, 0, 0, 0, 0]

        self.poprzednie_ruchy = []

        self.ruszono_o_2 = None
        self.kliknieta = None
        self.ostatni = None

        self.krol = (4, 7)
        self.atakuja = []
        self.tura = 1

        self.przycisk_poddaj_sie = pygame.Rect(805, 80, 140, 40)
        self.przycisk_nowa_gra = pygame.Rect(805, 440, 140, 30)
        self.przycisk_cofnij = pygame.Rect(805, 340, 140, 30)

        self.przycisk_zgoda_remis = pygame.Rect(805, 80, 140, 40)
        self.przycisk_gramy_dalej = pygame.Rect(805, 30, 140, 40)
        self.przycisk_remis = pygame.Rect(805, 30, 140, 40)

    def rysowanie_panelu(self, mode=None):
        pygame.draw.rect(self.okno, (255, 128, 0), pygame.Rect(800, 0, 150, 800))

        self.przycisk_poddaj_sie.y = 80
        self.przycisk_remis.y = 30
        self.przycisk_poddaj_sie.y += 600*(self.tura % 2)
        self.przycisk_remis.y += 700*(self.tura % 2)

        runda = self.font30.render('{}'.format(self.tura - 1), True, (255, 255, 255))
        poddaj_sie = self.font22.render('Poddaj się', True, (255, 255, 255))
        nowa_gra = self.font25.render('Nowa gra', True, (255, 255, 255))
        cofnij = self.font25.render('Cofnij', True, (255, 255, 255))
        remis = self.font22.render('Remis?', True, (255, 255, 255))

        self.okno.blit(runda, (865, 385))

        if mode is None:
            pygame.draw.rect(self.okno, (150, 75, 0), self.przycisk_poddaj_sie)
            pygame.draw.rect(self.okno, (150, 75, 0), self.przycisk_nowa_gra)
            pygame.draw.rect(self.okno, (150, 75, 0), self.przycisk_cofnij)
            pygame.draw.rect(self.okno, (150, 75, 0), self.przycisk_remis)

            self.okno.blit(poddaj_sie, (810, self.przycisk_poddaj_sie.y + 5))
            self.okno.blit(remis, (835, self.przycisk_remis.y + 5))
            self.okno.blit(nowa_gra, (815, 440))
            self.okno.blit(cofnij, (830, 340))

    def rysowanie_szachownicy(self):
        for i in range(64):
            if (i // 8) % 2:
                pygame.draw.rect(self.okno, (128*(i % 2) + 127,       128*(i % 2) + 127,       128*(i % 2) + 127),       (100*(i % 8), 100*(i // 8), 100, 100))
            else:
                pygame.draw.rect(self.okno, (128*((i + 1) % 2) + 127, 128*((i + 1) % 2) + 127, 128*((i + 1) % 2) + 127), (100*(i % 8), 100*(i // 8), 100, 100))

    def rysowanie_figur(self):
        if self.ostatni:
            pygame.draw.rect(self.okno, (0, 255, 0), (100*self.ostatni[0][0], 100*self.ostatni[0][1], 100, 100))
            pygame.draw.rect(self.okno, (0, 255, 0), (100*self.ostatni[1][0], 100*self.ostatni[1][1], 100, 100))

        if self.kliknieta:
            pygame.draw.rect(self.okno, (0, 0, 255), (100*self.kliknieta[0], 100*self.kliknieta[1], 100, 100))

            for ruch in self.mozliwe_ruchy(self.pola[self.kliknieta], False, self.kliknieta):
                temp = [self.pola[self.kliknieta]]
                if ruch in self.pola:
                    temp.append(self.pola[ruch])

                self.pola[ruch] = temp[0]
                del self.pola[self.kliknieta]

                if not self.szach():
                    pygame.draw.rect(self.okno, (255, 255, 0), (100*ruch[0], 100*ruch[1], 100, 100))

                self.pola[self.kliknieta] = temp[0]
                if len(temp) == 2:
                    self.pola[ruch] = temp[1]
                else:
                    del self.pola[ruch]

        for pole in self.pola:
            self.okno.blit(self.font100.render(self.symbol[self.pola[pole]], True, (0, 0, 0)), (100*pole[0] + 20, 100*pole[1] - 20))

    def rysowanie_zbitych(self):
        wszystkie_figury = self.wszystkie_figury[0][:]

        for pole in self.pola:
            if self.pola[pole] not in ('k', 'K'):
                wszystkie_figury.remove(self.pola[pole])

        pozycja_upper = 0
        pozycja_lower = 0
        for zbita in wszystkie_figury:
            if zbita.isupper():
                self.okno.blit(self.font50.render(self.symbol[zbita], True, (0, 0, 0)), (800 + 40*(pozycja_upper // 200), 110 + pozycja_upper % 200))
                pozycja_upper += 40
            else:
                self.okno.blit(self.font50.render(self.symbol[zbita], True, (0, 0, 0)), (800 + 40*(pozycja_lower // 200), 460 + pozycja_lower % 200))
                pozycja_lower += 40

    def rysowanie(self, mode=None):
        self.rysowanie_szachownicy()
        self.rysowanie_panelu(mode)
        self.rysowanie_zbitych()
        self.rysowanie_figur()
        pygame.display.update()

    def kliknieto_w_odpowiednia_figure(self, pos):
        for pole in self.pola:
            if (100*pole[0] <= pos[0] <= 100*(pole[0] + 1) and 100*pole[1] <= pos[1] <= 100*(pole[1] + 1)) and ((self.pola[pole].isupper() and self.tura % 2 == 1) or (self.pola[pole].islower() and self.tura % 2 == 0)):
                self.kliknieta = pole
                return

    def przemieszczenie_figury(self, new):
        new = (new[0] // 100, new[1] // 100)
        kliknieta = self.kliknieta

        if new in self.mozliwe_ruchy(self.pola[kliknieta], False):
            flag_1 = True

            ruszono_o_2 = None
            if self.ruszono_o_2:
                ruszono_o_2 = self.ruszono_o_2
            self.ruszono_o_2 = None

            poped = None
            if new not in self.pola.keys():
                poped_przelot = (None, None)

                if self.pola[kliknieta] in ('p', 'P') and abs(kliknieta[1] - new[1]) == 2:
                    self.ruszono_o_2 = new

                temp = self.ostatni
                self.ostatni = (kliknieta, new)

                self.pola[new] = self.pola[kliknieta]
                if new[0] != kliknieta[0] and self.pola[kliknieta] in ('p', 'P'):
                    poped_przelot = (self.pola.pop((new[0], 2*(self.tura % 2) + new[1] - 1), None), (new[0], 2*(self.tura % 2) + new[1] - 1))
                poped = self.pola.pop(kliknieta, None)

                if self.szach():
                    del self.pola[new]
                    self.ostatni = temp
                    self.pola[kliknieta] = poped

                    if poped_przelot[0]:
                        self.pola[(new[0], 2*(self.tura % 2) + new[1] - 1)] = poped_przelot[0]
                    if ruszono_o_2:
                        self.ruszono_o_2 = ruszono_o_2
                    return False

                else:
                    self.poprzednie_ruchy.append([kliknieta, new, poped, (poped_przelot[0], poped_przelot[1], temp), None, ruszono_o_2])
                    flag_1 = False

                helper = {('K', -2): (0, 1, 0, (3, 7), (0, 7), (2, 7), 'W'), ('K', 2): (0, 2, 0, (5, 7), (7, 7), (6, 7), 'W'), ('k', -2): (3, 4, 3, (3, 0), (0, 0), (2, 0), 'w'), ('k', 2): (3, 5, 3, (5, 0), (7, 0), (6, 0), 'w')}
                help = (poped, new[0] - kliknieta[0])
                if help in helper:
                    self.krolowie_i_wieze[helper[help][0]] = helper[help][5]
                    self.krolowie_i_wieze[helper[help][1]] = helper[help][3]
                    self.mozliwosci_roszady[helper[help][2]] = 1
                    self.pola[helper[help][3]] = helper[help][6]
                    del self.pola[helper[help][4]]

                    self.poprzednie_ruchy[-1][4] = [helper[help][0], helper[help][1], helper[help][4], helper[help][3], helper[help][6]]

            else:
                temp = (self.ostatni, self.pola[new])
                self.ostatni = (kliknieta, new)

                self.pola[new] = self.pola[kliknieta]
                poped = self.pola.pop(kliknieta, None)

                if self.szach():
                    del self.pola[new]
                    self.ostatni = temp[0]
                    self.pola[new] = temp[1]
                    self.pola[kliknieta] = poped

                    if ruszono_o_2:
                        self.ruszono_o_2 = ruszono_o_2
                    return False

                else:
                    self.poprzednie_ruchy.append([kliknieta, new, poped, (temp[1], None, temp[0]), None, None, ruszono_o_2])

            if poped in ('k', 'K', 'w', 'W'):
                for i, figura in enumerate(self.krolowie_i_wieze):
                    if figura == kliknieta:
                        self.mozliwosci_roszady[i] += 1
                        self.krolowie_i_wieze[i] = new

                        self.poprzednie_ruchy[-1][-2] = [i]
                        break

            self.kliknieta = None
            self.promocja()
            return True

        self.kliknieta = None
        self.promocja()
        return False

    def mozliwe_ruchy_wiezy(self, x, y, ruchy, tryb):
        elements_1 = [0, 0, 1, 1, 7, 0, 7, 0]
        elements_2 = [0, -1, 0, 1, 1, -1, 1, 1]
        elements_3 = [0, 3, 0, 3, 2, 1, 2, 1]
        figura = self.pola[(x, y)]

        for i in range(4):
            x1, y1 = x, y
            helper = [x1, y1, x, y]

            while True:
                helper[elements_2[2*i]] += elements_2[2*i + 1]

                if not 0 <= helper[elements_1[i]] <= 7:
                    break

                ruchy.append((helper[elements_3[2*i]], helper[elements_3[2*i + 1]]))
                if (helper[elements_3[2*i]], helper[elements_3[2*i + 1]]) in self.pola:
                    help = (helper[elements_3[2*i]], helper[elements_3[2*i + 1]])

                    if (self.pola[help].islower() and figura.islower()) or (self.pola[help].isupper() and figura.isupper()):
                        ruchy.pop()

                    if tryb and self.pola[help] in ('k', 'K'):
                        continue

                    break

    def mozliwe_ruchy_gonca(self, x, y, ruchy, tryb):
        elements = [7, 7, 0, 0, 7, 0, 0, 7, -1, -1, 1, 1, -1, 1, 1, -1]
        figura = self.pola[(x, y)]

        for i in range(4):
            x1, y1 = x, y

            while True:
                x1 += elements[2*i + 8]
                y1 += elements[2*i + 9]

                if not 0 <= x1 <= 7 or not 0 <= y1 <= 7:
                    break

                ruchy.append((x1, y1))
                if (x1, y1) in self.pola:
                    if (self.pola[(x1, y1)].islower() and figura.islower()) or (self.pola[(x1, y1)].isupper() and figura.isupper()):
                        ruchy.pop()

                    if tryb and self.pola[(x1, y1)] in ('k', 'K'):
                        continue

                    break

    def mozliwe_ruchy_krola(self, krol):
        x, y = krol
        ruchy = ((x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y))
        return [ruch for ruch in ruchy if 0 <= ruch[0] <= 7 and 0 <= ruch[1] <= 7 and (ruch not in self.pola or ((self.pola[ruch].islower() and self.pola[krol] == 'K') or (self.pola[ruch].isupper() and self.pola[krol] == 'k')))]

    def mozliwe_ruchy(self, figura, tryb=True, kliknieta=None):
        if kliknieta is None:
            kliknieta = self.kliknieta

        x, y = kliknieta
        ruchy = []

        if figura in ('p', 'P'):
            helper = {'p': (1, 1, 2, 3), 'P': (-1, 6, 5, 4)}

            if (x, y + helper[figura][0]) not in self.pola:
                ruchy.append((x, y + helper[figura][0]))
            if y == helper[figura][1] and (x, helper[figura][2]) not in self.pola and (x, helper[figura][3]) not in self.pola:
                ruchy.append((x, helper[figura][3]))
            if (x-1, y + helper[figura][0]) in self.pola:

                help = {'p': self.pola[(x-1, y + helper[figura][0])].isupper(), 'P': self.pola[(x-1, y + helper[figura][0])].islower()}
                if help[figura]:
                    ruchy.append((x-1, y + helper[figura][0]))

            if (x+1, y + helper[figura][0]) in self.pola:

                help = {'p': self.pola[(x+1, y + helper[figura][0])].isupper(), 'P': self.pola[(x+1, y + helper[figura][0])].islower()}
                if help[figura]:
                    ruchy.append((x+1, y + helper[figura][0]))

            if self.ruszono_o_2 and y == self.ruszono_o_2[1] and (x == self.ruszono_o_2[0] + 1 or x == self.ruszono_o_2[0] - 1):
                ruchy.append((self.ruszono_o_2[0], self.ruszono_o_2[1] + helper[figura][0]))

            return ruchy

        elif figura == 'w' or figura == 'W':
            self.mozliwe_ruchy_wiezy(x, y, ruchy, tryb)
            return ruchy

        elif figura == 's' or figura == 'S':
            ruchy = ((x-2, y-1), (x-1, y-2), (x+1, y-2), (x+2, y-1), (x+2, y+1), (x+1, y+2), (x-1, y+2), (x-2, y+1))
            return [ruch for ruch in ruchy if 0 <= ruch[0] <= 7 and 0 <= ruch[1] <= 7 and (ruch not in self.pola or ((self.pola[ruch].islower() and figura == 'S') or (self.pola[ruch].isupper() and figura == 's')))]

        elif figura == 'g' or figura == 'G':
            self.mozliwe_ruchy_gonca(x, y, ruchy, tryb)
            return ruchy

        elif figura == 'h' or figura == 'H':
            self.mozliwe_ruchy_wiezy(x, y, ruchy, tryb)
            self.mozliwe_ruchy_gonca(x, y, ruchy, tryb)
            return ruchy

        else:
            elements = ['k', 'K', 'w', 'W']
            ruchy = self.mozliwe_ruchy_krola(kliknieta)
            free = True

            for i in range(2):
                if figura == elements[i] and self.mozliwosci_roszady[3 - 3*i] == 0:
                    for j in range(2):
                        if self.mozliwosci_roszady[4 - 3*i + j] == 0:
                            for k in range(2 - 2*j, 5 - 3*j):
                                if not free:
                                    break

                                for przeciwnik in self.pola:
                                    tura = (self.pola[przeciwnik].isupper(), self.pola[przeciwnik].islower())

                                    if tura[i] and ((self.pola[przeciwnik] != 'k' and (k + 4*j, 7*i) in self.mozliwe_ruchy(self.pola[przeciwnik], kliknieta=przeciwnik)) or (self.pola[przeciwnik] == 'k' and (k + 4*j, 7*i) in self.mozliwe_ruchy_krola(przeciwnik))):
                                        free = False
                                        break

                                if k % (4 - j) and (k + 4*j, 7*i) in self.pola:
                                    free = False
                                    break

                            if free and (7*j, 7*i) in self.pola and self.pola[(7*j, 7*i)] == elements[i + 2] and self.krolowie_i_wieze[5 - 3*i - j] != (7*j, 7*i):
                                ruchy.append((2 + 4*j, 7*i))
                            free = True

            return ruchy

    def szach(self, mode=None):
        if mode is None:
            self.atakuja = []
        else:
            atakuja = []

        tura = ('k', 'K')
        krol = [pole for pole in self.pola if self.pola[pole] == tura[self.tura % 2]][0]

        for przeciwnik in self.pola:
            tura_2 = (self.pola[przeciwnik].isupper(), self.pola[przeciwnik].islower())

            if tura_2[self.tura % 2]:
                if krol in self.mozliwe_ruchy(self.pola[przeciwnik], False, kliknieta=przeciwnik):
                    if mode is None:
                        self.atakuja.append(przeciwnik)
                    else:
                        atakuja.append(przeciwnik)

        if (mode is None and self.atakuja) or (mode and atakuja):
            return True
        return False

    def promocja(self):
        if self.ostatni is None:
            return

        if self.pola[self.ostatni[1]] == 'p' and self.ostatni[1][1] == 7:
            figures = ('s', 'g', 'w', 'h', 'p')
        elif self.pola[self.ostatni[1]] == 'P' and self.ostatni[1][1] == 0:
            figures = ('S', 'G', 'W', 'H', 'P')
        else:
            return

        pygame.draw.rect(self.okno, (255, 255, 0), (200, 350, 400, 100))
        for i in range(4):
            self.okno.blit(self.font100.render(self.symbol[figures[i]], True, (0, 0, 0)), (100*i + 220, 340))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    for i in range(4):
                        if 100*i + 200 <= pos[0] <= 100*i + 300 and 350 <= pos[1] <= 450:
                            self.pola[self.ostatni[1]] = figures[i]
                            self.wszystkie_figury[0].remove(figures[4])

                            for j, figura in enumerate(self.wszystkie_figury[0]):
                                if figura == figures[i]:
                                    self.wszystkie_figury[0].insert(j, figures[i])
                                    self.wszystkie_figury[1].append([self.tura, figures[4], figures[i]])
                                    return

                elif event.type == pygame.QUIT:
                    quit()

    def blokada(self):
        self.krol = self.krolowie_i_wieze[3*((self.tura + 1) % 2)]
        tura = ('a', 'A')

        for ruch in self.mozliwe_ruchy_krola(self.krol):
            if ruch in self.pola:
                tura_2 = (self.pola[ruch].islower(), self.pola[ruch].isupper())

                if tura_2[self.tura % 2]:
                    continue

            else:
                atakuje = False
                self.pola[ruch] = tura[self.tura % 2]

                for przeciwnik in self.pola:
                    tura_3 = (self.pola[przeciwnik].isupper(), self.pola[przeciwnik].islower())

                    if tura_3[self.tura % 2]:
                        if ruch in self.mozliwe_ruchy(self.pola[przeciwnik], kliknieta=przeciwnik):
                            atakuje = True

                if self.pola[ruch] == tura[self.tura % 2]:
                    del self.pola[ruch]

                if not atakuje:
                    return False

        return True

    def mat(self):
        ruchy_do_obrony = []

        if len(self.atakuja) == 2:
            return True

        for sojusznik in self.pola:
            tura_2 = (self.pola[sojusznik].islower(), self.pola[sojusznik].isupper())

            if tura_2[self.tura % 2]:
                if self.atakuja[0] in self.mozliwe_ruchy(self.pola[sojusznik], kliknieta=sojusznik):
                    poped = (self.pola.pop(sojusznik), self.pola.pop(self.atakuja[0]))
                    self.pola[self.atakuja[0]] = poped[0]

                    if not self.szach(True):
                        self.pola[self.atakuja[0]] = poped[1]
                        self.pola[sojusznik] = poped[0]
                        self.kliknieta = None
                        return False

                    self.pola[self.atakuja[0]] = poped[1]
                    self.pola[sojusznik] = poped[0]

        if self.pola[self.atakuja[0]] in ('g', 'G', 'w', 'W', 'h', 'H'):
            if self.krol[0] == self.atakuja[0][0]:
                if self.krol[1] > self.atakuja[0][1]:
                    for i in range(self.atakuja[0][1] + 1, self.krol[1]):
                        ruchy_do_obrony.append((self.krol[0], i))
                else:
                    for i in range(self.krol[1] + 1, self.atakuja[0][1]):
                        ruchy_do_obrony.append((self.krol[0], i))

            elif self.krol[1] == self.atakuja[0][1]:
                if self.krol[0] > self.atakuja[0][0]:
                    for i in range(self.atakuja[0][0] + 1, self.krol[0]):
                        ruchy_do_obrony.append((i, self.krol[1]))
                else:
                    for i in range(self.krol[0] + 1, self.atakuja[0][0]):
                        ruchy_do_obrony.append((i, self.krol[1]))

            else:
                if self.krol[0] > self.atakuja[0][0] and self.krol[1] > self.atakuja[0][1]:
                    for i in range(self.krol[0] - self.atakuja[0][0] - 1):
                        ruchy_do_obrony.append((self.atakuja[0][0] + 1 + i, self.atakuja[0][1] + 1 + i))
                elif self.krol[0] > self.atakuja[0][0] and self.krol[1] < self.atakuja[0][1]:
                    for i in range(self.krol[0] - self.atakuja[0][0] - 1):
                        ruchy_do_obrony.append((self.atakuja[0][0] + 1 + i, self.atakuja[0][1] - 1 - i))
                elif self.krol[0] < self.atakuja[0][0] and self.krol[1] > self.atakuja[0][1]:
                    for i in range(self.atakuja[0][0] - self.krol[0] - 1):
                        ruchy_do_obrony.append((self.krol[0] + 1 + i, self.krol[1] - 1 - i))
                elif self.krol[0] < self.atakuja[0][0] and self.krol[1] < self.atakuja[0][1]:
                    for i in range(self.atakuja[0][0] - self.krol[0] - 1):
                        ruchy_do_obrony.append((self.krol[0] + 1 + i, self.krol[1] + 1 + i))

            for sojusznik in self.pola:
                tura_1 = ('k', 'K')
                tura_3 = (self.pola[sojusznik].islower(), self.pola[sojusznik].isupper())

                if self.pola[sojusznik] != tura_1[self.tura % 2] and tura_3[self.tura % 2]:
                    for ruch_do_obrony in ruchy_do_obrony:
                        if ruch_do_obrony in self.mozliwe_ruchy(self.pola[sojusznik], kliknieta=sojusznik):
                            poped = self.pola.pop(sojusznik)
                            self.pola[ruch_do_obrony] = poped

                            if not self.szach(True):
                                del self.pola[ruch_do_obrony]
                                self.pola[sojusznik] = poped
                                self.kliknieta = None
                                return False

                            del self.pola[ruch_do_obrony]
                            self.pola[sojusznik] = poped

        self.kliknieta = None
        return True

    def pat(self):
        tura = ('k', 'K')

        for sojusznik in self.pola:
            tura_2 = (self.pola[sojusznik].islower(), self.pola[sojusznik].isupper())

            if self.pola[sojusznik] != tura[self.tura % 2] and tura_2[self.tura % 2]:
                for ruch in self.mozliwe_ruchy(self.pola[sojusznik], kliknieta=sojusznik):
                    if ruch in self.pola and ((self.pola[ruch].islower() and tura_2[1]) or (self.pola[ruch].isupper() and tura_2[0])):
                        poped = (self.pola.pop(sojusznik), self.pola.pop(ruch))

                        if not self.szach(True):
                            self.pola[sojusznik] = poped[0]
                            self.pola[ruch] = poped[1]
                            self.kliknieta = None
                            return False

                        self.pola[sojusznik] = poped[0]
                        self.pola[ruch] = poped[1]

                    elif ruch not in self.pola:
                        poped = self.pola.pop(sojusznik)

                        if not self.szach(True):
                            self.pola[sojusznik] = poped
                            self.kliknieta = None
                            return False

                        self.pola[sojusznik] = poped

        self.kliknieta = None
        return True

    def cofanie(self):
        if self.tura >= 2:
            cofniecie = self.poprzednie_ruchy.pop()

            if cofniecie[-1]:
                self.ruszono_o_2 = cofniecie[-1]

            if len(cofniecie) == 6:
                self.pola[cofniecie[0]] = cofniecie[2]
                del self.pola[cofniecie[1]]

                if cofniecie[3][1]:
                    self.pola[cofniecie[3][1]] = cofniecie[3][0]

                if type(cofniecie[4]) == list and len(cofniecie[4]) == 5:
                    del self.pola[cofniecie[4][3]]
                    self.pola[cofniecie[4][2]] = cofniecie[4][-1]
                    self.krolowie_i_wieze[cofniecie[4][1]] = cofniecie[4][2]

            else:
                self.pola[cofniecie[0]] = cofniecie[2]
                self.pola[cofniecie[1]] = cofniecie[3][0]

            if type(cofniecie[-2]) == list:
                self.krolowie_i_wieze[cofniecie[-2][0]] = cofniecie[0]
                self.mozliwosci_roszady[cofniecie[-2][0]] -= 1

            self.ostatni = cofniecie[3][2]
            self.kliknieta = None
            self.tura -= 1

            if len(self.wszystkie_figury[1]) > 0 and self.tura == self.wszystkie_figury[1][-1][0]:
                cofniecie = self.wszystkie_figury[1].pop()
                self.wszystkie_figury[0].remove(cofniecie[2])

                for j, figura in enumerate(self.wszystkie_figury[0]):
                    if figura == cofniecie[1]:
                        self.wszystkie_figury[0].insert(j, cofniecie[1])
                        return

    def wygrana(self, mode=None):
        if mode:
            napis, dlugosc = 'Remis', 340
        elif self.tura % 2 == 1:
            napis, dlugosc = 'Wygrywają czarne', 210
        else:
            napis, dlugosc = 'Wygrywają białe', 220

        self.rysowanie('decyzja')
        pygame.draw.rect(self.okno, (0, 255, 0), pygame.Rect(200, 350, 400, 100))
        self.okno.blit(self.font40.render(napis, True, (255, 255, 255)), (dlugosc, 375))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    return

                elif event.type == pygame.QUIT:
                    quit()

    def decyzja(self):
        self.rysowanie('decyzja')

        self.przycisk_zgoda_remis.y = 80
        self.przycisk_gramy_dalej.y = 30
        self.przycisk_zgoda_remis.y += 600*((self.tura + 1) % 2)
        self.przycisk_gramy_dalej.y += 700*((self.tura + 1) % 2)

        pygame.draw.rect(self.okno, (150, 75, 0), self.przycisk_zgoda_remis)
        pygame.draw.rect(self.okno, (150, 75, 0), self.przycisk_gramy_dalej)
        self.okno.blit(self.font22.render('Gramy dalej', True, (255, 255, 255)), (805, self.przycisk_gramy_dalej.y + 5))
        self.okno.blit(self.font22.render('Remis', True, (255, 255, 255)), (840, self.przycisk_zgoda_remis.y + 5))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if self.przycisk_zgoda_remis.collidepoint(pos):
                        return True
                    elif self.przycisk_gramy_dalej.collidepoint(pos):
                        return False

                elif event.type == pygame.QUIT:
                    quit()


os.environ['SDL_VIDEO_WINDOW_POS'] = '300, 25'

pygame.display.set_mode()
pygame.display.set_caption('Szachy')
pygame.font.init()

gra = Gra()

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if pos[0] >= 800:
                if gra.przycisk_cofnij.collidepoint(pos):
                    gra.cofanie()
                elif gra.przycisk_nowa_gra.collidepoint(pos):
                    gra = Gra()
                elif gra.przycisk_poddaj_sie.collidepoint(pos):
                    gra.wygrana()
                    gra = Gra()
                elif gra.przycisk_remis.collidepoint(pos):
                    if gra.decyzja():
                        gra.wygrana('pat')
                        gra = Gra()

            elif gra.kliknieta and gra.przemieszczenie_figury(pos):
                gra.tura += 1

                if gra.blokada():
                    szach = gra.szach()

                    if szach and gra.mat():
                        gra.wygrana()

                    elif not szach and gra.pat():
                        gra.wygrana('pat')

            else:
                gra.kliknieto_w_odpowiednia_figure(pos)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            gra.kliknieta = None
        elif event.type == pygame.QUIT:
            quit()

    gra.rysowanie()
