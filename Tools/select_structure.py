import re

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Tools.automaton import Compiler

class SelectStructure():
    def __init__(self, temporal_code: list[str], compiler):
        self.temporal_code: list[str] = temporal_code
        self.compiler: Compiler = compiler