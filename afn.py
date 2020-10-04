# Denise Keiko Ferreira Adati - 10430962
import argparse
import sys

if __name__ == '__main__':
    optparse = argparse.ArgumentParser(
        description="Verifica se uma cadeia faz parte da linguagem de um automato AFN.")
    optparse.add_argument("-i", help="Caminho do arquivo de entrada", type=str, required=True)
    optparse.add_argument("-o", help="Caminho do arquivo de saída", type=str, required=True)

args = optparse.parse_args(sys.argv[1:])  # extrair os argumentos

qtdAutomatos = 0

class Automato():
    def __init__(self, estados, simbolos, transicoes, inicial, estadosFinais, casos):
        self.estados = estados
        self.simbolos = simbolos
        self.transicoes = transicoes  # transicoes[estadoAtual]
        self.inicial = inicial
        self.estadosFinais = estadosFinais
        self.casos = casos

class No:
    def __init__(self, simbolo=None, estadoSucessor=None, proximo=None):
        self.simbolo = simbolo
        self.estadoSucessor = estadoSucessor
        self.proximo = proximo

def encontraSucessorRecursivo(transicoes, estado, simbolo, visitados):
    nodeTrans = transicoes[estado]
    resp = []
    while nodeTrans:
        if nodeTrans.simbolo == simbolo:
            sucessor = nodeTrans.estadoSucessor
            if not visitados[sucessor]:
                visitados[sucessor] = True
                resp.append(sucessor)
                resp += encontraSucessorRecursivo(transicoes, sucessor, 0, visitados)
        nodeTrans = nodeTrans.proximo
    return resp

def cadeiaEhReconhecida(automato, cadeia):  # cadeia - lista de números que representa a cadeia
    atuaisEstados = [automato.inicial]
    visitados = [False] * 5
    atuaisEstados = encontraSucessorRecursivo(automato.transicoes,automato.inicial,0,visitados)
    atuaisEstados.append(automato.inicial)
    while len(cadeia) > 0:
        if cadeia[0] == 0:
            break
        visitados = [False] * 5
        proxEstados = []
        simbolo = cadeia.pop(0)

        for estado in atuaisEstados:
            proxEstados += encontraSucessorRecursivo(automato.transicoes,estado,simbolo,visitados)
        proxEstados = list(dict.fromkeys(proxEstados))
        atuaisEstados = proxEstados
    for estado in automato.estadosFinais:
        if estado in atuaisEstados:
            return True
    return False


def testaCasos(automato):  # testa todos os casos de um automato
    linha = []
    # with open(args.o,'a') as out:
    for caso in automato.casos:
        linha.append(str(int(cadeiaEhReconhecida(automato, caso))))
        linha.append(" ")
    linha.pop(-1)
    linha = "".join(linha)
    return linha


def escreveSaida(listaAutomatos):
    breakLine = "\n"
    f = open(args.o, "a")
    f.truncate(0)
    for i in range(len(listaAutomatos)):
        f.write(testaCasos(listaAutomatos[i]))
        if i != qtdAutomatos - 1:
            f.write(breakLine)
    f.close()

def lerArquivo():
    retorno = []
    arquivoTeste = open(args.i, 'r')
    qtdAutomatos = int(arquivoTeste.readline())
    for i in range(qtdAutomatos):
        automato = []
        Casos = []
        qtdCasos = 0
        linha = arquivoTeste.readline()
        automato = list(map(int, linha.split(" ")))
        automatoAtual = Automato(automato[0], automato[1], None, automato[3], None, None)

        qtdAceitacao = automato[4]
        linhaEstadosAceitacao = arquivoTeste.readline()
        if(qtdAceitacao > 0):
            automatoAtual.estadosFinais = list(map(int, linhaEstadosAceitacao.split(" ")))
        else:
            automatoAtual.estadosFinais = []

        qtdTransicao = automato[2]
        listaTransicaoAux = [None] * automatoAtual.estados
        for j in range(qtdTransicao):
            linha = arquivoTeste.readline()
            transAux = list(map(int, linha.split(" ")))
            atual = transAux[0]
            simbolo = transAux[1]
            destino = transAux[2]
            no = No(simbolo, destino)
            if listaTransicaoAux[atual] == None:
                listaTransicaoAux[atual] = no
            else:
                pivo = listaTransicaoAux[atual]
                while pivo:
                    if pivo.proximo == None:
                        pivo.proximo = no
                        break
                    else:
                        pivo = pivo.proximo
        automatoAtual.transicoes = listaTransicaoAux
        qtdCasos = int(arquivoTeste.readline())
        for caso in range(qtdCasos):
            linha = arquivoTeste.readline()
            Casos.append(list(map(int, linha.split(" "))))
        automatoAtual.casos = Casos
        retorno.append(automatoAtual)
    arquivoTeste.close()
    return retorno


listaAutomatos = lerArquivo()
escreveSaida(listaAutomatos)