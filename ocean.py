import twitter
import sqlite3
import random
import time

consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''

api = twitter.Api(consumer_key=consumer_key,
				consumer_secret=consumer_secret,
				access_token_key=access_token_key,
				access_token_secret=access_token_secret)

db = sqlite3.connect('dummies.db')

db.execute('CREATE TABLE IF NOT EXISTS dummies (id INTEGER PRIMARY KEY AUTOINCREMENT, statusid VARCHAR(32) NOT NULL);')

def BerateDummy ():
	tweets = api.GetSearch('across the pond')
	for status in tweets:
		if not DummyHasBeenBerated(status.id):
			#reply_text = "@%s It's actually an ocean, %s." % (status.user.GetScreenName(),Dummy())
			#replyto = status.id
			#api.PostUpdate(reply_text, in_reply_to_status_id=replyto)
			reply_body = "It's actually an ocean, %s. RT @%s " % (Dummy(), status.user.GetScreenName())
			status_excerpt = Excerpt(status.text, "across the pond", 140 - len(reply_body))
			reply = reply_body + status_excerpt
			api.PostUpdate(reply)
			print("In response to %d, tweeted: %s" % (status.id, reply))
			RecordDummyBerated(status.id)
			break

def DummyHasBeenBerated (statusid):
	query = "SELECT COUNT(*) FROM dummies WHERE statusid = '%s';" % (str(statusid))
	result = db.execute(query).fetchone()[0]
	return (result != 0)

def RecordDummyBerated (statusid):
	query = "INSERT INTO dummies (statusid) VALUES ('%s')" % (str(statusid))
	db.execute(query)

def Dummy ():
	epithets = (
		"dummy",
		"moron",
		"stupid",
		"idiot",
		"you fool",
		"you ignoramus",
		"you ignorant mule",
		"you clod",
		"you simpleton",
		"you oaf",
		"you buffoon"
	)
	return epithets[random.randint(0,len(epithets)-1)]

def Excerpt (text, phrase, maxlength):
	if len(text) <= maxlength:
		return text
	else:
		start = text.lower().find(phrase.lower())
		if start == -1:
			return ""
		end = start + len(phrase)
		if end < maxlength:
			return text[0:maxlength-3] + "..."
		elif (len(text) - start) < maxlength:
			return text[start:]
		else:
			return text[start:end]

if __name__ == "__main__":
	while True:
		BerateDummy()
		time.sleep(360)



