"""Ensembl.py test"""
from mofiwo.connector.ensembl import read_ensembl

def test_read_ensembl():
    _ret = read_ensembl('ENSMUST00000037811', req_param={'type':'cds'})
    assert True