""" This module contains helper functions for rna_handler"""

from mofiwo import log

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def generate_utr_seq(
    cds_seq_obj, 
    cdna_seq_obj
) -> bool:
    """Check UTR location and generate UTR sequences (3' and 5')

    Args:
        cds_seq_obj: Coding sequence of SeqRecord object
        cdna_seq_obj: Whole sequence of SeqRecord object

    Returns:
        bool: True if it locates a valid position
    """
    ret_seq = None
    location_idx = cdna_seq_obj.seq.find(cds_seq_obj.seq)

    if location_idx <= 0:
        log.warning(f'Can not find coding sequence(CDS) position in {cds_seq_obj.id}')
    
    else:
        utr5_seq = cdna_seq_obj.seq[:location_idx]
        utr3_seq = cdna_seq_obj.seq[location_idx + len(cds_seq_obj.seq):]
        
        ret_seq = {'utr3': SeqRecord(utr3_seq, id=cdna_seq_obj.id, name= '3UTR region'),
            'utr5': SeqRecord(utr5_seq, id=cdna_seq_obj.id, name ='5UTR region')}
    
    return ret_seq
