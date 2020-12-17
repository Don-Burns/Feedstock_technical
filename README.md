# Enron Email Topic Analysis
## Summary
A topic analysis of the Enron email database as found [here](https://www.cs.cmu.edu/~./enron/).
The data should be extracted to the `data` folder.  After which either either both [`Enron_data_extraction.ipynb`](https://github.com/Don-Burns/Feedstock_technical/blob/master/code/Enron_data_extraction.ipynb) and [`Enron_email_field_splitting.ipynb`](https://github.com/Don-Burns/Feedstock_technical/blob/master/code/Enron_email_field_splitting.ipynb) or [`data_extraction.py`](https://github.com/Don-Burns/Feedstock_technical/blob/master/code/data_extraction.py) on the extracted copy of the enron dataset.  For ease of use the dataset should be named `maildir`, however this is only needed if using the notebooks.  If using [`data_extraction.py`](https://github.com/Don-Burns/Feedstock_technical/blob/master/code/data_extraction.py) simple add the name of the directory containing the files when running from within the code directory, e.g. `python data_extraction.py ../data/maildir/`.

The results of my analysis are presented within [`Enron_Analysis.ipynb`](https://github.com/Don-Burns/Feedstock_technical/blob/master/code/Enron_Analysis.ipynb).

## Dependecies
- `spacy`

- `pandas`

- `gensim`

- `pyLDAvis`

- `seaborn`

Additionally, a language model needs to be downloaded from `spacy` using the command `python -m download en`.

## Contents
### [code](https://github.com/Don-Burns/Feedstock_technical/tree/master/code)
Contains any code and notebooks for the anlysis.

### [data](https://github.com/Don-Burns/Feedstock_technical/tree/master/data)
The directory where the dataset should be save and all outputs will be saved.