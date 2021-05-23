import os
import gc
import gzip
import numpy as np
import pickle
import pandas as pd
from pathlib import Path
from datetime import datetime
from Bio import SeqIO, bgzf
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

def write_seq(fout, seq):
    SeqIO.write(seq, fout, 'fastq')
    return True

def main():
    df_barcode = pd.read_excel('barcode.xlsx')
    meta = {'len_barcode': 6, 'len_umi': 10}
    meta['path_raw'] = r'./data/fastq/raw/'
    meta['raw_fastq'] = os.listdir(meta['path_raw'])
    meta['path_output'] = f"output_{datetime.now().strftime('%Y%m%d_%H%M')}"
    meta['path_pool'] = {y: os.path.join(meta['path_output'], y) for y in set([x[:6] for x in meta['raw_fastq']])}

    meta['pool_fastq'] = {'ML1_S4': 'N701', 'ML2_S5': 'N702'}

    for pool_key, pool_path in meta['path_pool'].items():
    
        _tgt_seq = {x: list() for x in df_barcode[df_barcode.pool == meta['pool_fastq'][pool_key]].sequence}
        
        fastq = {'R1':'', 'R2':''}    
        for _key in fastq.keys():
            fastq[_key] = [x for x in meta['raw_fastq'] if x.startswith(pool_key) and x.find(_key) > 0][0]
            
        _fobj = dict()
        for _barcode in _tgt_seq.keys():
            _path_barcode = os.path.join(pool_path,_barcode)
            Path(_path_barcode).mkdir(parents=True,exist_ok=True)
            _fobj[_barcode] = dict()
            for _key, _val in fastq.items():
                _fobj[_barcode][_key] = open(os.path.join(_path_barcode, f"{_val[:-8]}fastq"),'wt')
        
        with gzip.open(os.path.join(meta['path_raw'], fastq['R1']), 'rt') as fin_r1:
            with gzip.open(os.path.join(meta['path_raw'], fastq['R2']), 'rt') as fin_r2:
                _read1 = SeqIO.parse(fin_r1, "fastq")
                _read2 = SeqIO.parse(fin_r2, "fastq")
                iter_count = 0
                while True:
                    try:
                        _r1_seq = next(_read1)
                        _r2_seq = next(_read2)
                        _barcode = str(_r1_seq.seq[:meta['len_barcode']])
                        if _barcode in _tgt_seq.keys():
                            write_seq(_fobj[_barcode]['R1'], _r1_seq)
                            write_seq(_fobj[_barcode]['R2'], _r2_seq)
                        iter_count += 1
                        if iter_count % 100000 == 0:
                            print(f'Line proceeded: {iter_count}')
                    except Exception as ex:
                        print(ex)
                        for _filer1r2 in _fobj.values():
                            for _file in _filer1r2.values():
                                _file.close()
                        break

        for _filer1r2 in _fobj.values():
            for _file in _filer1r2.values():
                _file.close()
        
        print(f"writing finished: {pool_key}({datetime.now().strftime('%Y%m%d %H:%M')})")

if __name__ == "__main__":
    main()