import re
from collections import defaultdict
id_dict = defaultdict(list)
id_to_rating = "/Users/ivywang/PycharmProjects/movie_final/title.ratings.tsv"
id_to_attr = '/Users/ivywang/PycharmProjects/movie_ratings/data.tsv'
movie_attributes = '/Users/ivywang/PycharmProjects/movie_ratings/movie_attributes.tsv'
# append those that: type is either short or movie, append title, append start/end year if there is any; append year
# that is more than 1950; append genre, lowered. Title is also lowered and stripped of spaces
with open(id_to_attr, 'r') as attr:
    next(attr)
    for line in attr:
        fields = line.strip().split('\t')
        if fields[1] == 'movie' or fields[1] == 'short':
            title = fields[2].lower()
            title = "".join(title.split())
            title = re.sub(r'[^\w\s]', '', title)
            id_dict[fields[0]].append(title) # append title
            # try to append year, if no year then do 0000
            if len(fields[5]) > 3 and fields[5] is not None:
                year = int(fields[5])
            elif len(fields[6]) > 3 and fields[6] is not None:
                year = int(fields[6])
            else:
                year = 0
            if year > 1950 or year == 0:
                id_dict[fields[0]].append(year)
            if fields[8] is not None:
                id_dict[fields[0]].append(fields[8].lower()) # genre


# append raitng and numVotes
with open(id_to_rating, 'r') as rating:
    next(rating)
    for line in rating:
        r_fields = line.strip().split('\t')
        if r_fields[0] in id_dict.keys():
            id_dict[r_fields[0]].append(r_fields[1]) # rating
            id_dict[r_fields[0]].append(r_fields[2]) # number of votes


# remove from the ones that do not have ratings
for i, j in list(id_dict.items()):
    if len(j) < 4:
        del id_dict[i]
with open(movie_attributes, 'w') as output:
    for i, j in id_dict.items():
        output.write(i)
        output.write('\t')
        for attr in j:
            output.write(str(attr))
            output.write('\t')
        output.write('\n')

print(len(id_dict.keys())) # returns 341306 films



movie_name_list = '15minutes'
dialog_filename = '15minutes_dialog.txt'
scene_filename = f'{movie_name_list}_scene.txt'
dialog_list = []

dialog_file = f'/Users/ivywang/PycharmProjects/movie_final/dialogs/Action/{dialog_filename}'
scene_file = f'/Users/ivywang/PycharmProjects/movie_final/scenes/Action/{scene_filename}'


# extract the dialog in the file
with open(dialog_file, 'r') as dialog_file:
    for line in dialog_file:
        dialog_list.append(line)
        dialog_list = [d for d in dialog_list if d is not '\n']
        # dialog_list = [d for d in sublist for sublist in dialog_list]
print(len(dialog_list))
for d in dialog_list[:5]:
    print(d)
