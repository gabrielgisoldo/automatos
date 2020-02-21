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
        self.nome_arq = 'automato.cpp'

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


automato = Automato()

automato.menu()

print(vars(automato))
