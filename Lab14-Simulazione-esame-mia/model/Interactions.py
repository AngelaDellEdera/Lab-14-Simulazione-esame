from dataclasses import dataclass
@dataclass
class Interaction:
    GeneID1:str
    GeneID2:str
    Type:str
    Expression_Corr:float

    def __str__(self):
        return f'{self.GeneID1}---{self.GeneID2} '
    def __hash__(self):
        return hash(self.GeneID1) + hash(self.GeneID2)