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

    def _indent(self, texto):
        """."""
        return texto.replace('<sp>', '    ')

    def _gerar_if(self, vetor, nivel=1):
        if not vetor:
            return ""
        if len(vetor) == 1:
            item = vetor.pop()
            nf = self.estados[item[1]]

            if isinstance(item[0], int):
                aux = (("<sp>if(fita[index] == %s){\n<spp>index++;\n<spp>" +
                        "%s();\n<sp>}else{\n<spp>REJEITA();\n<sp>}") % (
                    item[0], nf))
            else:
                aux = (("<sp>if(fita[index] == '%s'){\n<spp>index++;\n<spp>" +
                        "%s();\n<sp>}else{\n<spp>REJEITA();\n<sp>}") % (
                    item[0], nf))

            return aux.replace('<sp>', '    ' * nivel).\
                replace('<spp>', '    ' * (nivel + 1))
        else:
            item = vetor.pop()
            r = self._gerar_if(vetor, (nivel + 1))
            nf = self.estados[item[1]]

            if isinstance(item[0], int):
                aux = (("<sp>if(fita[index] == %s){\n<spp>index++;\n<spp>" +
                        "%s();\n<sp>}else{\n%s\n<sp>}") % (
                    item[0], nf, r))
            else:
                aux = (("<sp>if(fita[index] == '%s'){\n<spp>index++;\n<spp>" +
                        "%s();\n<sp>}else{\n%s\n<sp>}") % (
                    item[0], nf, r))

            return aux.replace('<sp>', '    ' * nivel).\
                replace('<spp>', '    ' * (nivel + 1))

    def header(self):
        """Gera o header basico de um programa em c++."""
        s = ["#include <iostream>", "#include <string>", "",
             "using namespace std;", "", "string fita;", "int index = 0;"]

        return '\n'.join(s)

    def proto_func(self):
        """."""
        s = ["void ACEITA();", "void REJEITA();"]
        for item in range(0, self.qtd_est):
            s.append('void %s();' % self.estados[item])

        return '\n'.join(s)

    def mk_default_func(self):
        """."""
        aceita = """void ACEITA(){\n<sp>cout << "ACEITA";\n}"""
        rejeita = """void REJEITA(){\n<sp>cout << "REJEITA";\n}"""
        main = (
            ("int main() {\n<sp>getline(cin, fita);\n<sp>%s" +
             "();\n<sp>cin.get();\n<sp>return 0;\n}") % (
                self.estados[self.inicial]))

        return '\n'.join((aceita, rejeita, main))

    def funcoes(self):
        """."""
        ret = []
        base = 'void %s(){\n%s\n}'
        for i in range(self.qtd_est):
            tmp = [item for item in self.adjacencia[i] if item[1] > -1]
            if i in self.finais:
                tmp.append((0, 'aceita'))
            ret.append(base % (self.estados[i], self._gerar_if(vetor=tmp)))

        return '\n'.join(ret)

    def menu(self):
        """."""
        print("Gerador de autômatos\n\n")

        self.simbolos = input(
            "Quais os simbolos da linguagem?(separados por espaço): "
        ).strip().split(' ')
        self.qtd_est = int(input("Quantidade de estados: ").strip())
        self.estados = {"aceita": "ACEITA"}
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

        print(self._indent(self.header()))
        print(self._indent(self.proto_func()))
        print(self._indent(self.funcoes()))
        print(self._indent(self.mk_default_func()))


automato = Automato()

automato.menu()

print(vars(automato))
