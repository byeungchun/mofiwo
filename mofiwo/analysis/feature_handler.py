""" Feature handler """

import re
from itertools import product
from pandas import DataFrame, Series
from mofiwo import log

def generate_k_mer(num_k: int, nucleotides: list = ['A', 'T', 'C', 'G']) -> list:
    """ generate a cartesian product of input iterables

    Args:
        num_k: number of k merase
        nucleotides: list of nucleotides
    Return:
        list: 
    """
    return [''.join(nt) for nt in [nt_record for nt_record in product(nucleotides, repeat=num_k)]]


def generate_feature_by_kmer_loc(dic_seq: dict, kmers: list = [3, 4, 5], need_log: bool=False) -> dict:
    """ generate feature dataframe by kmer list and sequence group (cds, utr) 

    Args:
        dic_seq: sequence dictionary by target_id
        kmers: list of k-mers

    Return:
        dict:
    """
    cnt_res = 0
    target_feature = dict()
    for target_id, seqs in dic_seq.items():
        row_cnt = dict()
        for seq_idx, seq in seqs.items():
            for num_k in kmers:
                _temp = Series({f'{seq_idx}_{kmer}': len(re.findall(
                    kmer, str(seq))) for kmer in generate_k_mer(num_k)})
                row_cnt.update(_temp.apply(
                    lambda x: x / _temp.sum()).to_dict())
        target_feature[target_id] = row_cnt
        if need_log:
            cnt_res += 1
            if cnt_res % 100 == 0:
                log.info(f'# proceed: {len(target_feature)}')
    return target_feature
