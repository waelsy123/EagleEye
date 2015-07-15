import spade
from bs4 import BeautifulSoup
import urllib2
import re 
import datetime
from pymongo import MongoClient

host = "127.0.0.1" 
VimeoID = 56298789 
IdForTwitter = VimeoID 

# db config
###########
client = MongoClient('localhost', 27017)
db = client.eedb


# Functions:
###########

def insertFilmData( sender, data ):
	print data['vimeoId'] 
	query =  db.films.find( { 'vimeoId' : data['vimeoId']} )
	if query is None:
		films = db.films
   		#film_id = films.count()
  		data['date'] = datetime.datetime.utcnow() 	
  		data['id'] = film_id 
  		films.insert_one(data) 
		print 'One row insert in db..' 
	#else :  updateFilmData() 

def sendMsgToAgent( address , self , msgContent):
	# First, form the receiver AID
        TwiRec = spade.AID.aid(name=address , addresses=["xmpp://" + address ])
        IdForTwitter = self.counter
        # Second, build the message
        self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
        self.msg.setOntology("EagleEyeOntology")        # Set the ontology of the message content
        self.msg.setLanguage("English")           # Set the language of the message content
        self.msg.addReceiver(TwiRec)              # Add the message receiver
        self.msg.setContent(msgContent)              # Set the message content

        # Third, send the message with the "send" method of the agent
        self.myAgent.send(self.msg)




def getAccount( website , url):
	res = urllib2.urlopen(url)
        html = res.read()
	soup = BeautifulSoup(html)
	try:
		reg = '(((http:\/\/|https:\/\/))+|(www\.)?)' + website + '\.com\/(#!\/)?[a-zA-Z0-9_]+'
		res=re.search(reg, html)
		print res.group(0) 
		url_res = res.group(0)   
		return url_res 
	except Exception as e:
		return None 

############### Class
class bcolors:
    OKBLUE = '\033[1;36m'
    OKGREEN = '\033[1;32m'
    OKRED = '\033[1;31m'
    ENDC = '\033[0m'


# # Vimeo agent done:
#  1. print Id, author, title 
#  
class VimeoAgent(spade.Agent.Agent):
    class MyBehav(spade.Behaviour.Behaviour):
        def onStart(self):
            print bcolors.OKBLUE + "%s* Starting Vimeo behaviour.." % ("[Vimeo]".ljust(10)) + bcolors.ENDC
            self.counter = VimeoID

        def _process(self):

            try:
		url = 'http://vimeo.com/' + str(self.counter)
                res = urllib2.urlopen(url)
                html = res.read()                
                soup = BeautifulSoup(html)  

                author = soup.find('a', rel="author")
		authorUrl = author['href'] 
		author = soup.find('a', rel="author").get_text() 

                title = soup.title.get_text()
                print bcolors.OKBLUE + '[%d] %s | %s' % (self.counter, author.ljust(16), title) + bcolors.ENDC
                
		authorUrl = 'http://vimeo.com' + authorUrl
		print authorUrl 
		
		
		des = soup.find('div', class_="description_wrapper") 
		VideoDes = soup.find('div', class_="description_wrapper").get_text() 
		#VideoDes = os.linesep.join([s for s in VideoDes.splitlines() if s])
		print VideoDes 
		
		res_author = urllib2.urlopen(authorUrl) 
		html_author = res_author.read()
		soup_author = BeautifulSoup(html_author) 
		des_author = soup_author.find('section', class_="user_bio") 
		des_author_text = soup_author.find('section', class_="user_bio").get_text() 

		print des_author_text   
		
	 	reg = '(((http://|https://))+|(www\.)+)(?!facebook)(?!twitter)[a-z0-9]+(\.(?!facebook)(?!twitter)[a-z0-9]+)+'	
                website=re.search(reg, des_author_text)
		website = website.group(0) 
                print "The website of the author: " +  website

		facebook = getAccount( 'facebook',  url )  
		if facebook is None: 
			facebook = getAccount( 'facebook' , authorUrl)  
               		if facebook is None: 
                        		facebook = getAccount( 'facebook' , website)  

		twitter = getAccount( 'twitter',  url )
                if twitter is None:
                        twitter = getAccount( 'twitter' , authorUrl)  	
			if twitter is None:
		                        twitter = getAccount( 'twitter' , website )  


		address = "twitteragent@" + host 
        	IdForTwitter = self.counter
		sendMsgToAgent(address, self, twitter)	
	
		self.counter = self.counter + 1
		
            except:
                self.counter = self.counter + 1 
                return 
            # time.sleep(1)

    def _setup(self):
        print bcolors.OKBLUE +  "[Vimeo]".ljust(10) + "** Starting Vimeo Agent.." + bcolors.ENDC
        # b = self.MyBehav()
        # self.addBehaviour(b, None)

