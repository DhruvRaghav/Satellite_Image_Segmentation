import wget
import requests

with open('index.txt') as f:
    lines = f.readlines()
    # print(lines)
    count=0
for line in lines:
    count += 1
    # print(type(line))
    url = 'http://www.cs.toronto.edu/~vmnih/data/mass_buildings/train/sat//'+ line
    newstr = url.strip()
    # print("filename = wget.download('"+newstr+"')")
    filename = wget.download(newstr)
