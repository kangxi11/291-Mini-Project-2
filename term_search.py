from bsddb3 import db


def searchTerm(subj, body):
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



def main():
    
    result = searchTerm("c%", None)

    print(result)


main()