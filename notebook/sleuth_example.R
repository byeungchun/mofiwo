library("sleuth")

setwd('/home/byeungchun/workspace/eth/output_20210512_0128_sample_10000/ML1_S4')
kal_dirs <-file.path(sampid, 'output')

s2c<-read.table('hiseq_info.txt', header=TRUE, stringsAsFactors =FALSE,sep='\t')
s2c<-dplyr::select(s2c, sample=run_accession, condition)
s2c <- dplyr::mutate(s2c, path=kal_dirs)
so <- sleuth_prep(s2c, extra_bootstrap_summary=TRUE)
