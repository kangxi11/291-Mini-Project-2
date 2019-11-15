from bsddb3 import db


def searchTerm(subj, body):
    DB_File = "te.idx"
    database = db.DB()
    database.open(DB_File)
    cur = database.cursor()

    subj_rows = []
    body_rows = []

    if subj is not None:
        query = 's-'+subj
        iter = cur.set(query.encode("utf-8"))

        if iter is not None:
            while iter[0].decode("utf-8").find(query) != -1:
                subj_rows.append(iter[1].decode("utf-8"))
                iter = cur.next()

    if body is not None:
        query = 'b-'+body
        iter = cur.set(query.encode("utf-8"))

        if iter is not None:
            while iter[0].decode("utf-8").find(query) != -1:
                body_rows.append(iter[1].decode("utf-8"))
                iter = cur.next()
    cur.close()
    database.close()

    return list(set(subj_rows) & set(body_rows))



def main():
    
    result = searchTerm("check", "the")

    print(result)


main()