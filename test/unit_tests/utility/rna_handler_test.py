""" rna_handler_test.py """
import os
from Bio.SeqRecord import SeqRecord
from mofiwo.utility import load_rna_fasta_zipfile, generate_utr_from_cdna_cds

zipfile_cds = r'test/data/s1_cds.zip'
zipfile_cdna = r'test/data/s1_cdna.zip'

def test_load_rna_fasta_zipfile():
    """ test rna zip file loading """

    dic_cds = load_rna_fasta_zipfile(zipfile_cds)
    dic_cdna = load_rna_fasta_zipfile(zipfile_cdna)

    assert isinstance(dic_cds, dict)
    assert isinstance(dic_cdna, dict)

def test_generate_utr_from_cdna_cds():
    """ test generate utr from cdna cds sequence """
   
    dic_cds = load_rna_fasta_zipfile(zipfile_cds)
    dic_cdna = load_rna_fasta_zipfile(zipfile_cdna)
    dic_utr = generate_utr_from_cdna_cds(dic_cdna, dic_cds)
    key, val = dic_utr.popitem()

    assert isinstance(key, str)
    assert 'utr3' in val.keys()
    assert isinstance(val['utr5'], SeqRecord)