from bsddb3 import db
import datetime
import time
import sys

def searchTerms(subj, body):
    DB_File = "te.idx"
    database = db.DB()
    database.open(DB_File)
    cur = database.cursor()

    subj_rows = set()
    body_rows = set()

    if subj is not None:
        if '%' not in subj:
            query = 's-'+subj
            iter = cur.set(query.encode("utf-8"))

            if iter is not None:
                while iter[0].decode("utf-8").find(query) != -1:
                    subj_rows.add(iter[1])
                    iter = cur.next()
        else:
            query = 's-'+subj[:-1]
            iter = cur.set_range(query.encode("utf-8"))
            
            while iter[0].decode("utf-8")[:len(query)].find(query) != -1:
                subj_rows.add(iter[1])
                iter = cur.next()



    if body is not None:
        if '%' not in body:
            query = 'b-'+body
            iter = cur.set(query.encode("utf-8"))

            if iter is not None:
                while iter[0].decode("utf-8").find(query) != -1:
                    body_rows.add(iter[1])
                    iter = cur.next()
        else:
            query = 'b-'+body[:-1]
            iter = cur.set_range(query.encode("utf-8"))
            
            while iter[0].decode("utf-8")[:len(query)].find(query) != -1:
                body_rows.add(iter[1])
                iter = cur.next()
    cur.close()
    database.close()

    if subj is not None and body is not None:
        return subj_rows | body_rows
    elif subj is None and body is not None:
        return body_rows
    elif subj is not None and body is None:
        return subj_rows

# returns a list of key value pairs specified by row keys in rows
def searchRecords(rows):
    database = db.DB()
    database.open("re.idx")
    cur = database.cursor()
    output = []

    if rows is not None:
        for row in rows:
            iter = cur.set(row)
            # add key value pair to output
            output.append(iter)
    
    return output
   
# returns a set of row values associated with given field-email key
def searchEmails(field, email):
    database = db.DB()
    database.open("em.idx")
    cur = database.cursor()
    key = field + "-" + email
    rows = set()
    iter = cur.set(key.encode("utf-8"))
    while iter:
        rows.add(iter[1])
        iter = cur.next_dup()
    return rows

def searchDates(date_t, sign):
    database = db.DB()
    database.open("da.idx")
    cur = database.cursor()

    date = datetime.datetime.strptime(date_t, '%Y/%m/%d')

    rows = set()


    if sign == "<":
        #Find all emails that are older than date; Start from oldest --> current
        iter = cur.first()
        while datetime.datetime.strptime(iter[0].decode("utf-8"), '%Y/%m/%d') < date:
            rows.add(iter[1])

            iter = cur.next()
            if iter == None:
                break
        return rows
    elif sign == "<=":
        #Find all emails that are older than date, INCLUDING
        iter = cur.first()
        while datetime.datetime.strptime(iter[0].decode("utf-8"), '%Y/%m/%d') <= date:
            rows.add(iter[1])
            iter = cur.next()

            if iter == None:
                break
        return rows
    elif sign == ">":
        #Find all emails that are more recent than date; Start from current --> end

        # edge case:
        iter = cur.last()
        if datetime.datetime.strptime(iter[0].decode("utf-8"), '%Y/%m/%d') <= date:
            return rows

        iter = cur.set(date_t.encode("utf-8"))

            # have to find the first date that is valid
        date2 = date
        while iter is None:
            date2 += datetime.timedelta(days = 1)
            iter = cur.set(date2.strftime('%Y/%m/%d').encode("utf-8"))
        
        # because > is not inclusive we have to find the next date
        while datetime.datetime.strptime(iter[0].decode("utf-8"), '%Y/%m/%d') == date:
            iter = cur.next()
        
        while iter != None:
            rows.add(iter[1])
            iter = cur.next()

        return rows
    elif sign == ">=":
        #Find all emails that are more recent than date; Start from current --> end

        # edge case:
        iter = cur.last()
        if datetime.datetime.strptime(iter[0].decode("utf-8"), '%Y/%m/%d') < date:
            return rows

        iter = cur.set(date_t.encode("utf-8"))

            # have to find the first date that is valid
        date2 = date
        while iter is None:
            date2 += datetime.timedelta(days = 1)
            iter = cur.set(date2.strftime('%Y/%m/%d').encode("utf-8"))
                
        while iter != None:
            rows.add(iter[1])
            iter = cur.next()
            
        return rows
    else:
        if sign != ":":
            raise AssertionError("Not a valid comparator operative")
        else:
            iter = cur.set(date_t.encode("utf-8"))

            if (iter is None) or (datetime.datetime.strptime(iter[0].decode("utf-8"), '%Y/%m/%d') != date):
                return

            while datetime.datetime.strptime(iter[0].decode("utf-8"), '%Y/%m/%d') == date:
                rows.add(iter[1])
                iter = cur.next()
            return rows

