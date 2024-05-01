"""Top-level package for pytrials."""

from pathlib import Path

__author__ = """João Vitor F. Cavalcante"""
__email__ = "jvfe@ufrn.edu.br"
__version__ = "0.3.0"

HERE = Path(__file__).parent.resolve()

study_fields = Path(HERE, "fields.csv")
