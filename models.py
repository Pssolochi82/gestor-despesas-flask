from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Despesa:
    data: date
    descricao: str
    categoria: str
    valor: float

    def as_dict(self) -> dict:
        return {
            "data": self.data.isoformat(),
            "descricao": self.descricao,
            "categoria": self.categoria,
            "valor": float(self.valor),
        }
