import urllib.request, json, atexit

key = []
cities = []
queries = []
try:
    keyFile = open('keys.txt', 'r')
    for line in keyFile:
            key.append(line.rstrip())
except FileNotFoundError:
    print("keys.txt not found!")
    sys.exit()

try:
    citiesFile = open('cities.txt', 'r')
    for line in citiesFile:
            cities.append(line.rstrip())
except FileNotFoundError:
    print("cities.txt not found!")
    sys.exit()

try:
    queriesFile = open('queries.txt', 'r')
    for line in queriesFile:
            queries.append(line.rstrip())
except FileNotFoundError:
    print("queries.txt not found!")
    sys.exit()

def penetrate(thetoken, theattorneys, itr):
    newattorneys = theattorneys
    if(itr >= len(key)):
        print("exhausted api keys")
        print("ended on " + city)
        exit_handler()
        exit()
    with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/textsearch/json?key=" + key[itr] + "&pagetoken=" + thetoken) as url:
       data = json.loads(url.read().decode())
    if data['status'] != "OK":
        if data['status'] == "OVER_QUERY_LIMIT" or data['status'] == "INVALID_REQUEST" or data['status'] == "ZERO_RESULTS":
            return theattorneys
        else:
            print(url.geturl())
            print(data)
            print(data['status'])
            exit()
    if 'next_page_token' in data:
        newattorneys = penetrate(data['next_page_token'], newattorneys, itr)
    else:
        print("successfully exhausted pages")
    newleads = []
    for i in data['results']:
        rating = ""
        if 'rating' not in i:
            continue
        rating = str(i['name']) + ": " + str(i['rating'])
        if i['rating'] <= 3 and i['place_id'] not in newattorneys:
            newattorneys.append(i['place_id'])
            with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/details/json?key=" + key[itr] + "&placeid=" + i['place_id']) as url:
                rawplacedata = json.loads(url.read().decode())
            if 'lawyer' not in rawplacedata['result']['types']:
                continue
            if 'formatted_phone_number' in rawplacedata['result']:
                rating = rating + ", " + rawplacedata['result']['formatted_phone_number']
            try:
                print(rating)
                print(i['place_id'])
                newleads.append(i['place_id'] + "\n")
            except ValueError:
                #fnewleads.append(i['place_id'] + " ~x" + "\n")
                print("Err on + " + i['place_id'] + " adding print exception")
    fh = open("leads.txt", "a")
    print("successfully penetrated")
    fh.writelines(newleads)
    fh.close()
    return newattorneys

def leadgen():
    attorneys = []
    itr = 0
    afh = open("leads.txt", "r")
    for lawyer in afh:
        if(len(lawyer) == 28):
            lawyer = lawyer[:-1]
        attorneys.append(lawyer)
    afh.close()

    def exit_handler():
        print("Handling exit ;)")
    atexit.register(exit_handler)
    for city in cities:
        for query in queries:            
            if(itr >= len(key)):
                print("exhausted api keys")
                print("ended on " + city)
                exit_handler()
                exit()
            try:
                with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + query.replace(' ', '%20') + "%20" + city.replace(' ', '%20') + "&key=" + key[itr]) as url:
                   data = json.loads(url.read().decode())
            except:
                continue
            if data['status'] != "OK":
                if data['status'] == "OVER_QUERY_LIMIT":
                    old = itr
                    itr = itr + 1
                    print("key " + str(old) + " over-extended, moving to key: " + str(itr))
                elif data['status'] == "ZERO_RESULTS":
                    print("zero results for: " + query)
                    continue
                else:
                    print(url.geturl())
                    print(data)
                    print(data['status'])
                    exit()
            if 'next_page_token' in data:
                attorneys = penetrate(data['next_page_token'], attorneys, itr)
            newleads = []
            for i in data['results']:
                rating = ""
                if 'rating' not in i:
                    continue
                rating = str(i['name']) + ": " + str(i['rating'])
                if i['place_id'] not in attorneys:
                    attorneys.append(i['place_id'])
                    try:
                        with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/details/json?key=" + key[itr] + "&placeid=" + i['place_id']) as url:
                            rawplacedata = json.loads(url.read().decode())
                    except:
                        continue
                    if 'lawyer' not in rawplacedata['result']['types']:
                        continue
                    if 'formatted_phone_number' in rawplacedata['result']:
                        rating = rating + ", " + rawplacedata['result']['formatted_phone_number']
                    try:
                        print("(" + query + ", " + city + ") " + rating)
                        print(i['place_id'])
                        newleads.append(i['place_id'] + "\n")
                    except ValueError:
                        #fnewleads.append(i['place_id'] + " ~x" + "\n")
                        print("Err on + " + i['place_id'] + " adding print exception")
            fh = open("leads.txt", "a")
            fh.writelines(newleads)
            fh.close()

