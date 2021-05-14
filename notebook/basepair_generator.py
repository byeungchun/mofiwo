import os
import re
import timeit
import pickle
import itertools
import numpy as np
import pandas as pd
from concurrent import futures
from datetime import datetime

from mofiwo.utility.rna_handler import load_rna_fasta_zipfile
from mofiwo.utility.rna_handler import generate_utr_from_cdna_cds

def prep_seq():
    fasta_cds_zipfile = r'D:\workspace\rnamotif\samples\s1_cds.zip'
    fasta_cdna_zipfile = r'D:\workspace\rnamotif\samples\s1_cdna.zip'
    
    dic_cds = load_rna_fasta_zipfile(fasta_cds_zipfile)
    dic_cdna = load_rna_fasta_zipfile(fasta_cdna_zipfile)
    
    dic_utr3 = generate_utr_from_cdna_cds(dic_cdna, dic_cds)
    df_s1 = pd.read_excel(r'D:/workspace/rnamotif/samples/aan2399_table_S1.xlsx')

    return df_s1, dic_utr3

def generate_target_group(df_target, dic_utr3, qval_limit = 0.2, is_apical=True, mean_obs_limit=3.539):
    if is_apical:
        df_target = df_target[df_target.b > 0]
    else:
        df_target = df_target[df_target.b < 0]
    lst_apical = list(df_target[df_target.apply(lambda x: 
                                                x.qval < qval_limit and 
                                                x.mean_obs > mean_obs_limit , axis=1)].target_id)
    
    return {x:str(dic_utr3[x].seq) for x in lst_apical if x in dic_utr3.keys()}

def calculate_bp_count(seqs,grp_num):
    seq_key = seqs[0]
    seq_str = seqs[1]
    bp_all = itertools.product(['A','T','C','G'], repeat=grp_num)
    bp_all = [''.join(x) for x in bp_all]
    bp_cnt = {bp:0 for bp in bp_all}
    for bp in bp_all:
        num_bp = len(re.findall(bp, seq_str)) 
        if num_bp > 0:
            bp_cnt[bp] += num_bp
    return {seq_key:bp_cnt}

def main():
    df_s1, dic_utr3 = prep_seq()
    dic_apical = generate_target_group(df_s1, dic_utr3)
    dic_basal = generate_target_group(df_s1, dic_utr3, is_apical=False)

    # with futures.ThreadPoolExecutor(max_workers=10) as executor:
    #     bp_all = itertools.product(['A','T','C','G'], repeat=6)
    #     bp_all = [''.join(x) for x in bp_all]
    #     ret_bp_cnt = {executor.submit(calculate_bp_count, seq_str, bp_all): seq_str for seq_str in dic_apical.values()}
    #     ret= [x.result() for x in futures.as_completed(ret_bp_cnt)]
    
    for seq_loc in ['apical', 'basal']:
        if seq_loc == 'apical':
            seqs = dic_apical.items()
        else:
            seqs = dic_basal.items()
        for grp_num in [3,4,5,6,7,8,9,10]:
            with futures.ProcessPoolExecutor(max_workers=10) as executor:
                ret = dict()
                for seq, bp_cnt in zip(seqs, executor.map(calculate_bp_count, seqs, itertools.repeat(grp_num))):
                    ret.update(bp_cnt)
            pickle.dump(ret, open(os.path.join(os.path.expanduser(r'~\Downloads'), f'{seq_loc}_bp_{grp_num}.pickle'), "wb"))
            print(f'DONE - {seq_loc}_bp_{grp_num}')
if __name__ == '__main__':
    print(timeit.Timer(main).repeat(repeat=1, number=1))