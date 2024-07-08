import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.DiGraph()
        self._nodes = []
        self._edges = []

        self.solBest = []
        self.idMap={}
        self._listGenes = []
        self._listChromosome=[]
        self._listConnGenes=[]

        self.loadChromosome()
        self.loadGenes()
        self.loadConnectedGenes()


    def get_path(self,soglia):
        for n in self.get_nodes():
            partial = []
            partial_edges = []
            partial.append(n)
            self.ricorsione(partial, partial_edges,soglia)
    def ricorsione(self,partial,partial_edges,soglia):
        n_last = partial[-1]

        neigh = self.getAdmissibleNeighbs(n_last, partial_edges,soglia)

        # stop
        if len(neigh) == 0:
            weight_path = self.computeWeightPath(partial_edges)
            weight_path_best = self.computeWeightPath(self.solBest)
            if weight_path > weight_path_best:
                self.solBest = partial_edges[:]
            return

        for n in neigh:
            partial_edges.append((n_last, n, self.graph.get_edge_data(n_last, n)))
            partial.append(n)

            self.ricorsione(partial, partial_edges,soglia)
            partial.pop()
            partial_edges.pop()

    def computeWeightPath(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]['weight']
        return weight

    def getAdmissibleNeighbs(self,n_last,partial_edges,soglia):
        vicini=self.graph.edges(n_last, data=True)
        result=[]
        for v in vicini:
            if v[2]['weight'] > soglia:
                v_inv=(v[1],v[0],v[2])
                if (v_inv not in partial_edges) and (v not in partial_edges):
                    result.append(v[1])
        return result

    def buildGraph(self):
        self.graph.clear()
        for c in self._listChromosome:
            self._nodes.append(c)
        self.graph.add_nodes_from(self._nodes)
        edges = {}
        for g1, g2, corr in self._listConnGenes:
            if (self.idMap[g1], self.idMap[g2]) not in edges:
                edges[(self.idMap[g1], self.idMap[g2])] = float(corr)
            else:
                edges[(self.idMap[g1], self.idMap[g2])] += float(corr)
        for k, v in edges.items():
            self._edges.append((k[0], k[1], v))
        self.graph.add_weighted_edges_from(self._edges)
    def count_bigger(self,soglia):
        count=0
        for e in self.get_edges():
            if e[2]['weight'] > soglia:
                count+=1
        return count

    def count_smaller(self,soglia):
        count=0
        for e in self.get_edges():
            if e[2]['weight'] < soglia:
                count += 1
        return count


    def get_min_weight(self):
        return min([x[2]['weight'] for x in self.get_edges()])

    def get_max_weight(self):
        return max([x[2]['weight'] for x in self.get_edges()])

    def loadConnectedGenes(self):
        self._listConnGenes=DAO.getAllConnectedGenes()
    def loadChromosome(self):
        self._listChromosome = DAO.getAllChromosomes()

    def loadGenes(self):
        self._listGenes = DAO.getAllGenes()
        for g in self._listGenes:
            self.idMap[g.GeneID] = g.Chromosome

    def get_nodes(self):
        return self.graph.nodes()

    def get_edges(self):
        return list(self.graph.edges(data=True))

    def get_num_of_nodes(self):
        return self.graph.number_of_nodes()

    def get_num_of_edges(self):
        return self.graph.number_of_edges()