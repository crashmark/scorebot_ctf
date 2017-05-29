# FORKED for unict CTF 2017

Using the ucsb icttf 2015 vm.

[Services Spreadsheet](https://docs.google.com/spreadsheets/d/1neJixO6zLH3hMt0TSZnZKl6QOM6abev77Lt18J0X3dU/edit?usp=sharing)

[iCTF 2015 VM Download](https://ictf.cs.ucsb.edu/archive/2015/vms/ictf2015.services.tpxz)

### Service avaiable in this repo
| Service name | Port | Description | Flag description | Language | Author |
|-----------------|-------|-------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|---------------|
| pirate_map | 20038 | Pirate map -- find correct map and get pirate treasure! | Flags are indentified by treasure name. | bin | [@PieMaug](https://github.com/PieMaug)  |
| hanoiFones | 20040 | OnlineAuction platform | Flags are identified by the auction IDs. | bin | [@pietrobiondi](https://github.com/pietrobiondi) |
| red_messenger | 20064 | A simple message application. Register and start sending messages to other users, maybe you'll receive a response. Using HELP may be a good start. | The flag ID is the name of the user who send to himself a message with the flag in it. | C | [@PieMaug](https://github.com/PieMaug) |
| sharing | 20065 | Message sharing platform | Flags are identified by the sharing key | Python / DB | [@Tkd-Alex](https://github.com/Tkd-Alex) |
| Bl4ckG0ld | 20066 | Starbugs(tm) for your enjoyment. | Flags are identified by the RecipeNo. | bin | [@Tkd-Alex](https://github.com/Tkd-Alex) |
| nadmozg | 20067 | google translate killer | private dictionary name | C/bin | [@Aktivkernel](https://github.com/Aktivkernel) |
| text_file_store | 20093 | Password-protected text file storage service for the web. | Username used in identifing the file | PHP | [@emavgl](https://github.com/emavgl) |
| FHM-Maintenance | 20111 | Password-protected web storage for secrets in C. | Flags are identified by the username. | / | [@crashmark](https://github.com/crashmark) |
| tweety_bird | 20118 | Tweet backup storage service in C. | Flags are identified by the twit_id. | bin | [@emavgl](https://github.com/emavgl) |
| ropeman | 20129 | An interesting ropeman/hangman game binary program. Password-protected note storage service in C. | Flags are identified by the note name.The flags are the status field in a txt file for a registered user | bin | [@Tkd-Alex](https://github.com/Tkd-Alex) |
| hacker_diary | 20130 | Keeps a private log of how your exploits work, with timestamps and hashes you can share, so you can prove you exploited something without sharing how | A flag_id is an entry id which corresponds to a detailed, prehashed description of an exploit. http: //<hostname>: <port>/entries/<flag_id> should yield an entry with the flag | Python/Django | [@GabMus](https://github.com/GabMus) |

# Dependences
```python
...
pwntools
pwn
lxml
Flask
requests
pexpect
parse
```

# scorebot_ctf
This is a simple sketch of a scorebot for Attack-Defense CTF in python.
It has been tested using two services (textfilestore, tweety_bird) from iCTF 2015.

### Configuration
```python
...
#import here your services
import textfilestore
import tweetybird
...
if __name__ == '__main__':
	teams = {'team1': Team('team1', "192.168.56.101"), 'team2': ... }
	services = {'tweety_bird': Service('tweety_bird', '20118', tweetybird), 'textfilestore': Service('textfilestore', '20093', textfilestore)}
	game = Game(teams, services)
	...
```
The configuration has to be set in the main function.
You have to initialize the dictionary *teams* which contains for each team an object of type *Team(name, ip)*.
Every team has a name and an IP that the scorebot use to test the services.
Then you have to initialize the dictionary *service* with objects of type *Service(name, port)*.

### Services
Each service must have a python script inside the directory **./services** that contains the functions **set_flag(host, port, flag)** and **get_flag(host, port, flag_id, token)** used by the scorebot to set a new flag into the service and gets it back. The set_flag function returns to the main script a *flag_id* and a *token*. The get_flag function returns a flag given a flag_id and a token.

### Flask server
There is also a simple HTTP server that lets the teams submit flags, get flagIDs and view the scores.

```python
@app.route("/")
def hello():
	res = ""
	for team_name, team in teams.iteritems():
		res += "Name: {0}</br>Def Pnt: {1}</br>Att Pnt: {2}</br></br>".format(team_name, team.def_score, team.att_score)
	return res

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
```
