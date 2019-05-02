# Predicting IMDB public rating from screenplays

In this project, we are interested in examining the screenplay in films, and whether 
these textual information could be used to predict movie ratings. 

## Dataset

We used two datasets for this project, one of the screenplay texts and the other of 
user rating, among other movie metadata. 

IMDB API files: ???

Film Corpus 2.0: https://nlds.soe.ucsc.edu/fc2

## data_extraction.py

This code extracts movie scripts and ratings from the IMDB API files and movie script files. 
The output is a tsv file of movie names, movie rating and movie scripts. 

There are five command arguments possible: 

* -d --dialogues_file: folder of movie script files. 
* -r --id_to_rating_file: IMDB API tsv file containing movie IDs, ratings and number of votes.
* -a --id_to_attr_file: IMDB API tsv file containing movie IDs, ratings and other metadata.
* -ao --attributes_output: path name of tsv file containing movie names and movie metadata.
* -dfo --data_frame_output: path name of tsv file containing movie names, movie ratings and movie scripts.

Example usage:

    python data_.py -d dialogs -r title.ratings.tsv -a title.basics.tsv -ao movie_attributes.tsv -dfo script_file.txt 
    
    

`

## train_data.py
