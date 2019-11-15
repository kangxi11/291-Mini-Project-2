from bsddb3 import db

def searchTerms(subj, body):
    DB_File = "te.idx"
    database = db.DB()
    database.open(DB_File)
    cur = database.cursor()

    subj_rows = []
    body_rows = []

    if subj is not None:
        if '%' not in subj:
            query = 's-'+subj
            iter = cur.set(query.encode("utf-8"))

            if iter is not None:
                while iter[0].decode("utf-8").find(query) != -1:
                    subj_rows.append(iter[1].decode("utf-8"))
                    iter = cur.next()
        else:
            query = 's-'+subj[:-1]
            iter = cur.set_range(query.encode("utf-8"))
            
            while iter[0].decode("utf-8")[:len(query)].find(query) != -1:
                subj_rows.append(iter[1].decode("utf-8"))
                iter = cur.next()



    if body is not None:
        if '%' not in body:
            query = 'b-'+body
            iter = cur.set(query.encode("utf-8"))

            if iter is not None:
                while iter[0].decode("utf-8").find(query) != -1:
                    body_rows.append(iter[1].decode("utf-8"))
                    iter = cur.next()
        else:
            query = 'b-'+body[:-1]
            iter = cur.set_range(query.encode("utf-8"))
            
            while iter[0].decode("utf-8")[:len(query)].find(query) != -1:
                body_rows.append(iter[1].decode("utf-8"))
                iter = cur.next()
    cur.close()
    database.close()

    if subj is not None and body is not None:
        return list(set(subj_rows) & set(body_rows))
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
            break
        if query == "output=brief":
            setting = 0
            continue
        if query == "output=full":
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
            temp_que.append(result.pop(0))

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
                    for comp in comparators:
                        if result[0].find(comp) != -1:
                            sign = comp
                if sign == None:
                    sign = ":"

                # now append the query to the master list
                temp_que[0] = "date"
                temp_que.append(sign)
                # next element is just the sign
                for comp in comparators:
                    if result[0] == comp:
                        result.pop(0)
                        temp_que.append(result.pop(0))
                        
            queries.append(temp_que)
        
        print(queries)


        for word in result:
            first = False
            # get next word
            if result.index(word) != len(result)-1:
                next_word = result[result.index(word)+1]
            # get previous word
            if result.index(word) != 0:
                prev_word = result[result.index(word)-1]
            # set flag for first word
            else:
                first = True
            # check if word is to, from, cc or bcc
            if word in emailPrefixes:
                returns = searchEmails(word, next_word)
                # if its the first return put it in rows
                if first:
                    rows = returns
                # else intersect returns with rows
                else:
                    rows = rows & returns
            # check if word is subj or body
            elif word in termPrefixes:
                returns = searchTerms(word, next_word)
                # if its the first return put it in rows
                if first:
                    rows = returns
                # else intersect returns with rows
                else:
                    rows = rows & returns
            # check if word is date
            elif word[:4] == "date":
                # daniel handles all the different cases
                continue
            # word is not a prefix
            else:
                # word is < > <= >= or =
                if word in comparators:
                    continue
                # word is part of email or term query
                elif prev_word in emailPrefixes or prev_word in termPrefixes:
                    continue
                # word is part of date query
                elif "date" in prev_word or prev_word in comparators:
                    continue
                # word is a term to search for in subj and body fields
                else:
                    print(word)
                    # ryan implements this part
                    continue

        # get output from records index and print
        output = searchRecords(rows)
        # print full output
        if setting:
            print(output)
        # print brief output
        else:
            for x in output:
                print(x)
        # we'll deal with the correct printing later



main()
