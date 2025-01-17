#!/usr/bin/env python
desc= "Concatenate file(s) containing median current intensity values per position values."

# Import required libraries:
import argparse
import statistics
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.compute as pc
import pyarrow.dataset as ds
from pyarrow import fs

def generate_output(output_file, data, initial):
    #Create output file:
    out_file = output_file+'.tsv.gz'

    if initial: 
        data.to_csv(out_file, sep = '\t', index = False, compression = "gzip")
                
    else:
        data.to_csv(out_file, sep = '\t',  mode='a', index = False, header = False, compression = "gzip")

def process_dicts(files, output_file):
    list_tables = list()
    
    #Concatenate parquete files:
    for file in files:
        #Open and read input file:
            new_table = pq.read_table(file, columns=['contig','position', 'reference_kmer', 'median', 'coverage'])
            #list_tables.append(new_table)

            #concat_table = pa.concat_tables(list_tables) 
    
            #Create partitioned data:
            pq.write_to_dataset(new_table, root_path='dataset_name', partition_cols=['contig'])

    #Create schema:
    dataset = ds.dataset("./dataset_name", format="parquet", partitioning="hive")

    #Extract all contigs:
    filenames = os.listdir("./dataset_name")
    transcripts = ' '.join(filenames).replace('contig=','').split()
    initial = True

    for single_transcript in transcripts:
        table = dataset.scanner(filter=ds.field("contig") == single_transcript).to_table().to_pandas(use_threads=True).groupby(['contig', 'position','reference_kmer'], observed=True).agg({'median':'median', 'coverage':'sum'})
        #table = concat_table.filter(mask).to_pandas().groupby(['contig', 'position','reference_kmer'], observed=True).agg({'median':'median', 'coverage':'sum'}) 
        table.columns = ['median', 'coverage']
        table = table.reset_index()
 
        #Generate output:
        generate_output(output_file, table, initial)
        initial = False

def main():
    parser  = argparse.ArgumentParser(description=desc)

    parser.add_argument('-i', '--input', nargs='+' ,help='Input file(s) to process.')
    parser.add_argument('-o', '--output', help='Output filename')

    a = parser.parse_args()
    
    #Read, parse and merge data from individual eventalign files:
    process_dicts(a.input, a.output)
    
if __name__=='__main__': 
    main()
