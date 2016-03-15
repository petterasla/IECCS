# Tools for writing predictions to file
def initFile(filename):
    file = open(filename+".txt", 'w')
    return file

def writeTextToFile(text, file):
    if isinstance(text, str):
        file.write(text)
    else:
        file.write(str(text))
    file.write("\n")

