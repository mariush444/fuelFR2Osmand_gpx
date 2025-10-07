#!/usr/bin/python3
'''
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
'''
# source: https://mariush444.github.io/Osmand-tools/
# https://github.com/cbosdo/gas-price/tree/osmand


fuel="1"
DOblack=1
FilesPath="/storage/26D1-32F6/Download/dev-tmp/fuel/"

#checking
if fuel not  in {"1","2","3","4","5","6"}:
	print("fuel must be 1 or 2 or 3 or 4 or 5 or 6")
	exit()
if DOblack not in {0,1}:
	print("DOblack must be 1 or 2")
	exit()
print("Start")		
import xml.etree.ElementTree as ET
import urllib.request
from zipfile import ZipFile
import io

# downloading open data with FR fuel prices
url = "https://donnees.roulez-eco.fr/opendata/instantane"
zipF = FilesPath + "instantane.zip"

try:
    urllib.request.urlretrieve(url, zipF)
    print("File downloaded successfully.")
except urllib.error.URLError as e:
    print(f"Error downloading file: {e}")  
    
# unziping file
with ZipFile(zipF, 'r') as zip_object:
    zip_object.extract('PrixCarburants_instantane.xml',FilesPath)

# parsing    
xml_filename = FilesPath+ "PrixCarburants_instantane.xml"
root = ET.fromstring(open(xml_filename , "r",encoding="iso-8859-1" , errors='ignore').read())

fuelTAB = {1:"Gazole",
2: "SP95",
3: "E85", 
4:"GPLc",
5: "E10", 
6:"SP98"} 	
# min max prices and last date, creating order defs
Pmin=1000
Pmax=0
date=""
for station in root.findall("./pdv"):
	for price in station.findall(".//prix"):
	       	if price.get("id")==fuel:
	       		if Pmin > float(price.get("valeur")):  Pmin=float(price.get("valeur"))
	       		if Pmax < float(price.get("valeur")):  Pmax=float(price.get("valeur"))
	       		if date<price.get("maj")[0:10]: date=price.get("maj")[0:10]

Prange=round(Pmax-Pmin,3)

P0_5=round(Pmin+Prange*0.05,3)
P5_10=round(Pmin+Prange*0.1,3)
P11_20=round(Pmin+Prange*0.2,3)
P21_30=round(Pmin+Prange*0.3,3)
P31_70=round(Pmin+Prange*0.7,3)
P71_80=round(Pmin+Prange*0.8,3)
P81_90=round(Pmin+Prange*0.9,3)

GPXname=FilesPath + '🇨🇵-⛽-'+fuelTAB[int(fuel)]+'-'+("full" if DOblack==1 else  "only")+"-"+date.replace('-','')[2:8]+'.gpx'
GPXfile=open(GPXname,'w')

# creating gpx
print("<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>", file= GPXfile)
print('<gpx version="1.1" creator="OsmAnd+Maryush444" xmlns="http://www.topografix.com/GPX/1/1" xmlns:osmand="https://osmand.net" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">', file= GPXfile)
print("<metadata><name>fuel FR</name></metadata>", file= GPXfile)

for station in root.findall("./pdv"):
	name="no "+fuelTAB[int(fuel)]+" "
	desc=""
	thePrice=0
	color="000001" #black
	for price in station.findall(".//prix"):
		if price.get("id")==fuel: 
			name=price.get("nom")+" "+price.get("valeur") + " " + price.get("maj")[2:10]+" "
			thePrice=float(price.get("valeur"))		
		desc=desc+"\t"+price.get("nom")+" "+price.get("valeur") + "€ " + price.get("maj")[2:10]+"&lt;br&gt;\n"
		
	for service in station.findall(".//service"):
		if (service.text)=="Bar" : name=name+"🍴"
		if (service.text)=="Restauration sur place" : name=name+"🍴"
		if (service.text)=="Boutique alimentaire" : name=name+"🛒"
		if (service.text)=="DAB (Distributeur automatique de billets)" : name=name+"🏧"
		if (service.text)=="Douches" : name=name+"🚿"
		if (service.text)=="Espace bébé" : name=name+"🚼"
		if (service.text)=="Relais colis" : name=name+"📦"
		if (service.text)=="Services réparation / entretien" : name=name+"🛠️"
		if (service.text)=="Station de gonflage" : name=name+"𖥕"
		if (service.text)=="Toilettes publiques" : name=name+"🚻"
		if (service.text)=="Wifi" : name=name+"ᯤ"
		
	if thePrice>0 and thePrice<=P0_5: color="10c0f0"            # light blue
	if P0_5< thePrice and thePrice <=P5_10: color="00842b"      # dark green
	if P5_10< thePrice and thePrice <=P11_20: color="88e030"    # light green
	if P11_20< thePrice and thePrice <=P21_30 : color="eecc22"  # yewllow
	if P21_30< thePrice and thePrice <=P31_70: color="ff8500"   # orange
	if P31_70< thePrice and thePrice <=P71_80: color="d00d0d"   # red
	if P71_80< thePrice and thePrice <=P81_90: color="a71de1"   # violet
	if thePrice>P81_90: color="1010a0"                          # blue navy
	
	if  DOblack==1 or color!="000001":
		print(" <wpt lat=\""+str(round(float(station.get("latitude")),0)/100000)+"\" lon=\""+str(round(float(station.get("longitude")),0)/100000)+ "\">", file= GPXfile)
		print("\t<name>"+ name.strip()+"</name>", file= GPXfile)
		print("\t<desc>\n"+desc+"\t</desc>", file= GPXfile)
		if color=="000001": print("<type>Absence</type>", file= GPXfile)
		print("\t<extensions>", file= GPXfile)
		print("\t\t<osmand:color>#"+color+"</osmand:color>", file= GPXfile)
		print("\t\t<osmand:icon>fuel</osmand:icon>", file= GPXfile)
		print("\t\t<osmand:background>cirlce</osmand:background>", file= GPXfile)
		print("\t</extensions>", file= GPXfile)
		print("</wpt>", file= GPXfile)
	
print("</gpx>", file= GPXfile)

#info and descrption for user
print("File",GPXname," was created. ")
print ("The file is ordered due to the", fuelTAB[int(fuel)]+"prices")
print('''
You can change type of fuel that should be ordered at line ...
1:"Gazole",
2:"SP95",
3:"E85", 
4:"GPLc",
5:"E10", 
6:"SP98"}

Ordered due to prices means''')
print(Pmin,"-",P0_5,"blue")
print(round(P0_5+0.001,3),"-", P5_10, "dark green")
print(round(P5_10+0.001,3),"-", P11_20, "light green")
print(round(P11_20+0.001,3),"-", P21_30, "yellow")
print(round(P21_30+0.001,3),"-" , P31_70, "orange")
print(round(P31_70+0.001,3),"-",P71_80,"red")
print(round(P71_80+0.001,3),"-", P81_90,"violet") 
print(round(P81_90+0.001,3),"-",Pmax,"navy blue / dark blue" )
print("Black if "+fuelTAB[int(fuel)] +" isn't sold at station")
print(''''Black' stations are defined as group 'Absence' and they can be excluded from the view in Osmand
or they can be excluded from the file (file will be smaller) at line ... by changing the variable DOblack from 1 to 0''')
