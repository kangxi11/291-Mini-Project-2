from bsddb3 import db

def searchEmails(field, email):
    print("field is", field)
    print("email is", email)

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
        comparators = ["=", "<=", ">=", "<", ">"]
        rows = []

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
        for word in result:
            # get next word
            if result.index(word) != len(result)-1:
                next_word = result[result.index(word)+1]
            # get previous word
            if result.index(word) != 0:
                prev_word = result[result.index(word)-1]
            # check if word is to, from, cc or bcc
            if word in emailPrefixes:
                returns = searchEmails(word, next_word)
                rows.append(returns)
            # check if word is subj or body
            else if word in termPrefixes:
                returns = searchTerms(word, next_word)
                rows.append(returns)
            # check if word is date
            else if word[:4] == "date":
                # daniel handles all the different cases
            # word is not a prefix
            else:
                # word is < > <= >= or =
                if word in comparators:
                    continue
                # word is part of email or term query
                else if prev_word in emailPrefixes or prev_word in termPrefixes:
                    continue
                # word is part of date query
                else if "date" in prev_word or prev_word in comparators:
                    continue
                # word is a term to search for in subj and body fields
                else:
                    # ryan implements this part

            # get output from records index and print
            output = searchRecords(rows)
            # print full output
            if setting:
                print(output)
            # print brief output
            else:
                print(output)
            # we'll deal with the correct printing later
            # clear rows list
            rows = []



main()