def tokenleadgen():
    attorneys = []
    itr = 0

    #city = input("Where? ")
    tokens = input("Token file: ")
    leadfile = input("Lead file: ")

    lf = open(leadfile, "r")
    for lead in lf:
        if(len(lead) == 28):
            lead = lead[:-1]
        attorneys.append(lead)
    lf.close()

    def exit_handler():
        print("Handling exit ;)")
    atexit.register(exit_handler)
    tf = open(tokens, "r")
    try:
        for token in tf:
            if(itr >= len(key)):
                print("exhausted api keys")
                print("ended on " + city)
                exit_handler()
                exit()
            with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/textsearch/json?key=" + key[itr] + "&pagetoken=" + token) as url:
               data = json.loads(url.read().decode())
            if data['status'] != "OK":
                if data['status'] == "OVER_QUERY_LIMIT":
                    old = itr
                    itr = itr + 1
                    print("key " + str(old) + " over-extended, moving to key: " + str(itr))
                elif data['status'] == "ZERO_RESULTS":
                    print("zero results for: " + practice)
                    continue
                else:
                    print(url.geturl())
                    print(data)
                    print(data['status'])
                    exit()
            if 'next_page_token' in data:
                tokenfh = open("pagetokens.txt", "a")
                tokenfh.write(data['next_page_token'] + "\n")
                tokenfh.close()
            newleads = []
            for i in data['results']:
                rating = ""
                if 'rating' not in i:
                    continue
                rating = str(i['name']) + ": " + str(i['rating'])
                if i['rating'] <= 3 and i['place_id'] not in attorneys:
                    attorneys.append(i['place_id'])
                    with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/details/json?key=" + key[itr] + "&placeid=" + i['place_id']) as url:
                        rawplacedata = json.loads(url.read().decode())
                    if 'lawyer' not in rawplacedata['result']['types']:
                        continue
                    if 'formatted_phone_number' in rawplacedata['result']:
                        rating = rating + ", " + rawplacedata['result']['formatted_phone_number']
                    try:
                        print(rating)
                        print(i['place_id'])
                        newleads.append(i['place_id'] + "\n")
                    except ValueError:
                        #fnewleads.append(i['place_id'] + " ~x" + "\n")
                        print("Err on + " + i['place_id'] + " adding print exception")
            fh = open(leadfile, "a")
            fh.writelines(newleads)
            fh.close()
    except ValueError:
        tf.close()
    tf.close()

