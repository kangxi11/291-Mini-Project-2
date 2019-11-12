#import sys

class Email(object):
    def __init__(self, row, fr, to, cc, bcc, subj, body, date):
        self.row = row
        self.fr = fr
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.subj = subj
        self.body = body
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
            fr = line[line.find("<from>")+6:line.find("</from>")].lower()
            date = line[line.find("<date>")+6:line.find("</date>")].lower()
            to = ""
            if line.find("<to>") != -1:
                to = line[line.find("<to>")+4:line.find("</to>")].lower()
            cc = ""
            if line.find("<cc>") != -1:
                cc = line[line.find("<cc>")+4:line.find("</cc>")].lower()
            bcc = ""
            if line.find("<bcc>") != -1:
                bcc = line[line.find("<bcc>")+5:line.find("</bcc>")].lower()
            if line.find("<subj>") != -1:
                subj = line[line.find("<subj>")+6:line.find("</subj>")].lower()
            if line.find("<body>") != -1:
                body = line[line.find("<body>")+6:line.find("</body>")].lower()
            emails.append(Email(row, fr, to, cc, bcc, subj, body, date))

    # write to recs.txt file
    e = open("recs.txt", "w")
    for email in emails:
        row_str = email.row + ":<mail>"
        row2_str = "<row>" + email.row + "</row>"
        date_str = "<date>" + email.date + "</date>"
        from_str = "<from>" + email.fr + "</from>"
        to_str = "<to>" + email.to + "</to>"
        subj_str = "<subj>" + email.subj + "</subj>"
        cc_str = "<cc>" + email.cc + "</cc>"
        bcc_str = "<bcc>" + email.bcc + "</bcc>"
        body_str = "<body>" + email.body + "</body>"
        end_str = "</mail>\n"

        temp = row_str + row2_str + date_str + from_str + to_str + subj_str + cc_str + bcc_str + body_str + end_str
        e.write(temp)

    e.close()
    f.close()

main()