def main():
    print("\nWelcome to the information retrieval system.")
    print("You may enter queries to retrieve records from the database.")
    print("Your queries will output the row id and the subject field of all matching records.")
    print("If you want to change the output to the full record, enter \"output=full\".")
    print("To change back to the default output, enter \"output=brief\".")
    print("To exit the system, enter \"exit\".\n")

    # 0 for brief output and 1 for full output
    setting = 0

    while True:
        query = input("Please enter your query: ")
        result = []
        emailPrefixes = ["from", "to", "cc", "bcc"]
        termPrefixes = ["subj", "body"]
        comparators = ["<", ">","<=", ">=",]
        rows = set()

        queries = []

        if query == "exit":
            print("Exiting.")
            break
        if query == "output=brief":
            setting = 0
            print("Output changed to brief.")
            continue
        if query == "output=full":
            print("Output changed to full.")
            setting = 1
            continue
        # split the query by whitespace and colons
        for x in query.split():
            for y in x.split(":"):
                if y != "":
                    result.append(y)

        # handle the query
        while result != []:
            temp_que = []
            temp2 = None
            temp_que.append(result.pop(0))
            date = None
            d_temp = None

            if temp_que[0] in emailPrefixes or temp_que[0] in termPrefixes:
                temp_que.append(result.pop(0))
            elif temp_que[0].find("date") != -1:
                # find the inequality sign
                # sign is either in [0] or the next element
                sign = None
                for comp in comparators:
                    if temp_que[0].find(comp) != -1:
                        sign = comp
                if sign == None:
                    temp2 = result.pop(0)
                    for comp in comparators:
                        if temp2.find(comp) != -1:
                            sign = comp
                if sign == None:
                    sign = ":"

                # find the date we are trying to find
                # the date is either in temp_que[0], temp2, or result[0]

                if temp_que[0].find("/") != -1:
                    date = temp_que[0][len(sign)+4:]
                elif temp2 is not None and temp2.find("/") != -1:
                    if sign is not ":":
                        date = temp2[len(sign):]
                    else:
                        date = temp2
                else:
                    date = result.pop(0)

                # now find the date we are trying to find
                temp_que[0] = "date"
                temp_que.append(sign)
                temp_que.append(date)

            queries.append(temp_que)
        
        # initialize final row set
        rows = set()
        for t_que in queries:
            first = False
            # set flag if query is the first query
            if not rows:
                first = True
            if t_que[0] in emailPrefixes:
                returns = searchEmails(t_que[0], t_que[1])
                # if its the first return put it in rows
                if first:
                    rows = returns
                # else intersect returns with final row set
                else:
                    rows = rows & returns
            # check if word is date
            elif t_que[0] is "date":
                returns = searchDates(date, sign)
                # if its the first return put it in rows
                if first:
                    rows = returns
                # else intersect returns with final row set
                else:
                    rows = rows & returns
            # word is not a prefix
            else:
                if t_que[0] == "subj":
                    returns = searchTerms(t_que[1], None)
                elif t_que[0] == "body":
                    returns = searchTerms(None, t_que[1])
                else:
                    returns = searchTerms(t_que[0], t_que[0])

                if first:
                    rows = returns
                # else inersect returns with final row set
                else:
                    rows = rows & returns
        # get output from records index and print
        output = searchRecords(rows)
        if not output:
            print("Query did not match any records.")
            continue
        # print full output
        if setting:
            for pair in output:
                print("Row ID: ", pair[0].decode("utf-8"))
                # perhaps change this to be more visually appealing
                print("Full record: ", pair[1].decode("utf-8"))
        # print brief output
        else:
            print ("Row ID     | Subject Field\n")
            for pair in output:
                subj = pair[1].decode("utf-8")
                subj = subj[subj.find("<subj>")+6:subj.find("</subj>")]
                print(pair[0].decode("utf-8").ljust(10,' '), ' ', subj)



main()
