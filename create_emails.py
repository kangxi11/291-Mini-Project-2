#import sys

class Email(object):
    def __init__(self, row, fr, to, cc, bcc):
        self.row = row
        self.fr = fr
        self.to = to
        self.cc = cc
        self.bcc = bcc

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
            fr = line[line.find("<from>")+6:line.find("</from>")].lower()
            to = ""
            if line.find("<to>") != -1:
                to = line[line.find("<to>")+4:line.find("</to>")].lower()
            cc = ""
            if line.find("<cc>") != -1:
                cc = line[line.find("<cc>")+4:line.find("</cc>")].lower()
            bcc = ""
            if line.find("<bcc>") != -1:
                bcc = line[line.find("<bcc>")+5:line.find("</bcc>")].lower()
            emails.append(Email(row, fr, to, cc, bcc))

    # write to emails.txt file
    e = open("emails.txt", "w")
    for email in emails:
        row_str = ":" + email.row + "\n"
        temp = "from-" + email.fr + row_str
        e.write(temp)
        if email.to:
            buff = email.to.split(",")
            for x in buff:
                temp = "to-" + x + row_str
                e.write(temp)
        if email.cc:
            buff = email.cc.split(",")
            for x in buff:
                temp = "cc-" + x + row_str
                e.write(temp)
        if email.bcc:
            buff = email.bcc.split(",")
            for x in buff:
                temp = "bcc-" + x + row_str
                e.write(temp)

    e.close()
    f.close()

main()
        
           

