#!/usr/bin/python3.7
# -*- coding: utf-8 -*-


class Automato(object):
    """."""

    def __init__(self):
        """."""
        self.simbolos = []
        self.qtd_est = 0
        self.estados = {}
        self.inicial = 0
        self.finais = []
        self.adjacencia = {}
        self.nome_arq = ''

    def header(self):
        """Gera o header basico de um programa em c++."""
        return "#include <iostream>\n#include <string>\n\n" +\
            "using namespace std;\n\nstring fita;\nint index = 0;"

    def proto_func(self):
        """."""
        s = []
        for item in range(0, self.qtd_est):
            s.append('void %s();' % self.estados[item])

        return '\n'.join(s)

    def mk_default_func(self):
        """."""
        aceita = """void ACEITA(){\n\tcout << "ACEITA";\n}"""
        rejeita = """void REJEITA(){\n\tcout << "REJEITA";\n}"""
        main = ("int main() {\n\tgetline(cin, fita);\n\t%s;\n}" % (
                self.estados[self.inicial]))

        return '\n'.join((aceita, rejeita, main))

    def menu(self):
        """."""
        print("Gerador de autômatos\n\n")

        self.simbolos = input(
            "Quais os simbolos da linguagem?(separados por espaço): "
        ).strip().split(' ')
        self.qtd_est = int(input("Quantidade de estados: ").strip())
        self.estados = {}
        for item in range(0, self.qtd_est):
            tmp = input("Qual o nome do estado %s: " % item).strip()
            self.estados[item] = tmp

        self.inicial = int(
            input(
                "Qual o estado inicial? (Entre 0 e %s): " % (self.qtd_est - 1)
            ).strip()
        )

        if self.inicial > (self.qtd_est - 1):
            raise Exception('Estado inicial inválido')

        self.finais = input(
            "Quais os estados finais? (Separados por espaço, entre " +
            "0 e %s): " % (self.qtd_est - 1)).strip().split(' ')

        self.finais = [int(i) for i in self.finais
                       if int(i) <= (self.qtd_est - 1)]

        for item in range(0, self.qtd_est):
            s = "Para o estado %s, qual o próximo estado para os " +\
                "simbolos %s: (Separados por espaço, entre -1 e %s)"
            tmp = input(s % (self.estados[item], ', '.join(self.simbolos),
                             (self.qtd_est - 1))).strip().split(' ')
            if len(tmp) > len(self.simbolos):
                tmp = tmp[:len(self.simbolos)]

            tmp = [int(i) for i in tmp]

            self.adjacencia[item] = list(zip(self.simbolos, tmp))

        nome = input('Nome do arquivo (automato): ').strip()
        self.nome_arq = (nome and nome or 'automato') + '.cpp'

        print(self.header())
        print(self.proto_func())
        print(self.mk_default_func())


automato = Automato()

automato.menu()

print(vars(automato))
