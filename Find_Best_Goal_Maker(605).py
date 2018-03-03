import csv
from bs4 import BeautifulSoup
import requests


#write in file
def make_file(*parameter):
	file_name,mode,content=parameter
	file=open(file_name,mode,newline="")
	writer=csv.writer(file)
	writer.writerows(content)
	file.close()
	pass

player={'name':{'goal':0,'asist':0,'total':0, 'team':'tname', 'nation':'blank', 'source':'website'}}
ListOfplayer=[]

writeList=[]
writeList.append(['Name','Goal','Asist','Total Point', 'Currently Playing', 'nation', 'Source'])
make_file('Best_Goal_Maker.csv','w',writeList)
#get url 

allUrl=['http://www.espnfc.us/team/paris-saint-germain-/160/squad?league=all',
'http://www.espnfc.co.uk/club/real-madrid/86/squad?league=all','http://www.espnfc.co.uk/club/barcelona/83/squad?league=all',
'http://www.espnfc.co.uk/team/manchester-city/382/squad?league=all',
'http://www.espnfc.co.uk/team/manchester-united/360/squad?league=all',
'http://www.espnfc.co.uk/team/liverpool/364/squad?league=all',
'http://www.espnfc.co.uk/team/tottenham-hotspur/367/squad?league=all',
'http://www.espnfc.co.uk/team/chelsea/363/squad?league=all',
'http://www.espnfc.co.uk/team/arsenal/359/squad?league=all',
'http://www.espnfc.co.uk/team/leicester-city/375/squad?league=all',
'http://www.espnfc.co.uk/team/atletico-madrid/1068/squad?league=all',
'http://www.espnfc.co.uk/team/valencia/94/squad?league=all',
'http://www.espnfc.co.uk/team/bayern-munich/132/squad?season=2017&league=all',
'http://www.espnfc.co.uk/team/juventus/111/squad?league=all',
'http://www.espnfc.co.uk/team/as-monaco/174/squad?league=all',
'http://www.espnfc.co.uk/team/marseille/176/squad?league=all']

for url in allUrl:

	call=requests.get(url)
	content=call.text


	soup=BeautifulSoup(content,"html.parser")

	pga=soup('td',{"class": ( "pla","totalGoals","goalAssists")})

	getTeam=soup('div',{'class':'squad-title'})

	teams=getTeam[0].find('h1')
	team=teams.text

	count=0;
	while count<len(pga):
		name=pga[count].text
		name=name[1:len(name)-1]
		goal=int(pga[count+1].text)
		asist=int(pga[count+2].text)
		link=pga[count].find('a',href=True)
		#if 'href'in link:
		source="ESPN"
		nation='Unknown'
		if link:
			source=link['href']
			callTeam=requests.get(source)
			ContentTeam=callTeam.text
			soupTeam=BeautifulSoup(ContentTeam,'html.parser')
			Nationaltname=soupTeam('div',{"class": "player-spec"})
			if Nationaltname:
				TeamName=Nationaltname[0].find_all('dd')
				if TeamName:
					if len(TeamName)>5:
						nation=TeamName[len(TeamName)-1].text
		#else:
			
		total=goal+asist
		
		if name in player:
			player[name]['goal'] = player[name]['goal'] + goal
			player[name]['asist'] = player[name]['asist'] + asist
			player[name]['total'] = player[name]['total'] + total
			pass
		else:
			ListOfplayer.append(name)
			player[name]={}
			player[name]['goal']=goal
			player[name]['asist']=asist
			player[name]['total']=total
			player[name]['source']=source
			player[name]['team']=team
			player[name]['nation']=nation
			#writeList=[]
			#writeList.append([name,goal,asist,total,team,source])
			#make_file('FootballPlayer.csv','a',writeList)
			pass

		#print(name," : ", player[name])
		count+=3
		pass
	pass

i=0
NoPlayer=len(ListOfplayer)
while i<NoPlayer:
	j=i+1;
	while j<NoPlayer:
		p1=ListOfplayer[i]
		p2=ListOfplayer[j]
		value1=player[p1]['total']
		value2=player[p2]['total']
		if value2>value1:
			ListOfplayer[i]=p2
			ListOfplayer[j]=p1
			pass
		j=j+1
		pass
	i=i+1
	pass

i=0
while i<NoPlayer:
	writeList=[]
	p=ListOfplayer[i]
	v1=player[p]['goal']
	v2=player[p]['asist']
	v3=player[p]['total']
	v4=player[p]['team']
	v5=player[p]['nation']
	v6=player[p]['source']
	writeList.append([p,v1,v2,v3,v4,v5,v6])
	make_file('Best_Goal_Maker.csv','a',writeList)
	print(p," : ", player[p])
	i=i+1
	pass