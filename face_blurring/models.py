from dataclasses import dataclass


@dataclass
class ProblemJsonResponse:
    type: str
    title: str
    status: int
    detail: str
