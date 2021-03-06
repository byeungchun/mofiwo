"""This module contains RNA sequence processing functions"""

import os

from Bio import SeqIO
from zipfile import ZipFile


def load_rna_fasta_zipfile(
    fasta_zipfile: str
) -> dict:
    """Read fasta format RNA sequence using BioPython libarary and save to dictionary.
    Zipfile should contain one fasta file

    Args:
        fasta_file: fasta file location
    Returns:
            dict: key-value pair
    """

    dir_name = os.path.dirname(fasta_zipfile)
    fasta_file = os.path.basename(fasta_zipfile).replace('.zip', '.fasta')

    with ZipFile(fasta_zipfile, 'r') as zip_ref:
        zip_ref.extract(fasta_file, dir_name)

    dict_fasta = dict()
    with open(os.path.join(dir_name, fasta_file), 'r') as fin:
        for record in SeqIO.parse(fin, 'fasta'):
            dict_fasta[record.id] = record

    return dict_fasta


def generate_3utr_from_cdna_cds(
        dict_cdna: dict,
        dict_cds: dict,
) -> dict:
    """Generate 3UTR sequence using CDNA and CDS sequence. 
    CDNA contains the whole sequence of the RNA, including coding and untranslated sequence.
    CDS contains only coding sequence

    Args:
            dict_cdna: CDNA sequence dictionary. Sequence should be BioPython data type
            dict_cds: CDS sequence dictionary. Sequence should be BioPython data type
    Returns:
            dict: 3UTR dictionary
    """

    pass
