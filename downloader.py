import urllib.request

FILE_ADDRESS = "/Users/Ken/Downloads/image/image.txt"
FOLDER = "/Users/Ken/Downloads/image/"
line_num = 53

def download():
    f = open(FILE_ADDRESS, 'r')
    count = 0
    for line in f:
        count += 1
        if count<line_num:
            continue
        name, href=line.split(',')
        urllib.request.urlretrieve(href, FOLDER + name+".jpg")

if __name__ == "__main__":
    download()



