import re
import os
from collections import defaultdict

## README
print ('#### ATTENTION ####:\n \
This code is TESTED on Windows.\n\
Running on Ubuntu may yield an error while reading from files\
due to some SPECIAL UNRECOGNIZED characters.\n \
For example: in Cloning Pets.txt, there is a charater \'"\'-(double quotes) \
at the word Actually, 2nd sentence.')
## 

# optional function
def write_to_file(inverted_index):
    with open('inverted_index.txt', 'w') as out:
        for key in inverted_index:
            out.write(key)
            out.write(str(inverted_index[key]))
            out.write('\n')

# Find all docs that contains query
def list_all_docs(inverted_index, query):
    # Test func for 1.3b
    #query = re.sub(r'[^\w\s]','', query.lower())
    query = re.findall(r'([\d]+,[\d]+|[\d]+.[\d]+|[\w]+)', query.lower())[0]

    if query in inverted_index:
        return inverted_index[query]
    else:
        return None

# Convert doc index to file's name and print out
def print_list_of_file_name(list):
    if list is None:
        return

    print (len(list))
    for item in list:
        print('->', docs_index[item])

# Get list of file's names
file_list = os.listdir('docs')
path = os.getcwd()
docs_path = path + '\\docs'

# Inverted index without term freq -> non sorting
# {word : doc_index}
inverted_index = defaultdict()

# {doc_index : filename}
docs_index = defaultdict()

## Ex1.3a+b ##
# read file -> create dictionary -> create inverted_index
print ('------ Ex1.3a+b ------')
index = 0
with open('dictionary.txt', 'w') as out:
    for filename in file_list:
        docs_index[index] = filename
        with open(docs_path + '\\'+ filename, 'r') as file:
            for line in file:
                # This may not be the best solution
                # re.findall(r'([\d]+,[\d]+|[\d]+.[\d]+|[\w]+)', line)
                # re.sub(r'[^\w\s]','', line).split(' ')
                words = re.findall(r'([\d]+,[\d]+|[\d]+.[\d]+|[\w]+)', line)
                for word in words:
                    word = word.lower()
                    if word not in inverted_index:
                        inverted_index[word] = [index]
                        out.write(word + '\n')
                    else:
                        if index not in inverted_index[word]:
                            inverted_index[word].append(index)
        index += 1

# write_to_file(inverted_index)


## Test inverted_index ##
query = input('Test query for 1.3b: ')
print_list_of_file_name(list_all_docs(inverted_index, query))

print ('------ Ex1.3a+b ------')
print ()
## Driver for 1.3c ##
print ('------ Ex1.3c ------')
query = input('String query for 1.3c: ')

ret = []
for word in query.split(' '):
    tmp = list_all_docs(inverted_index, word)
    if tmp is not None:
        ret.extend(list(set().union(ret, tmp)))

print ("Search result for: ", query),
print_list_of_file_name(ret)

print ('------ Ex1.3c ------')