class TwitterAgent(spade.Agent.Agent):
        class MyBehav(spade.Behaviour.Behaviour):
                def onStart(self):
                        print bcolors.OKRED + "[Twitter]".ljust(10) + "* Starting Twitter behaviour.." + bcolors.ENDC
                        self.counter = 0

                
        class ReceiveBehav(spade.Behaviour.Behaviour):
        
                def _process(self):
		    while(True):
			 self.msg = None             
                	 # Blocking receive for 10 seconds
                	 self.msg = self._receive(True)
                	    
                    	 # Check wether the message arrived
                   	 if self.msg:
                   	     print bcolors.OKRED + 'Twitter found: %s ' % self.msg.getContent() + bcolors.ENDC
                   	     res = urllib2.urlopen("http://" + self.msg.getContent())
                   	     html = res.read()
                   	         
                   	     soup = BeautifulSoup(html)  
                   	     address = soup.find('span', class_="ProfileHeaderCard-locationText u-dir").get_text()
                             twitter_bio = soup.find('p' , class_="ProfileHeaderCard-bio u-dir").get_text() 
			     website = soup.find('a', rel="me_nofollow").get_text()
                  	     print bcolors.OKRED + '[%d] address: %s ' % (IdForTwitter, address.ljust(16) ) + bcolors.ENDC
          		     print bcolors.OKRED + '[%d] Biography from twitter: %s ' % (IdForTwitter, twitter_bio ) + bcolors.ENDC
                             print bcolors.OKRED + '[%d] Website from twitter: %s ' % (IdForTwitter, website ) + bcolors.ENDC
                        
        def _setup(self):
                b = self.MyBehav()
                self.setDefaultBehaviour(b)

		Btemplate = spade.Behaviour.ACLTemplate()
		Btemplate.setOntology("EagleEyeOntology")
		mt = spade.Behaviour.MessageTemplate(Btemplate)
		
		rb = self.ReceiveBehav()
		self.addBehaviour(rb,mt)
                print bcolors.OKRED + "[Twitter]".ljust(10) + "** Starting Twitter Agent.." + bcolors.ENDC

class FBAgent(spade.Agent.Agent):
        class MyBehav(spade.Behaviour.Behaviour):
                def onStart(self):
                        print bcolors.OKGREEN + "[FB]".ljust(10) + "* Starting Facebook behaviour.." + bcolors.ENDC
                        self.counter = 0

        class ReceiveBehav(spade.Behaviour.Behaviour):

                def _process(self):
                    while(True):
                         self.msg = None
                         # Blocking receive for 10 seconds
                         self.msg = self._receive(True)

                         # Check wether the message arrived
                         if self.msg:
                             print bcolors.OKGREEN + 'Facebook found: %s ' % self.msg.getContent() + bcolors.ENDC
                             res = urllib2.urlopen("http://" + self.msg.getContent())
                             html = res.read()

                             soup = BeautifulSoup(html)
                             ShortDes = soup.find('div', class_="_50f4").get_text()
			     print ShortDes 
        def _setup(self):
                b = self.MyBehav()
		self.setDefaultBehaviour(b)

		Btemplate= spade.Behaviour.ACLTemplate() 
		Btemplate.setOntology("EagleEyeOntology")
		mt = spade.Behaviour.MessageTemplate(Btemplate)
		
		rb = self.ReceiveBehav()
		self.addBehaviour(rb, mt)
                print bcolors.OKGREEN + "[FB]".ljust(10) + "** Starting Facebook Agent.." + bcolors.ENDC

if __name__ == "__main__":
    # # Create the agents ans start them.. 
    vimeo = VimeoAgent("vimeoagent@" + host , "secret")
    twitter = TwitterAgent("twitteragent@" + host , "secret")
    fb = FBAgent("fbagent@" + host , "secret")

    vimeo.start()
    twitter.start()
    fb.start()
    
    # # create vimeo behav which will start scrapping vimeo videos..
    b = vimeo.MyBehav()
    vimeo.addBehaviour(b, None)

