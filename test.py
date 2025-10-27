file = open("index.html", 'r')
print([s.strip() for s in file.readlines()])
