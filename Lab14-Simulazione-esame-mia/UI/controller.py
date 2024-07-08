import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici:{self._model.get_num_of_nodes()}  Numero di archi:{self._model.get_num_of_edges()}"))
        self._view.txt_result.controls.append(ft.Text(f"Informazioni sui pesi degli archi-val minimo{self._model.get_min_weight()}    -val massimo {self._model.get_max_weight()}"))
        self._view.update_page()
    def handle_countedges(self, e):
        soglia=float(self._view.txt_name.value)
        if soglia>self._model.get_max_weight() or soglia<self._model.get_min_weight():
            self._view.txt_result2.controls.append(ft.Text(f"Valore soglia non valido!"))
            return
        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi con peso maggiore della soglia:{self._model.count_bigger(soglia)}"))
        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi con peso minore della soglia:{self._model.count_smaller(soglia)}"))
        self._view.update_page()


    def handle_search(self, e):
        soglia = float(self._view.txt_name.value)
        if soglia > self._model.get_max_weight() or soglia < self._model.get_min_weight():
            self._view.txt_result2.controls.append(ft.Text(f"Valore soglia non valido!"))
            return
        self._model.get_path(soglia)
        self._view.txt_result3.controls.append(ft.Text(f"Peso cammino massimo:{self._model.computeWeightPath(self._model.solBest)}"))
        for i in self._model.solBest:
            self._view.txt_result3.controls.append(ft.Text(f"{i[0]}----> {i[1]}:{i[2]['weight']}"))

        self._view.update_page()