import os
from glob import glob
from natsort import natsorted
import fileinput
import argparse
import configparser
import pathlib
import sys

package_base_dir = pathlib.Path(__file__).parent.parent.parent.resolve()

def parse_args():
    config = configparser.ConfigParser()
    cred_file = os.path.join(package_base_dir,'credentials','default_path.txt')
    if os.path.exists(cred_file):
        config.read(cred_file)
        default_path = config['defaults']['default_path']
    else:
        default_path = './'

    parser = argparse.ArgumentParser(description='Creates master document for paper summaries. \
        Requires a directory structure where the master document ends up in the base folder. \
        This base folder requires two subfolders, pdfs/ and summaries/. pdfs/ holds the pdfs \
        associated with each paper and these will be linked to in the master document via \
        hyper refs. summaries/ holds markdown documents summarising each paper. These \
        files should not contain hyper links. It is a good idea to in these files give the full \
        title of the paper. The naming convention for all .md and .pdf files should be \
        "Firstauthor+year" + file ending. In the case of multiple papers ending up with the \
        same name, add Secondauthor, etc. before "+year".')

    parser.add_argument(
        '--basedir', 
        type=str, 
        default=default_path,
        help='Path to base directory. Needs to hold directories "summaries" and "pdfs".'
    )
    

    return parser

def get_all_papers(source_document_path, source_pdf_path):
    papers_md = glob(os.path.join(source_document_path,'*md'))
    papers_pdf = glob(os.path.join(source_pdf_path,'*pdf'))
    paper_names = []
    for paper in papers_md:
        name = paper.split('\\')[-1].split('.')[0]
        if name not in paper_names:
            paper_names.append(name)
    for paper in papers_pdf:
        name = paper.split('\\')[-1].split('.')[0]
        if name not in paper_names:
            paper_names.append(name)
    paper_names = natsorted(paper_names)
    return paper_names

def get_name(paper_name):
    if '+' in paper_name:
        paper_name = paper_name.replace('+', ' et al. (')+')'
    return paper_name

def write_link(paper_name):
    name = get_name(paper_name)
    rel_path = os.path.join('pdfs', f'{paper_name}.pdf')
    write_string = f'### [{name}]({rel_path})\n'
    return write_string
        
def main():
    parser = parse_args()
    args = parser.parse_args()

    basedir = os.path.abspath(args.basedir)

    source_document_path = os.path.join(basedir, 'summaries')
    source_pdf_path = os.path.join(basedir, 'pdfs')
    master_document_path = os.path.join(basedir, 'paper_summaries_master.md')

    # uncomment for debugging
    # print(f'source_document_path = {source_document_path}')
    # print(f'source_pdf_path = {source_pdf_path}')
    # print(f'master_document_path = {master_document_path}')
    
    paper_names = get_all_papers(source_document_path, source_pdf_path)
    
    with open(master_document_path, 'w') as fo:
        for paper_name in paper_names:
            try:
                md_name = os.path.join(source_document_path, f'{paper_name}.md')
                pdf_name = os.path.join(source_pdf_path, f'{paper_name}.pdf')
                if not os.path.exists(md_name):
                    print(f'{md_name} does not exist. Will create it.')
                    with open(md_name, 'w') as foo:
                        
                        line = get_name(paper_name)
                        foo.write(f'### {line}\n')
                        foo.write(f'##### [title]\n')

                finput = fileinput.input(md_name)
                for i,line in enumerate(finput):
                    if i==0:
                        if not os.path.exists(pdf_name):
                            print(f'{pdf_name} does not exist')
                            name = get_name(paper_name)
                            line = f'### {name} [pdf is missing]\n'
                        else:
                            line = write_link(paper_name)
                    fo.write(line)
                fo.write('\n\n')
            except Exception as e:
                print(f'trying to write {paper_name} to {md_name} fails:', e)
                finput.close()

if __name__ == '__main__':
    sys.exit(main())