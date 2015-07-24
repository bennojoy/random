#!/usr/bin/env python
import itertools as it
import redis
from random import randint

r = redis.StrictRedis(host='localhost', port=6379, db=0)

category_base_path ='/usr/share/games/fortune/'

def add_category_to_db(category_name=None):
    hash_name = category_name
    hash_index = 0
    filename = category_base_path + hash_name
    with open(filename,'r') as f:
        index = 0
        for key,group in it.groupby(f,lambda line: line.startswith('%')):
            if not key:
                value = ''
                for line in group:
                    line.replace('\n', '\\\\n')
                    line.replace('\t', '\\\\t')
                    value += line
                if index == 1000:
                    hash_index = hash_index + 1
                    index = 0
                r.hset(hash_name + '_' + str(hash_index), str(index), value)
                index = index + 1
    max_records = 1000 * hash_index + index
    r.set(hash_name, max_records - 1)

r.delete('categories')
categories = ['cookie', 'people']
for i in categories:
    for j in range(0, 100):
        r.delete(i + '_' + str(j))
for i in categories:
    r.lpush('categories', i)
    add_category_to_db(i)

print r.llen('categories')

cat_index = randint(0, int(r.llen('categories')))

cat = r.lrange('categories', cat_index, cat_index)[0]
print cat
max_items = r.get(cat)
random_index = randint(0, int(max_items))
print random_index

random_hash_index = int(random_index / 1000)

if random_hash_index == 0:
    random_index_number = random_index
else:
    random_index_number = random_index - (1000 * random_hash_index)

print random_index_number
val = r.hget(cat + '_' + str(random_hash_index), random_index_number)

print val


    

