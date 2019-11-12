#import sys

class Email(object):
    def __init__(self, row, date):
        self.row = row
        self.date = date

def main():
    # uncomment later to open file passed as command line arg
    #f = open(sys.argv[1], "r")

    f = open("1000_data.xml", "r")
    lines = f.readlines()
    emails = []

    # extract all necessary info from xml file
    for line in lines:
        if line.find("<mail>") != -1:
            row = line[line.find("<row>")+5:line.find("</row>")].lower()
            date = line[line.find("<date>")+6:line.find("</date>")].lower()
            emails.append(Email(row, date))

    # write to emails.txt file
    e = open("dates.txt", "w")
    for email in emails:
        row_str = ":" + email.row + "\n"
        temp = email.date + row_str
        e.write(temp)

    e.close()
    f.close()

main()