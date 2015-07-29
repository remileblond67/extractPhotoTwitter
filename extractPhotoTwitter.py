#!/usr/bin/python
# -*- coding: utf8 -*-
#--------------------------------------------------
# Extraction de photo à partir de recherche Twitter
#--------------------------------------------------
import twitter
import requests
import re
import shutil
import os.path

class compteTwitter:
    "Connexion au compte Twitter"
    def __init__(self):
        # Consumer keys and access tokens, used for OAuth
        configTwitter = {}
        execfile("twitter.conf", configTwitter)
        consumer_key = configTwitter["consumer_key"]
        consumer_secret = configTwitter["consumer_secret"]
        access_token = configTwitter["access_token"]
        access_token_secret = configTwitter["access_token_secret"]

        print ("Connecting to Twitter")
        self.api = twitter.Api(consumer_key, consumer_secret, access_token, access_token_secret)

    def presentUser(self):
        user = self.api.VerifyCredentials()
        print (user.name)

    def fetchTweet(self, findTxt, nbTweet):
        print ("--- Recherche des Tweets contenant " + findTxt)
        # Recherche des Tweets par groupes de 100 (limitation de l'Api Twitter)
        nbTweet = 0
        maxId = 0

        for i in range (0,1000):
            if maxId == 0:
                print "Première recherche"
                search = self.api.GetSearch(term=findTxt, count=nbTweet)
            else:
                print "Recherche à partie de l'id " + str(maxId)
                search = self.api.GetSearch(term=findTxt, count=nbTweet, max_id=maxId)

            for t in search:
                nbTweet = nbTweet + 1
                maxId = t.id
                for file in t.media:
                    urlImage = file['media_url']
                    findName = re.compile('^.*\/([^\/]*)$')
                    extractFileName = findName.match(urlImage)
                    if extractFileName:
                        fileName = "img/" + extractFileName.group(1)
                    # Test si le fichier existe déjà
                    if (os.path.isfile(fileName)):
                        print "Déjà téléchargée"
                    else:
                        print (urlImage + " -> " + fileName)
                        img = requests.get(urlImage, stream=True)
                        if img.status_code == 200:
                            file = open(fileName, 'wb')
                            for block in img.iter_content(1024):
                                if not block:
                                    break
                                file.write(block)
                            file.close()
                        del img
            print (nbTweet)

myTwitter = compteTwitter()
myTwitter.presentUser()
myTwitter.fetchTweet("#jesuischarlie", 10)
