from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class EvaluatorResult:
    """
    Class to represent the evaluator result model
    """

    score: float


class Evaluator(ABC):
    @abstractmethod
    def __call__(self, **kwargs: Any) -> EvaluatorResult:
        pass
