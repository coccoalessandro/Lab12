import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._retailers = []
        self._idMapRetailers = {}
        self._ottimo = []
        self._pesoMax = 0

    def getCountries(self):
        return DAO.getCountries()

    def buildGraph(self, year, country):
        self._retailers = DAO.getRetailers(country)
        self._graph.add_nodes_from(self._retailers)
        for retailer in self._retailers:
            self._idMapRetailers[retailer.Retailer_code] = retailer

        allEdges = DAO.getEdges(year, country, self._idMapRetailers)

        for edge in allEdges:
            self._graph.add_edge(edge[0], edge[1], weight=edge[2])


    def volumeVendita(self):
        dizVolumi = {}
        for r in self._retailers:
            for e in self._graph.edges(data=True):
                if r == e[0] or r == e[1]:
                    if r in dizVolumi.keys():
                        dizVolumi[r] += int(e[2]['weight'])
                    else:
                        dizVolumi[r] = int(e[2]['weight'])

        sortedDiz = sorted(dizVolumi.items(), key=lambda x: x[1], reverse=True)
        return sortedDiz

    def percorsoOttimo(self, n):
        self._pesoMax = 0
        self._ottimo = []
        parziale = []
        self._ricorsione(parziale, n)
        return self._ottimo, self._pesoMax

    def _ricorsione(self, parziale, n):
        if len(parziale) == (n+1):
            if self.calcolaPeso(parziale) > self._pesoMax:
                self._pesoMax = self.calcolaPeso(parziale)
                self._ottimo = copy.deepcopy(parziale)
        else:
            if len(parziale) == 0:
                for nodo in self._retailers:
                    parziale.append(nodo)
                    self._ricorsione(parziale, n)
                    parziale.pop()
            else:
                if len(parziale) < n:
                    for nodo in self._graph.neighbors(parziale[-1]):
                        if nodo not in parziale:
                            parziale.append(nodo)
                            self._ricorsione(parziale, n)
                            parziale.pop()

                elif len(parziale) == n:
                    if parziale[0] in self._graph.neighbors(parziale[-1]):
                        parziale.append(parziale[0])
                        self._ricorsione(parziale, n)
                        parziale.pop()


    def calcolaPeso(self, parziale):
        peso = 0

        for i in range(len(parziale)-1):
            if self._graph.has_edge(parziale[i], parziale[i+1]):
                peso += self._graph[parziale[i]][parziale[i+1]]['weight']

        return peso



