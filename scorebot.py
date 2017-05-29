import sys
import time, threading
import random, string

from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates', static_folder="static")

# Start-import-Services
sys.path.insert(0, './services/')

import textfilestore
import tweetybird
import nadmozg
import piratemap
import redmessanger
import ropeman
import blackgold
import sharing
import hanoifones
import FHMMaintenance
import hacker_diary

# End-import-Services

class Game:
	def __init__(self, teams, services):
		self.teams = teams
		self.services = services

	def getFlags(self):
		for service_name, service in services.iteritems():
			for team_name, team in teams.iteritems():
				tmp_flag = service.getFlag(team.host, team_name)
				if tmp_flag == service.flags[team.name]:
					print '[+] Defense point! +1 for %s - %s' % (team_name, service_name)
					team.updateDefScore()

	def setFlags(self):
		for service_name, service in services.iteritems():
			for team_name, team in teams.iteritems():
				service.setFlag(team.host, team_name)


	def updateLog(self):
		localtime = time.asctime( time.localtime(time.time()) )
		out_file = open("log.txt","a")
		text = "\n-------------------\nLocal time: " + str(localtime)
		for team_name, team in teams.iteritems():
			text += "\n-------------------\n" + team_name + "\nAttack point: " + str(team.att_score) + "\nDefense point: " + str(team.def_score)

		out_file.write(text)
		out_file.close()

	def getFlagID(self, service_name, evil_team):
		return self.services[service_name].args[evil_team].get('flag_id')


	def submitFlags(self, team_name, service_name, flag):
		teamx = self.teams[team_name]
		dic_flags = self.services[service_name].flags
		for user, user_flag in dic_flags.iteritems():
			if flag == user_flag: #and user != teamx.name:
				print '[+] Attack point! +2 for ' + team_name
				teamx.updateAttScore()
				self.services[service_name].flags[user] = ""
				return "Flag valid!"
		return "Flag invalid!"

class Team:
	def __init__(self, name, host, pic):
		self.name = name
		self.host = host
		self.pic = pic
		self.att_score = 0
		self.def_score = 0

	def updateAttScore(self):
		self.att_score += 2

	def updateDefScore(self):
		self.def_score += 1

class Service:
   def __init__(self, name, port, module):
      self.name = name
      self.port = port
      self.module = module
      self.flags = {}
      self.args = {}

   def getFlagID(self, team_name):
   	  return (args[team_name]).get("flag_id", None)

   def setFlag(self, host, team_name):
   	  flag = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
   	  self.args[team_name] = self.module.set_flag(host, self.port, flag)
   	  self.flags[team_name] = flag
   	  print '[-] Set flag to ' + self.name + " service for " + team_name + " team"

   def getFlag(self, host, team_name):
   	  flag_id = self.args[team_name]["flag_id"]
   	  token = self.args[team_name]["token"]
   	  flag = self.module.get_flag(host, self.port, flag_id, token)
	  #print 'Retrieved flag: %s' % (flag)
	  print '[-] Retive flag to ' + self.name + " service for " + team_name + " team"
	  return flag

def routine():
	game.setFlags()
	game.getFlags()
	game.updateLog()
	threading.Timer(10, routine).start()

@app.route("/")
def hello():
	return render_template('index.html', teams=teams)	
	'''
	res = ""
	for team_name, team in teams.iteritems():
		res += "Name: {0}</br>Def Pnt: {1}</br>Att Pnt: {2}</br></br>".format(team_name, team.def_score, team.att_score)
	return res
	'''

@app.route('/submit', methods=['POST'])
def submitFlag():
	flag = request.form.get('flag', None)
	team_name = request.form.get('team', None)
	service_name = request.form.get('service', None)
	status = game.submitFlags(team_name, service_name, flag)
	return status

@app.route('/flagid', methods=['GET'])
def getFlagID():
	username = request.args.get('enemy_name')
	service_name = request.args.get('service')
	flagid = game.getFlagID(service_name, username)
	return str(flagid)

if __name__ == '__main__':

	teams = {'CuredPin': Team('CuredPin', "192.168.1.101", "cat.jpg"),
			 'LiquidPad': Team('LiquidPad', "192.168.1.101", "dog.jpg")}

	services = {'nadmozg': Service('nadmozg', '20067', nadmozg),
				'piratemap': Service('piratemap', '20038', piratemap),
				'FHMMaintenance': Service('FHMMaintenance', '20111', FHMMaintenance),
				'ropeman': Service('ropeman', '20129', ropeman),
				'blackgold': Service('blackgold', '20066', blackgold),
				'sharing': Service('sharing', '20065', sharing),
				'hanoifones': Service('hanoifones', '20040', hanoifones),
				'FHMMaintenance': Service('FHMMaintenance', '20111', FHMMaintenance), 
				'hacker_diary': Service('hacker_diary', '20130', hacker_diary)}
	
	'''
	teams = {'testTeam': Team('testTeam', "192.168.0.8")}
	'''
	'''
	Not working.
	'redmessanger': Service('redmessanger', '20064', redmessanger),
	'''

	game = Game(teams, services)
	routine()
	app.run()
