# Predicting IMDb Rating From Movie Scripts
Authors: Ivy Wang, Siyu Liang, Jingjing Lin
## Objective 

In this project, we are interested in examining the screenplay in films, and whether 
these textual information could be used to predict movie ratings. 

## Datasets

We used two datasets for this project, one of the screenplay texts and the other of 
user rating, among other movie metadata. 

IMDB API files: https://datasets.imdbws.com

Film Corpus 2.0: https://nlds.soe.ucsc.edu/fc2

## Code Instruction

There are two python files in this project
- data_extraction.py 
- train_data.py

And two output files of processed datasets 
- movie_attributes.tsv
- script_file.tsv

It takes around 30 minutes to run the entire project.

### data_extraction.py

This code extracts movie scripts and ratings from the IMDB API files and movie script files. 
The output is a tsv file of movie names, movie rating and movie scripts. 

There are five command lines arguments possible: 

* -d --dialogues_file: folder of movie script files. 
* -r --id_to_rating_file: IMDB API tsv file containing movie IDs, ratings and number of votes.
* -a --id_to_attr_file: IMDB API tsv file containing movie IDs, ratings and other metadata.
* -ao --attributes_output: path name of tsv file containing movie names and movie metadata.
* -dfo --data_frame_output: path name of tsv file containing movie names, movie ratings and movie scripts.

Example usage:

    python data_extraction.py -d dialogs -r title.ratings.tsv 
    
-----

### train_data.py

This Python script is intended to be used after the dataset between film scripts and IMDb 
ratings has been incorporated and cleaned. The code takes the input file, extracts the 
script and the rating. It first puts the ratings into a list of gold standard labels, 
and then based on each script, engineers desired features. 

#### Features include:
- number of sentences (baseline)
- mean words per sentence (average sentence length)
- TFIDF vector (fitted for sparsity)
- percentages of nouns, verbs, and adjectives

To engineer these features we first obtain relevant data into lists, then, after filtering out the items that contain over 50 of the number of mean words per sentence (outliers), we transform the lists into numpy arrays. 

For each individual/combined feature, we split the dataset into training, validation, and test. Then we trained each feature  and feature combinations on both linear regression model and Random Forest Regression model. We evaluated the models on validation data. 
Our last results were generated on the baseline feature and the TFIDF-Mean words feature, for the test dataset.

Example usage: 

    python train_data.py -f script_file.txt
    
## Output Files

### movie_attributes.tsv

Output file of data_extraction.py; contains IMDb ID, movie name, production year, genre, rating 
and number of votes. 

### script_file.tsv

Output file of data_extraction.py; contains movie name, rating and movie script.
