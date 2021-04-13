# Project_DS

## Repository of projetos de Data Science. See the programming languages, OS, hardware of application, API, OSS and Frameworks used:

  - Python.
  - SQL.
  - Linux (ubuntu v20.10).
  - Raspberry Pi W Zero.
  - PostgreSQL.
  - MongoDB.
  - Grafana.
  
  


# Project 1 [Keywords about COVID-19 in Brazil via Twitter](https://github.com/Mendes1302/Projects_DS/tree/main/Text_Mining/Twitter_covid)

* ## Part I

> ### Data obtained between 30/03/2021 and 01/04/2021, more than 100 thousand data. Superficially filtered by the Portuguese language and saved in MongoDB (saving id_user for possible problems, location and text message). [See the code](https://github.com/Mendes1302/Projects_DS/blob/main/Text_Mining/Twitter_covid/get_filter_saved.py).

* ## tips:
* > ### I had trouble connecting to MongoDB Web. So, install:
        pip3 install pymongo[srv]
        
* ## Part II

> ### Excluded outliers, converted from a NoSQL database (MongoDB) to SQL (PostgreSQL), converting the city name (string) to latitude and longitude, removing emoji from the names and filtering the geographic coordinates of Brazil limiting from Oiapoque to Chuí (latitude) and Ponta do Seixas to Serra Contamana (longitude). [See the code](https://github.com/Mendes1302/Projects_DS/blob/main/Text_Mining/Twitter_covid/send_database.py).

* ## tips:
* > ### There are many outliers. Do not worry!!
* > ### I had a problem installing the grafana on the raspberry pi w zero with the [link](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/). These commands worked:
        sudo apt-get install -y adduser libfontconfig1
        wget https://dl.grafana.com/oss/release/grafana_7.5.3_amd64.deb
        sudo dpkg -i grafana_7.5.3_amd64.deb

        
        
        
        

## Result:
![image](https://github.com/Mendes1302/Projects_DS/blob/main/Text_Mining/Twitter_covid/midia/conclusion.png)


