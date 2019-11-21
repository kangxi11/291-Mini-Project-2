import sys

class RecsEmail(object):
    def __init__(self, row, fr, to, cc, bcc, subj, body, date):
        self.row = row
        self.fr = fr
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.subj = subj
        self.body = body
        self.date = date

def create_recs(line,e):
    emails = []
    if line.find("<mail>") != -1:
        row = line[line.find("<row>")+5:line.find("</row>")]
        fr = line[line.find("<from>")+6:line.find("</from>")]
        date = line[line.find("<date>")+6:line.find("</date>")]
        to = ""
        if line.find("<to>") != -1:
            to = line[line.find("<to>")+4:line.find("</to>")]
        cc = ""
        if line.find("<cc>") != -1:
            cc = line[line.find("<cc>")+4:line.find("</cc>")]
        bcc = ""
        if line.find("<bcc>") != -1:
            bcc = line[line.find("<bcc>")+5:line.find("</bcc>")]
        if line.find("<subj>") != -1:
            subj = line[line.find("<subj>")+6:line.find("</subj>")]
        if line.find("<body>") != -1:
            body = line[line.find("<body>")+6:line.find("</body>")]
        emails.append(RecsEmail(row, fr, to, cc, bcc, subj, body, date))

    # write to recs.txt file
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


class DateEmail(object):
    def __init__(self, row, date):
        self.row = row
        self.date = date

def create_date(line,e):
    emails = []

    # extract all necessary info from xml file
    if line.find("<mail>") != -1:
        row = line[line.find("<row>")+5:line.find("</row>")]
        date = line[line.find("<date>")+6:line.find("</date>")]
        emails.append(DateEmail(row, date))

    
    # write to emails.txt file
    for email in emails:
        row_str = ":" + email.row + "\n"
        temp = email.date + row_str
        e.write(temp)




class EmailsEmail(object):
    def __init__(self, row, fr, to, cc, bcc):
        self.row = row
        self.fr = fr
        self.to = to
        self.cc = cc
        self.bcc = bcc

def create_emails(line,e):
    emails = []
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
        emails.append(EmailsEmail(row, fr, to, cc, bcc))

    # write to emails.txt file
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


class TermsEmail(object):
    def __init__(self, row, subj, body):
        self.row = row
        self.subj = subj
        self.body = body

def create_terms(line,t):
    emails = []
    valid_special = ["_", "-"]
    terms = []
    
    if line.find("<mail>") != -1:
        row = line[line.find("<row>")+5:line.find("</row>")]
        subj = line[line.find("<subj>")+6:line.find("</subj>")]
        body = line[line.find("<body>")+6:line.find("</body>")]

        emails.append(TermsEmail(row, subj, body))

    for email in emails:
        # search for terms in the subject line
        temp = ""
        for char in email.subj:
            if char.isalnum() or char in valid_special:
                temp += char
            else:
                if len(temp) > 2:
                    terms.append("s-"+temp.lower()+":"+email.row)
                temp = ""
        if len(temp) > 2:
            terms.append("s-"+temp.lower()+":"+email.row)

        # search for terms in the body line
        temp = ""
        for char in email.body:
            if char.isalnum() or char in valid_special:
                temp += char
            else:
                if len(temp) > 2:
                    terms.append("b-"+temp.lower()+":"+email.row)
                temp = ""
        if len(temp) > 2:
            terms.append("b-"+temp.lower()+":"+email.row)
    
    for term in terms:
        t.write(term+"\n")



def main():
    f = open(sys.argv[1], "r")
    line = f.readline()

    # clear all txt files if they already exist
    t = open("terms.txt", "w")
    e = open("emails.txt", "w")
    r = open("recs.txt", "w")
    d = open("dates.txt", "w")

    while line != "":
        create_terms(line,t)
        create_emails(line,e)
        create_date(line,d)
        create_recs(line,r)
        
        line = f.readline()


    f.close()
    t.close()
    e.close()
    r.close()
    d.close()


main()
