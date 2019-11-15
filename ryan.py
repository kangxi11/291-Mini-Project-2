from bsddb3 import db
DB_File = "te.idx"
database = db.DB()
database.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
database.open(DB_File,None, db.DB_BTREE, db.DB_CREATE)
cur = database.cursor()

iter = cur.first()

while(iter):
    print(iter)
    iter = cur.next()
