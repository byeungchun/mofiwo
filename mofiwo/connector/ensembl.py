"""This module contains Ensembl API service hanlder service."""
from mofiwo.config import SETTINGS

def read_ensembl():
    print(SETTINGS.ensembl_url)
