# README
A small script to help organise scientific papers in a simple, portable way

## Package overview

Creates master document for paper summaries. Requires a directory structure where the master document ends up in the base folder. This base folder requires two subfolders, pdfs/ and summaries/. pdfs/ holds the pdfs associated with each paper and these will be linked to in the master document via hyper refs. summaries/ holds markdown documents summarising each paper. These files should not contain hyper links. It is a good idea to in these files give the full title of the paper. The naming convention for all .md and .pdf files should be "Firstauthor+year" + file ending. In the case of multiple papers ending up with the same name, add Secondauthor, etc. before "+year".

If you want to set a default path, add file "default_path.txt" to ./credentials, containing

    [defaults]
    default_path=your_default_path

where "your_default_path" is whatever you want your default path to be.

### Full package folder structure 
```
PaperMarkdownMerging
┣ credentials
┃ ┗ default_path.txt
┗ src
  ┗ PaperMarkdownMerging
    ┣ merge.py
    ┗ __init__.py
```

### Outline of basedir
```
basedir
┣ pdfs
┃ ┗ Firstauthor+year().pdf
┣ summaries
┃ ┗ Firstauthor+year().md
┗ paper_summaries_master.md
```

where each paper summary document should start with 
    
    ### FirstAuthor et al. (year)
    ##### Full paper title.

In case the .md file is missing for a paper where the pdf is present, an .md file will be created, containing only "### FirstAuthor et al. (year)"

## Installation
- Clone repo
- Create conda environment and install required packages
```
  conda create --name pmm python=3.7
  conda activate pmm
  pip install -r requirements.txt
```
- Add instructions here on how to make script accessible from anywhere. Install where in linux/windows? Add to path? 
## To do
- [] Add more proper installation instructions for both linux and windows to allow execution from arbitrary location
- [] Make pdf and summaries folders arbitrary
- [] Make summary document name editable
- [] Add support for relative paths
- [] Add support to give papers tags on which summary document can be sorted/filtered
  - [] Automatically write document with list of all existing tags