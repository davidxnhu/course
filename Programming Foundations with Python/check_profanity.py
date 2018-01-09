import urllib

def read_text():
    quotes=open("")
    contents_of_file=file.read()
    quotes.close()
    check_profanity(contents_of_file)

def check_profanity(test):
    connection=urllib.urlopen("http://...")
    output=connection.read()

    connection.close()

    if True in output:
        print("Profanity Alert")
    elif False in output:
        print("This document has no curse word")
    else:
        print("The file cannot be scanned")
    