def call():
    dnclist = []
    leadlist = []
    thelist = input("Lead filename: ")
    itr = 0
    lfh = open(thelist, "r")
    for line in lfh:
        if(len(line) >= 28):
            line = line[:-1]
        if(len(line) > 27):
            print("throwing exception for accepted error on: " + line) #come back to this later
        else:
            leadlist.append(line)
    lfh.close()
    old = open("DNC.txt", "r")
    for line in old:
        if(len(line) == 28):
            line = line[:-1]
        dnclist.append(line)
    old.close()
    dnc = open("DNC.txt", "a+")
    for lead in leadlist:
        if lead in dnclist:
            continue
        ready = input("Ready for a new lead? ")
        if ready == "no":
            print("Giving you one anyway")
        elif ready == "end" :
            dnc.close()
            exit()
        else:
            print("Here ya go:")
        with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/details/json?key=" + key[itr] + "&placeid=" + lead) as url:
            placedata = json.loads(url.read().decode())
        if placedata['status'] != "OK":
            if placedata['status'] == "OVER_QUERY_LIMIT":
                olditr = itr
                itr = itr + 1
                if itr > len(key) - 1:
                    print("exhausted all keys")
                    dnc.close()
                    exit()
                print("key " + str(olditr) + " over-extended, moving to key: " + str(itr))
                with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/details/json?key=" + key[itr] + "&placeid=" + lead) as url:
                    placedata = json.loads(url.read().decode())
            else:
                print(url.geturl())
                print(placedata)
                print(placedata['status'])
                dnc.close()
                exit()
        theogdata = placedata['result']
        if 'lawyer' not in theogdata['types']:
            print(lead + " is not a law firm.")
            continue
        print("Firm Name:")
        print("\t" + theogdata['name'])
        print("GPID:")
        print("\t" + lead)
        if 'website' in theogdata:
            print("Website:")
            print("\t" + theogdata['website'])
        print("Phone Number:")
        print("\t" + theogdata['formatted_phone_number'])
        print("Location:")
        print("\t" + theogdata['formatted_address'])
        print("Open?")
        if 'opening_hours' not in theogdata or 'open_now' not in theogdata['opening_hours']:
            print("\tnot sure")
        elif theogdata['opening_hours']['open_now']:
            print("\tyes")
        else:
            print(theogdata['opening_hours']['open_now'])
            print("\tno")
        print("Rating:")
        print("\t" + str(theogdata['rating']))
        print("Reviews:")
        if 'reviews' not in theogdata:
            print("\tNone")
        else:
            reviews = theogdata['reviews']
            for review in reviews:
                print("\t" + review['relative_time_description'] + " " + review['author_name']+ " said:")
                print("\t" + str(review['rating']) + " star,")
                try:
                    print("\t" + review['text'])
                except ValueError:
                    print("\tI don't like emojis :(")
                print("")
        callrate = input("Would you like to call them again? ")
        if callrate == "no":
            dnc.write(lead + "\n")
            dnclist.append(lead)
            print(theogdata['name'] + " added to the DNC list")
    dnc.close()
    
def pulldata():
    itr = 0
    lead = input("Enter PlaceID: ")
    with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/details/json?key=" + key[itr] + "&placeid=" + lead) as url:
        placedata = json.loads(url.read().decode())
    if placedata['status'] != "OK":
        if placedata['status'] == "OVER_QUERY_LIMIT":
            olditr = itr
            itr += 1
            if itr > len(key) - 1:
                print("exhausted all keys")
                dnc.close()
                exit()
            print("key " + str(olditr) + " over-extended, moving to key: " + str(itr))
            with urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/details/json?key=" + key[itr] + "&placeid=" + lead) as url:
                placedata = json.loads(url.read().decode())
        else:
            print(url.geturl())
            print(placedata)
            print(placedata['status'])
            dnc.close()
            exit()
    theogdata = placedata['result']
    if 'lawyer' not in theogdata['types']:
        print(lead + " is not a law firm.")
        return
    print("Firm Name:")
    print("\t" + theogdata['name'])
    print("GPID:")
    print("\t" + lead)
    if 'website' in theogdata:
        print("Website:")
        print("\t" + theogdata['website'])
    print("Phone Number:")
    print("\t" + theogdata['formatted_phone_number'])
    print("Location:")
    print("\t" + theogdata['formatted_address'])
    print("Open?")
    if 'opening_hours' not in theogdata or 'open_now' not in theogdata['opening_hours']:
        print("\tnot sure")
    elif theogdata['opening_hours']['open_now']:
        print("\tyes")
    else:
        print(theogdata['opening_hours']['open_now'])
        print("\tno")
    print("Rating:")
    print("\t" + str(theogdata['rating']))
    print("Reviews:")
    if 'reviews' not in theogdata:
        print("\tNone")
    else:
        reviews = theogdata['reviews']
        for review in reviews:
            print("\t" + review['relative_time_description'] + " " + review['author_name']+ " said:")
            print("\t" + str(review['rating']) + " star,")
            try:
                print("\t" + review['text'])
            except ValueError:
                print("\tI don't like emojis :(")
            print("")
    
if __name__ == '__main__':
    do = input("What would you like to do: genleads, call, pulldata, or exit? ")
    if(do == "genleads"):
        if input("from tokens? ") == "yes":
            tokenleadgen()
        else:
            leadgen()
    elif(do =="call"):
        call()
    elif(do == "pulldata"):
        pulldata()
    elif(do == "exit"):
        exit()
    else:
        print("Err: " + do + "is not an option.")
