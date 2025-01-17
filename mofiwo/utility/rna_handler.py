"""This module contains RNA sequence processing functions"""

import os

from Bio import SeqIO

from zipfile import ZipFile
from mofiwo import log
from mofiwo._helper import generate_utr_seq

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


def generate_utr_from_cdna_cds(
        dic_cdna: dict,
        dic_cds: dict,
) -> dict:
    """Generate UTR sequence using CDNA and CDS sequence. 
    CDNA contains the whole sequence of the RNA, including coding and untranslated sequence.
    CDS contains only coding sequence

    Args:
            dic_cdna: CDNA sequence dictionary. Key is a target ID. Sequence is SeqRecord.
            dic_cds: CDS sequence dictionary. Key is a target ID. Sequence is SeqRecord.
    Returns:
            dict: UTR dictionary
    """
    
    common_id = set(dic_cdna.keys()).intersection(dic_cds.keys())

    id_only_in_cdna = [x for x in dic_cdna.keys() if x not in common_id]
    id_only_in_cds = [x for x in dic_cds.keys() if x not in common_id]

    if len(id_only_in_cdna) > 0:
        log.warning(f'CDNA contains {len(id_only_in_cdna)} sequences more than CDS')
    
    if len(id_only_in_cds) > 0:
        log.warning(f'CDS contains {len(id_only_in_cds)} sequences more than CDNA')

    dic_utr = dict()
    for _id in common_id:
        utr_seq_obj = generate_utr_seq(dic_cds[_id],dic_cdna[_id])
        if utr_seq_obj is not None:
            dic_utr[_id] = utr_seq_obj
    
    return dic_utr


def load_cdna_cds_zipfile(
    downloadloc:str,
    cdna_file:str,
    cds_file:str
)->dict:
    """Load Ensembl CDNA,CDS file and generate CDS, UTR region.

    Args:
        downloadloc: folder location where CDNA, CDS exist
        cdna_file: Fasta format zip file for CDNA
        cds_file: Fasta format zip file for CDS
    Returns:
        dict: 3-UTR, 5-UTR, CDS sequence dictionary
    """

    # Load sequences from zip file
    seq_cdna = load_rna_fasta_zipfile(os.path.join(downloadloc, cdna_file))
    seq_cds = load_rna_fasta_zipfile(os.path.join(downloadloc, cds_file))

    # Classify CDS, UTR region
    seqs = dict()
    for k, v in generate_utr_from_cdna_cds(seq_cdna, seq_cds).items():
        seqs.update({k: {'CDS': seq_cds[k].seq, 'UT3': v['utr3'], 'UT5': v['utr5']}})
    
    return seqs
