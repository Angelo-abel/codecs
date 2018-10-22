#!/usr/bin/python3

import argparse
import subprocess
import sys
import os
import numpy as np
from elasticsearch import  Elasticsearch


CMD = "python3 " + os.path.join(os.path.dirname(os.path.abspath(__file__)),\
    "codec.py -i {} -o {} {} {}")
INFO_ALGO = {
    1: 'Inverter codec',
    2: 'Xor codec',  
    3: 'XorInv codec',
    4: 'Xor Passphrase'}

def cmdLine():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-n', '--number', help='Number of iteration', \
        type=int, required=True)
    parser.add_argument('-f', '--folder', help='path of folder contain the \
        benchmarks files', required=True)
    parser.add_argument('-t', '--tag', help='tag version', \
        type=str, required=True)
    parser.add_argument('-i', '--index', help='Index of latest record in \
        Elasticsearch', type=int, required=True)
    return parser.parse_args()


def readFolder(folder_path: str)->list:
    folder_list: list[str] = []
    if os.path.isdir(folder_path):
        for name in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, name)):
                folder_list.append(os.path.abspath(os.path.join(folder_path, name)))
    else:
        raise NotADirectoryError
    return folder_list

def run(benchmark_list_file: list, n: int, statistc_folder: str, index:int =1):
    output_folder = os.path.join(os.path.dirname(benchmark_file_list[0]), \
        'codecs')
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),\
        'measurement/{}/stats.md'.format(str(statistc_folder))), \
        'w', encoding='utf8') as destination_file:
        for k, algo in INFO_ALGO.items():
            destination_file.write('# {}\n'.format(algo))
            for file_path in benchmark_list_file:
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                destination_file.write('## File {}\n - [ ] Encode\n'.format(file_name))
                stats = np.array([])
                data = {
                    'version': int(statistc_folder.split('.')[2]),
                    'time_dec': [],
                    'time_enc': [],
                    'algo_name': algo,
                    'algo_num': k,
                    'size': file_name  
                }
                # Encode
                for i in range(n):
                    result = subprocess.check_output(CMD.format(file_path, output_folder+'/' + file_name, \
                         '-e {}'.format(k), '-p c'), shell=True)
                    stats = np.append([stats], [[float(result.decode('utf8').split('\n')[0])]])
                    destination_file.write('  {}. '.format(str(i+1))+result.decode('utf8'))
                destination_file.write('\n###Statistics\n  - Moy = {}\n  - Ecart type = {}\n\n'.format(stats.mean(), np.std(stats)))

                # Decode
                data['time_enc'] = list(stats)
                destination_file.write(' - [ ] Decode\n'.format(file_name))
                stats = np.array([])
                for i in range(n):
                    result = subprocess.check_output(CMD.format(output_folder \
                        +'/' + file_name, output_folder + '/dec_'\
                         + file_name, '-d {}'.format(k), '-p c'), shell=True)
                    stats = np.append([stats], [[float(result.decode('utf8').split('\n')[0])]])
                    destination_file.write('  {}. '.format(str(i+1))+result.decode('utf8'))
                destination_file.write('\n###Statistics\n  - Moy = {}\n  - Ecart type = {}\n\n'.format(stats.mean(), np.std(stats)))                    
                data['time_dec'] = list(stats)
                es = Elasticsearch()
                es.index(index="codecs_statistics", doc_type="statistic", body=data, id=index)
                index += 1
                # print(data)

if __name__ == '__main__':
    args = cmdLine()
    try:
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        benchmark_file_list  = readFolder(args.folder)
        if not os.path.isdir(os.path.abspath(
            os.path.join(args.folder, 'codecs'))):
            os.mkdir(os.path.join(args.folder, 'codecs'))
        if not os.path.isdir(os.path.abspath(
            os.path.join(script_path, 'measurement/{}'.format(args.tag)))):
            os.mkdir(script_path+'/measurement/{}'.format(str(args.tag)))
        run(benchmark_file_list, args.number, args.tag, args.index)
    except NotADirectoryError:
        print("Please, Folder required not file")
        sys.exit(-1)
    except PermissionError:
        print('Please, Permission denied to write in {}'.format(args.folder))
        exit(-1)
    except:
        pass
                
