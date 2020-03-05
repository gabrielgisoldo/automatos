# -*- coding: utf-8 -*-
from Automata import AutomataFunction, AutomataGoTo
import os


class AutomataGenerator(object):
    """."""

    def __init__(self):
        """."""
        self.qty_symbols = 0
        self.symbols = []
        self.qty_est = 0
        self.states = {}
        self.initial = 0
        self.qty_finals = 0
        self.finals = []
        self.adjacency = {}
        self.file_name = ''
        self.type = 1
        self.automata = None

    def _header(self):
        """Make basic C++ header."""
        s = ["#include <iostream>", "#include <string>", "#include <stdio.h>",
             "", "using namespace std;", "", "string tape;", "int index = 0;",
             "", ""]

        return '\n'.join(s)

    def make_file(self):
        """Make .cpp file with the automata."""
        if self.type == 1:
            self.automata = AutomataFunction(
                qty_est=self.qty_est, states=self.states,
                initial=self.initial, adjacency=self.adjacency,
                finals=self.finals)
        else:
            self.automata = AutomataGoTo(
                qty_est=self.qty_est, states=self.states,
                initial=self.initial, adjacency=self.adjacency,
                finals=self.finals)

        output = self._header() + self.automata.make()

        if not os.path.exists('output'):
            os.makedirs('output')

        with open('output/' + self.file_name, 'w') as f:
            f.write(output)
            f.close()

        input("Arquivo gerado...")

    def menu(self):
        """."""
        print("Gerador de autômatos\n\n")

        self.qty_symbols = int(input("Quantidade de simbolos: ").strip())
        for i in range(self.qty_symbols):
            self.symbols.append(input("Informe o simbolo Nº%s: " % i))

        self.qty_est = int(input("Quantidade de estados: ").strip())

        self.states = {"accept": "ACCEPT"}
        for item in range(0, self.qty_est):
            tmp = input("Qual o nome do estado Nº%s: " % item).strip()
            self.states[item] = tmp

        self.initial = int(
            input(
                "Qual o estado inicial? (Entre 0 e %s): " % (self.qty_est - 1)
            ).strip()
        )

        if self.initial > (self.qty_est - 1):
            raise Exception('Estado inicial inválido')

        self.qty_finals = int(input("Quantos estados finais: ").strip())

        for i in range(self.qty_finals):
            self.finals.append(
                input((("Qual o estado final Nº%s? (entre 0 e %s): ") %
                       (i, self.qty_est - 1))).strip()
            )

        self.finals = [int(i) for i in self.finals
                       if int(i) <= (self.qty_est - 1)]

        for item in range(0, self.qty_est):
            s = "Para o estado %s, qual o próximo estado para os " +\
                "simbolos %s (Separados por espaço, entre -1 e %s): "
            tmp = input(s % (self.states[item], ', '.join(self.symbols),
                             (self.qty_est - 1))).strip().split(' ')
            if len(tmp) > len(self.symbols):
                tmp = tmp[:len(self.symbols)]

            tmp = [int(i) for i in tmp]

            self.adjacency[item] = list(zip(self.symbols, tmp))

        name = input('Nome do arquivo (automato): ').strip()
        self.file_name = (name and name or 'automato').split('.')[0] + '.cpp'

        self.type = int(
            input("1 - Function\n2 - GOTO\nSelecione o tipo: ")
        )

        if self.type not in (1, 2):
            self.type = 1
            print('Tipo inválido. Gerando com funções\n\n')

generator = AutomataGenerator()

generator.menu()
generator.make_file()
