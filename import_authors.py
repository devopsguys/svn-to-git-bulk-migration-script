import csv


# Use this script to update authors.txt with a CSV file called 'users.csv'
# that contains username, firstname, lastname, email
# Autogenerate authors.txt by running: java -jar svn-migration-scripts.jar authors <svn-repo> > authors.txt

reader = csv.reader(open('users.csv'))
result = {}
for row in reader:
    key = row[0].strip().lower()
    if key in result:
        pass
    result[key] = row[1:]

with open('authors.txt') as f:
    authors = f.readlines()
authors = [x.strip() for x in authors] 

new_authors_file = open('authors.txt.new', 'w')
userlist = map(str.lower, result.keys())

for author in authors:
    authorname = author.split(' ', 1)[0]
    if authorname.lower() in userlist:
        author = "{0} = {1} {2} <{3}>".format(authorname, result[authorname.lower()][0].title().strip(), result[authorname.lower()][1].title().strip(), result[authorname.lower()][2])
    print author
    print>>new_authors_file, author
