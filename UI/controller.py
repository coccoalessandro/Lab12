import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []
        self._grafo = nx.Graph()

    def fillDD(self):
        self._listCountry = self._model.getCountries()
        for c in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))

        self._listYear = [2015, 2016, 2017, 2018]
        for y in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(str(y)))

        self._view.update_page()


    def handle_graph(self, e):
        country = self._view.ddcountry.value
        year = int(self._view.ddyear.value)
        self._grafo.clear()
        self._grafo = self._model.buildGraph(year, country)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di veritici: {len(self._model._graph.nodes)} nodi \nNumero di archi: {len(self._model._graph.edges)}"))

        self._view.update_page()


    def handle_volume(self, e):

        dizionario = self._model.volumeVendita()

        self._view.txtOut2.controls.clear()

        for r in dizionario:
            self._view.txtOut2.controls.append(ft.Text(f"{r[0].Retailer_name} --> {r[1]}"))

        self._view.update_page()


    def handle_path(self, e):
        n = int(self._view.txtN.value)
        self._view.txtOut3.controls.clear()

        sol, peso = self._model.percorsoOttimo(n)
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {peso}"))
        for i in range(len(sol)-1):
            self._view.txtOut3.controls.append(ft.Text(f"{sol[i].Retailer_name} --> {sol[i+1].Retailer_name}: {self._model._graph[sol[i]][sol[i+1]]['weight']}"))

        self._view.update_page()
