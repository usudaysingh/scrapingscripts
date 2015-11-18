"""
This script is to scrap data from webpage we have downloaded and stored in location.
"""
from bs4 import BeautifulSoup
import urllib2
from subprocess import call
from datetime import date
import redis
import requests
import base64
import random
import tinys3
import time
import MySQLdb
import hashlib
import sys
from os import listdir
from os.path import isfile, join
import os
import json
from requests.auth import HTTPProxyAuth
from functools import wraps
from operator import add, sub, mul, div
import re
import json
import unicodedata
import glob
import os.path

local_save_dir = "/home/udaysingh/"  
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

conn = MySQLdb.connect(host= "localhost", user="root", passwd="udaysingh", db="FIR",charset="utf8")
m = conn.cursor()

transfer_date=[]
from_courtjudge=[]
to_courtjudge=[]
petitioner=[]
respondent=[]
judgename=[]
hearing_date=[]
business_date=[]
order_detail=[]
purpose_of_hearing=[]
order_date=[]
hj=0
path='/home/udaysingh/Desktop/docs_test/'		#location path
for filename in glob.glob(os.path.join(path, '*.html')):	#to open html files from location
    print hj
    print filename
    doc=open(filename)
    soup=BeautifulSoup(doc,'html.parser')
    #print soup
    div= soup.find_all("div")
    if(div==[]):
        print "it does not contain div"
    else:    
        span1=div[2].find_all('span')

    #for link in span1:
        #print link.text +str(i)

        #print span1[1].text.split(":",1)[1].replace(" ","")                             #casetype
        case_type=span1[1].text.split(":",1)[1].replace(" ","")
        print "case type is"+case_type
        #print span1[3].text.split("F",2)[1].split(":",1)[1]                             #filling code
        filing_code=span1[3].text.split("F",2)[1].split(":",1)[1]
        print "filing_code is"+filing_code
        #print span1[3].text.split("F",2)[2].split(":",1)[1]                             #filing date
        filing_date=span1[3].text.split("F",2)[1].split(":",1)[1]
        print "filing date is"+filing_date
        #print span1[6].text.split("R",2)[1].split(":",1)[1]                             #Registration number
        registration_number=span1[6].text.split("R",2)[1].split(":",1)[1]
        print "registration number is"+registration_number
        #print span1[6].text.split("R",2)[2].split(":",1)[1]                             #Registration date
        registration_date=span1[6].text.split("R",2)[2].split(":",1)[1]
        print "registration date is"+registration_date
        #print span1[9].text.split(":",1)[1]                                             #Case Code
        case_code=span1[9].text.split(":",1)[1]
        print "case code is"+case_code   


        span2=div[3].find_all('span')
        if(span2==[]):
            print "it does not contain hearing block"
        else:        
            #print span2
            #for link in span2:
            #    print link.text.split(":",1)[1]

            first_hearing_date=span2[0].text.split(":",1)[1]                                             #First Hearing Date
            print "first hearing date"+first_hearing_date
            decision_date=span2[1].text.split(":",1)[1]                                             #Decison Date
            print decision_date
            case_status=span2[2].text.split(":",1)[1]                                             #Case Status
            print case_status
            disposal= span2[3].text.split(":",1)[1]                                             #Nature of Disposal
            print disposal
            try:
                court_judge= span2[4].text.split(":",1)[1]                                             #Court No. and Judge
                print court_judge
            except:
                print "it does not contain court number and judge"
                court_judge="it does not contain"    

        span3=div[4].find_all('span')
        if(span3==[]):
            print "it does not contain divs"
            petitioner.append("it does not contain")
            respondent.append("it does not contain")
        else:
            #print span3
            x=0
            while x<len(span3):                                                              #Petitioner and Advocate
                print span3[x].text                                                            #Respondent and Advocate
                if(x==1):
                    petitioner.append(span3[x].text)
                    print "petitioner is"+span3[x].text
                if(x==2):
                    respondent.append(span3[x].text)  
                    print "respondent is"+ span3[x].text
                x+=1      

    act=soup.find("span",{"class":"Acts_table"})
    if(act==None):
        print "it does noy contain act table"
        under_act=" it does not contain act table"
        under_section="it does not contain section table"
    else:
        print "it is act table"  
        under_act= act.text.split(":",2)[1].split("U",1)[0]                                  #Under Act
        print under_act
        try:
            under_section=act.text.split(":",2)[2]                                               #Under Section
            print under_section
        except:
            print "it does not contain under section" 
            under_section="it does not contain"   

    div1=soup.find("div",{"style":" width:700px;"})
    if(div1==None):
        print "it does not contain FIR block"
        fir_number="it does not contain FIR block"
        year="it does not contain FIR block"
        police_station="it does not contain FIR block"
    else:    
        span3=div1.find_all('span')
        print span3
        e=0
        while e<1:
            try:
                fir_number= span3[e].text.split("F",1)[1].split(":",2)[1].split("Y",1)[0]        #FIR Number
                print "fir_number is" + fir_number
            except:
                print "it does not conatin FIR numbe"
            try:        
                year= span3[e].text.split("F",1)[1].split(":",2)[2]                        #YEAR
                print "year of FIR is" + year
            except:
                print "it does not contain year"
            try:            
                police_station=span3[e].text.split("F",1)[0].split(":",1)[1]                        #POLICE Station
                print "police station is"+ police_station
            except:
                print "it does not contain name of police station"    
                police_station="it does not contain name of police station"
            e+=1 
            
    table=soup.find_all("table",{"width":"700px"})
    if(table==[]):
        print "it does not contain tables"
        judgename.append("it is not present")
        business_date.append("it is not present")
        purpose_of_hearing.append("it is not present")        
    else: 
        nuber1=len(table[0].find_all('tr'))
        hearing=table[0].find_all('tr')
        nmbr2=len(table[1].find_all('tr'))
        #print nuber1
        #print nmbr2
        k=nuber1-(nmbr2+1)
        print "hearing table found"
        l=1
        while l<k:
            print l
            td=hearing[l].find_all('td')
            print "in hearing table"
            i=0
            while i<5:
                data=td[i].getText()
                #print data
                if(i==0):
                    print "Registration number is same" 
                elif(i==1):
                    judgename.append(td[i].getText())                                           #judgename
                    print td[i].getText()
                    if(td[i].getText()==""):
                        print "it does not contain judgename"
                elif(i==2):
                    business_date.append(td[i].getText())                                        #businesdate
                    print "business_date is " +td[i].getText()
                    if(td[i].getText()==""):
                        print "it does not contain business date"
                elif(i==3):
                    hearing_date.append(td[i].getText())                                         #hearingdate
                    print "hearingdate is" +td[i].getText()
                    if(td[i].getText()==""):
                        print "it does not contain hearing date"
                elif(i==4):
                    purpose_of_hearing.append(td[i].getText())                                  #purpose of hearing
                    print "purpose_of_hearing is "+td[i].getText()
                    if(td[i].getText()==""):
                        print "it does not contain purpose of hearing"
                i+=1
            l+=1

          
        order=table[1].find_all('tr')                                                   #order table
        if(order==None or order==[]):
            print " it does not contain order table"
            order_date.append("it is not present")
            order_detail.append("it is not append")
            
        else:    
            q=1
            while q<len(order):
                print q
                td1=order[q].find_all('td')                                             
                t=1
                while t<3:
                    print td1[t].getText()
                    if(t==1):
                        order_date.append(td1[t].getText())                                      #order date
                        print "orderdate is " +td1[t].getText()
                    if(t==2):
                        order_detail.append(td1[t].a.get('href'))                                #order detail
                        print "orderdetail is" +td1[t].a.get('href')
                    t+=1
                q+=1     

        try:
            transfer=table[4].find_all('tr')
            if(transfer==None or transfer==[]):
                print "it does not contain transfer table"
                transfer_date.append("it is not present")
                from_courtjudge.append("it is noty present")
                to_courtjudge.append("it is not present")
                
            else:    
                #print transfer
                w=1
                while w<len(transfer):
                    #print w
                    td2=transfer[w].find_all('td')
                    z=0
                    while z<4:
                        print td2[z].getText()
                        if(z==0):
                            print "registration number is same"
                        if(z==1):
                            transfer_date.append(td2[z].getText())                                   #transferdate
                        if(z==2):
                            from_courtjudge.append(td2[z].getText())                                 #fromcourtjudge
                        if(z==3):
                             to_courtjudge.append(td2[z].getText())                                  #to court judge             
                        z+=1
                    w+=1     
        except:
            print "it does not contain transfer table"                
        hj+=1
        
        json_transfer_date=json.dumps(transfer_date)
        json_from_courtjudge=json.dumps(from_courtjudge)
        json_to_courtjudge=json.dumps(to_courtjudge)
        json_petitioner=json.dumps(petitioner)
        json_respondent=json.dumps(respondent)
        json_judgename=json.dumps(judgename)
        json_hearing_date=json.dumps(hearing_date)
        json_business_date=json.dumps(business_date)
        json_order_detail=json.dumps(order_detail)
        json_purpose_of_hearing=json.dumps(purpose_of_hearing)
        json_order_date=json.dumps(order_date)
        
        
        try:
            m.execute('''Insert into cases(case_type,filing_code,filing_date,registration_number,\
            registration_date,case_code,decision_date,case_status,disposal,court_judge,petitioner,\
            under_act,under_section,fir_number,year,police_station,transfer_date,from_courtjudge,respondent,judgename,\
            hearing_date,business_date,order_detail,purpose_of_hearing,order_date) Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(case_type,filing_code,filing_date,registration_number,\
            registration_date,case_code,decision_date,case_status,disposal,court_judge,petitioner,under_act,under_section,fir_number,\
            year,police_station,json_transfer_date,json_from_courtjudge,json_respondent,json_judgename,\
            json_hearing_date,json_business_date,json_order_detail,json_purpose_of_hearing,json_order_date))
            print "inserted"
            conn.commit()
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)

               
        
                    
