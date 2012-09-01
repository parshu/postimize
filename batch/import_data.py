import sys
sys.path.append('.')
import csv
from collections import defaultdict, Counter
from datetime import datetime
import pymongo

if __name__ == '__main__':
    ifile_name = sys.argv[1]
    dbname = sys.argv[2]
    tablename = sys.argv[3]
    table = pymongo.Connection('localhost', 27017)[dbname][tablename]
    if(sys.argv[4] == 'reload'):
        table.remove()
    for line in csv.DictReader(open(ifile_name, 'r')):
        table.insert(line)

