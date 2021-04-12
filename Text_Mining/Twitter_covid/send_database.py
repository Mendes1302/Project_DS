from geopy.geocoders import Nominatim
from pymongo import MongoClient
import psycopg2
import pymongo
import re


# Variables of control  
con = cur = None
count = 0     
control = ["BRASIL", "BRAZIL", "AC","AL",
            "AP","AM","BA","CE","ES","GO",
            "MA","MT","MS","MG","PA","PB",
            "PR","PE","PI","RJ","RN","RS",
            "RO","RR","SC","SP","SE","TO","DF"]



def connect():
    con = psycopg2.connect(database='covid_brazil', user='postgres',
            password='admin', host='localhost')
    cur = con.cursor()
    return con, cur


def anti_emoji(txt):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',txt)


def eliminate_outliers(txt):
    for c in control:
        if c in txt:
            txt = txt.replace(c, "").replace("/", "")
            break
    if len(str(txt.strip())) < 25:
        # Remove emoji
        txt = anti_emoji(txt)
        return txt.replace(",", "").replace(".", "")
    return 0


while (1):
    try:

        

        # MongoDB access
        cluester = MongoClient("your_mongodb+srv")
        geolocator = Nominatim(user_agent="my_user_agent")

        db = cluester["Twitter"]
        mycol = db["Covid_in_Brazil"]

        # Get MongoDB data 
        for x in mycol.find():
            
            # Function called to clean and eliminate outliers
            txt = eliminate_outliers(x["location"])
            if txt != 0:
                try:
                    # Get latitude and longitude
                    loc = geolocator.geocode(txt+","+"Brasil")

                    # Brazil's maximum and minimum latitude and longitude filter. Example: 'oiapoque ao chuí'/ 'Serra Contamana a Ponta do Seixas'
                    if loc.latitude != None and loc.longitude != None:
                        if loc.latitude < 4.0 and loc.latitude > -34.00:
                            if loc.longitude > -74.0 and loc.longitude < -33.00:
                                count += 1

                                # Monitoring and control
                                print(count, txt, len(txt))

                                # Added to the PostgreSQL database
                                cur.execute("INSERT INTO city(name, lat, lon) VALUES('{}', {}, {});".format(txt,loc.latitude, loc.longitude))
                                con.commit()
                

                except Exception as error:
                    print(error)

                    # If disconnection occurs with PostgreSQL, reconnect 
                    x = connect()
                    con = x[0]
                    cur = x[1]
                    continue

            else:
                x = connect()
                con = x[0]
                cur = x[1]
        print("Success!!")
        break    

    except Exception as e:
        print(e)
        continue

    finally:

        if con:
            con.close()