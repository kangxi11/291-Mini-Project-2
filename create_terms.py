class Email(object):
    def __init__(self, row, subj, body):
        self.row = row
        self.subj = subj
        self.body = body

def main():
    f = open ("10_data.xml", "r")
    lines = f.readlines()
    emails = []

    valid_special = ["_", "-"]

    terms = []

    for line in lines:
        if line.find("<mail>") != -1:
            row = line[line.find("<row>")+5:line.find("</row>")]
            subj = line[line.find("<subj>")+6:line.find("</subj>")]
            body = line[line.find("<body>")+6:line.find("</body>")]

            emails.append(Email(row, subj, body))

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
 
    t = open("terms.txt", "w")
    for term in terms:
        t.write(term+"\n")
    f.close()
    t.close()
main()