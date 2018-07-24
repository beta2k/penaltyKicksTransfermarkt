# -*- coding: utf-8 -*-
import time
import io
import sys
from bs4 import BeautifulSoup
import requests
import requests.exceptions as exceptions
import requests.packages.urllib3.exceptions as uexceptions


headers = {"User-Agent":"Mozilla/5.0"}
prefix = 'http://www.transfermarkt.co.uk'
comps = [
         'http://www.transfermarkt.co.uk/wettbewerbe/afrika']
global finished_clubs

                    
def scrapeLeagueTable(data):
    datatable = data[0].findAll('tr',class_=['odd','even'])
    for row in datatable:
        link = row.select('td table tr td:nth-of-type(2) a')
        value = row.select('td:nth-of-type(10)')[0].text
        
        league = (link[0].get('title'))
        url_competition = prefix+ link[0].get('href')
        #print(league)
        #print('-----')
        response_league = requests.get(url_competition, headers=headers)
        if ("pokalwettbewerb" in response_league.url):
            continue
        else:
            soup_league = BeautifulSoup(response_league.text, 'lxml')
            data_league = soup_league.findAll('table',class_="items") 
            for club in data_league[0].findAll('tr',class_=['odd','even']):
                link_club = club.select('td a')
                club_name = link_club[1].text
                
                if (club_name in finished_clubs):
                    print(club_name + ' already finished')
                    continue
                
                club = (link_club[0].string)
                url_club = prefix+ link_club[0].get('href')
                response_club = requests.get(url_club, headers=headers)
                soup_club = BeautifulSoup(response_club.text.encode('utf-8'), 'lxml')
                if (len(soup_club.body.findAll(text='No squad'))):
                    continue
                data_club = soup_club.findAll('table',class_="items")
                pnum=0
                clubdata= []
                players = data_club[0].findAll('tr',class_=['odd','even'])
                for player in players:
                    position = player.select('td:nth-of-type(2) table tr:nth-of-type(2) td')[0].text
                    if (position == 'Keeper'):
                        #here is the keeper
                        link_keeper = player.select('td:nth-of-type(2) table tr td:nth-of-type(2) div span a')
                        keeper = (link_keeper[0].get('title'))
                        url_keeper = prefix + link_keeper[0].get('href')
                        if 'profil' in url_keeper:
                            url_keeper = url_keeper.replace('profil','elfmeterstatistik')
                        else:
                            url_keeper = url_keeper.replace('nationalmannschaft','elfmeterstatistik')
                        response_keeper = requests.get(url_keeper, headers=headers)
                        soup_keeper = BeautifulSoup(response_keeper.text, 'lxml')
                        data_saved = soup_keeper.findAll('a',{"name" : "gehalten"})[0].text
                        data_saved = (data_saved.split("total",1)[1].strip())
                        data_not_saved = soup_keeper.findAll('a',{"name" : "nicht_gehalten"})[0].text
                        data_not_saved = (data_not_saved.split("total",1)[1].strip())
                        entry = league+','+value+','+club_name+','+url_keeper.split("spieler/",1)[1]+','+position+','+keeper+','+data_saved+','+data_not_saved
                        #print(entry)
                        clubdata.append(entry)
                    else:
                        #here is the rest
                        link_rest = player.select('td:nth-of-type(2) table tr td:nth-of-type(2) div span a')
                        rest = (link_rest[0].get('title'))
                        url_rest = prefix + link_rest[0].get('href')
                        if 'profil' in url_rest:
                            url_rest = url_rest.replace('profil','elfmetertore')
                        else:
                            url_rest = url_rest.replace('nationalmannschaft','elfmetertore')
                        response_rest = requests.get(url_rest, headers=headers)
                        soup_rest = BeautifulSoup(response_rest.text, 'lxml')
                        data_scored = soup_rest.findAll('a',{"name" : "tore"})[0].text
                        data_scored = (data_scored.split("total",1)[1].strip())
                        data_not_scored = soup_rest.findAll('a',{"name" : "verschossen"})[0].text
                        data_not_scored = (data_not_scored.split("total",1)[1].strip())
                        entry = league+','+value+','+club_name+','+url_rest.split("spieler/",1)[1]+','+position+','+rest+','+data_scored+','+data_not_scored
                        #print(entry)
                        clubdata.append(entry)
                    pnum=pnum+1
                    if (pnum == len(players)):
                        print(club_name+' finished. writing data...')
                        with io.open('data2.txt', 'a',encoding='utf8') as datafile:
                            for item in clubdata:
                                datafile.write("%s\n" % item)
                        with io.open('clubs2.txt', 'a',encoding='utf8') as clubfile:
                            clubfile.write(club_name+'\n')
                        

if __name__ == "__main__":
    done=False
    while not done:
        try:   
            try:
                with io.open('clubs2.txt', 'r',encoding='utf8') as f:
                    finished_clubs = f.read().splitlines()
            except:
                finished_clubs = []

            for competition in comps:
                url = competition
                print(url+' - '+time.strftime("%H:%M:%S"))
                #print('---')
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')
                data = soup.findAll('table',class_="items")
                scrapeLeagueTable(data)
                #iterate through pages
                #load next page
                nextPage = True
                pageSoup = soup
                pageData = None
                next_page_link = ''
                while nextPage:
                    next_page_button = pageSoup.findAll('li',class_="naechste-seite")
                    if len(next_page_button) == 0:
                        break
                    old_page_link = next_page_link
                    next_page_link = prefix + next_page_button[0].select('a')[0].get('href')
                    if(old_page_link == next_page_link):
                        break
                    print(next_page_link+' - '+time.strftime("%H:%M:%S"))
                    page_response = requests.get(next_page_link, headers=headers)
                    pageSoup = BeautifulSoup(page_response.text, 'lxml')
                    pagedata = pageSoup.findAll('table',class_="items")
                    scrapeLeagueTable(pagedata)
        except (TimeoutError,TypeError,exceptions.RetryError,exceptions.ConnectionError,
                exceptions.Timeout,exceptions.ConnectTimeout,exceptions.ChunkedEncodingError,
                uexceptions.ProtocolError) as e:
            print('Exception! New Try..')
            print(e)
#         except:
#             print('Other Exception! New Try..')
#             print(sys.exc_info()[0])
        else:
            done=True
            print('Finished')