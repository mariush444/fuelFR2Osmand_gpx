# fuelFR2Osmand_gpx

converter: from online open data with FR fuel prices to Osmand gpx with ordered prices by colors
source of data: https://donnees.roulez-eco.fr/opendata/instantane.zip

"ordered prices" means that prices for specified type of fuel are shown by colore icons from the cheapest to the most expensive:
light blue (cheapest) - from min price to min price + 5% (max price - min price)
dark green            - min price + (from  5% to 10%) of the (max price - min price)
light green           - min price + (from 10% to 20%) of the (max price - min price)
yellow                - min price + (from 20% to 30%) of the (max price - min price)
orange                - min price + (from 30% to 70%) of the (max price - min price)
red                   - min price + (from 70% to 80%) of the (max price - min price)
violet                - min price + (from 80% to 90%) of the (max price - min price)
blue navy, dark blue  - min price + 90% (max price - min price) to max price
black icon means that the type of fuel is not sold by the gas station.

black icons:
they can be switch from Osmamd view off as they are defind as separate group of icons called "Absence"
or
they can be excluded from the created file by changing variable "DOblack" from 1 to 0,
so the file will be smaller.

specified type of fuel means:
1:"Gazole"
2:"SP95"
3:"E85" 
4:"GPLc"
5:"E10" 
6:"SP98"
by changing variable "fuel" you can choose which type of fuel should be ordered by color.

variable "FilesPath" - working directory where files are downloaded, unzipped and created.

name of the waypoint (gas stetion with color) conteins:
price of the specified type of fuel
date of the price
some services provided at gas station (represented by icon that I could find in utf emoticons)

description of the waypoint contains all prices of fuels and their dates that are sold at the gas station.
