import decimal
import string
import math
import requests
from cmu_112_graphics import *
import csv
import os.path
login_file = 'logins.csv'
check_file = os.path.isfile(login_file)
#***All images used in this app were taken from the yelp api***
#***App pages designed by Theodore Bates***

class loginPage(Mode):
    username = ''
    def appStarted(mode):
        mode.username = ''
        mode.password = ''
        mode.name = ''
        mode.gettingUser = False
        mode.gettingPass = False
        mode.gettingName = False
        mode.gotUser = False
        mode.gotPass = False
        mode.gotName = False
        mode.logging = False
        mode.creating = False
        mode.userText = text(215,440)
        mode.passText = text(215,588)
        mode.nameText = text(215,722)
        mode.makeAcc = buttons(272,94,498,872,'orange')
        mode.createAcc = buttons(272,94,498,744,'pink')
        mode.signIn = buttons(272,94,500,736,'green')
        mode.login = buttons(272,94,498,609,'blue')
        mode.WelPhoto = Image.open('Welcome.png')
        mode.loginPhoto = Image.open('Login.png')
        mode.createPhoto = Image.open('Create Account.png')

    def mousePressed(mode,event):
        if not mode.logging and not mode.creating:
            if mode.login.findButton(event.x,event.y):
                mode.logging = not mode.logging
                mode.gettingUser = not mode.gettingUser
            elif mode.createAcc.findButton(event.x,event.y):
                mode.creating = not mode.creating
                mode.gettingUser = not mode.gettingUser
        elif mode.signIn.findButton(event.x,event.y):
            if mode.Enter(mode.username,mode.password) != False:
                mode.app.setActiveMode(mode.app.start)
            else:
                mode.refresh()
        elif mode.makeAcc.findButton(event.x,event.y):
            if mode.create(mode.username,mode.password,mode.name):
                mode.refresh()
                mode.logging = not mode.logging
                mode.gettingUser = not mode.gettingUser
            else:
                mode.refresh()  

    def refresh(mode):
        mode.gettingUser = False              
        mode.gettingPass = False
        mode.username = ''
        mode.password = ''
        mode.name = ''
        mode.userText.reset()
        mode.passText.reset()
        mode.nameText.reset()
        mode.gotUser = False
        mode.gotPass = False
        mode.gotName = False
        mode.logging = False
        mode.creating = False
    
    def keyPressed(mode,event):
        if mode.gettingUser:
            mode.userText.keyPressed(event)
        elif mode.gettingPass:
            mode.passText.keyPressed(event)
        elif mode.gettingName:
            mode.nameText.keyPressed(event)
        if event.key == 'Enter':
            if mode.logging:
                if mode.gettingUser:
                    mode.username = mode.userText.getWord() 
                    loginPage.username = mode.username
                    mode.gettingUser = not mode.gettingUser
                    mode.gettingPass = not mode.gettingPass
                    mode.gotUser = not mode.gotUser
                elif mode.gettingPass:
                    mode.password = mode.passText.getWord()
                    mode.gettingPass = not mode.gettingPass
                    mode.gotPass = not mode.gotPass
            elif mode.creating:
                if mode.gettingUser:
                    mode.username = mode.userText.getWord() 
                    loginPage.username = mode.username
                    mode.gettingUser = not mode.gettingUser
                    mode.gettingPass = not mode.gettingPass
                    mode.gotUser = not mode.gotUser
                elif mode.gettingPass:
                    mode.password = mode.passText.getWord()
                    mode.gettingPass = not mode.gettingPass
                    mode.gotPass = not mode.gotPass
                    mode.gettingName = not mode.gettingName
                else:
                    mode.name = mode.nameText.getWord().capitalize()
                    mode.gettingName = not mode.gettingName
                    mode.gotName = not mode.gotName                

    def Enter(mode,username,password):
        with open(login_file,'r',newline = '') as f:
            reader = csv.DictReader(f)
            logins = dict()
            names = dict()
            for row in reader:
                logins[row['user']] = row['pass']
                names[row['user']] = row['name']
            if username in logins and logins[username] == password:
                return names[username]
            else:
                return False
    
    def create(mode,username,password,name):
        if check_file:
            with open(login_file,'r',newline = '') as f:
                reader = csv.DictReader(f)
                existingUsers = []
                for row in reader:
                    existingUsers.append(row['user'])
                if username in existingUsers:
                    return False
                else:
                    with open(login_file,'a',newline = '') as f:
                        fieldNames = ['user','pass','name','friends','favorites','visited']
                        writer = csv.DictWriter(f,fieldNames)
                        logins = {'user':username,'pass':password,'name':name}
                        if not check_file:
                            writer.writeheader()
                        writer.writerow(logins)
                        return True
        else:
            with open(login_file,'a',newline = '') as f:
                fieldNames = ['user','pass','name','friends','favorites','visited']
                writer = csv.DictWriter(f,fieldNames)
                logins = {'user':username,'pass':password,'name':name}
                if not check_file:
                    writer.writeheader()
                writer.writerow(logins)
                return True
    #taken from homework 2
    def rgbString(mode, red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)

    def drawWarning(mode,canvas):
        color = mode.rgbString(248,222,126)
        text = "Press Enter\nto move on"
        canvas.create_rectangle(635,300,920,400,fill = color,width = 3)
        canvas.create_text(700,315,text = text, font = 'Arial 20',anchor = 'nw')
    
    def drawName(mode,canvas):
        canvas.create_text(215,722,text = mode.name, font = 'Arial 30',anchor = 'nw')
    
    def drawPassword(mode,canvas):
        hide = mode.passText.hidden
        canvas.create_text(215,588,text = hide, font = 'Arial 30',anchor = 'nw')
   
    def drawUsername(mode,canvas):
        canvas.create_text(215,440,text = mode.username, font = 'Arial 30',anchor = 'nw')
    
    def redrawAll(mode,canvas):
        if not mode.logging and not mode.creating:
            canvas.create_image(0,0,image = ImageTk.PhotoImage(mode.WelPhoto),anchor = 'nw')
        elif mode.logging:
            canvas.create_image(0,0,image = ImageTk.PhotoImage(mode.loginPhoto),anchor = 'nw')
            mode.drawWarning(canvas)
            color = mode.rgbString(57,181,74)
            if mode.gettingUser:
                mode.userText.drawWord(canvas)
                canvas.create_rectangle(350,686,700,796, fill = color,width = 0)
            elif mode.gettingPass:
                mode.passText.drawhideWord(canvas)
                mode.drawUsername(canvas)
                canvas.create_rectangle(350,686,700,796, fill = color,width = 0)
            elif mode.gotUser and mode.gotPass:
                mode.drawUsername(canvas)
                mode.drawPassword(canvas)
        elif mode.creating:
            canvas.create_image(0,0,image = ImageTk.PhotoImage(mode.createPhoto),anchor = 'nw')
            mode.drawWarning(canvas)
            color = mode.rgbString(51,102,255)
            if mode.gettingUser:
                mode.userText.drawWord(canvas)
                canvas.create_rectangle(355,800,650,940,fill = color, width = 0)
            elif mode.gettingPass:
                mode.passText.drawhideWord(canvas)
                mode.drawUsername(canvas)
                canvas.create_rectangle(355,800,650,940,fill = color, width = 0)
            elif mode.gettingName:
                mode.nameText.drawWord(canvas)
                mode.drawUsername(canvas)
                mode.drawPassword(canvas)
                canvas.create_rectangle(355,800,650,940,fill = color, width = 0)
            elif mode.gotName and mode.gotPass and mode.gotUser:
                mode.drawUsername(canvas)
                mode.drawPassword(canvas)
                mode.drawName(canvas)
                
class StartScreen(Mode):
    term = ''
    radiusMeters = ''
    radiusMiles = ''
    address = ''

    @staticmethod
    def mileToMeter(value):
        meter = 1609.34*value
        return StartScreen.roundHalfUp(meter)

    # taken from : https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html
    @staticmethod
    def roundHalfUp(d):
        import decimal
        rounding = decimal.ROUND_HALF_UP
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

    def appStarted(mode):
        user = loginPage().username
        mode.Profile = Profile(user)
        mode.name = mode.Profile.getName()
        mode.next = buttons(272,94,498,850,'pink')
        mode.termText = text(215,396)
        mode.radiusText = text(215,542)
        mode.addressText = text(215,688)
        mode.photo = Image.open('Search Food.png')
        mode.gettingTerm = True
        mode.gettingRadius = False
        mode.gettingAddress = False
        mode.gotTerm = False
        mode.gotRadius = False
        mode.gotAddress = False
        mode.start = False
        mode.term = ''
        mode.radius = ''
        mode.address = ''

    def mousePressed(mode,event):
        if mode.next.findButton(event.x,event.y):
            StartScreen.term = mode.term
            StartScreen.radiusMeters = StartScreen.mileToMeter(mode.radius)
            StartScreen.radiusMiles = mode.radius
            StartScreen.address = mode.address
            mode.app.setActiveMode(mode.app.mainPage)

    def keyPressed(mode,event):
        if mode.gettingTerm:
            mode.termText.keyPressed(event)
        if mode.gettingRadius:
            mode.radiusText.keyPressed(event)
        if mode.gettingAddress:
            mode.addressText.keyPressed(event)
        if event.key == 'Enter':
            if mode.gettingTerm:
                mode.term = mode.termText.getWord()
                mode.gotTerm = True
                mode.gettingTerm = False
                mode.gettingRadius = True
        
            elif mode.gettingRadius:
                radius = mode.radiusText.getWord()
                if radius.isdigit():
                    if int(radius) < 25 and int(radius) >= 6:
                        mode.radius = int(radius)
                        mode.gotRadius = True
                        mode.gettingRadius = False
                        mode.gettingAddress = True

            elif mode.gettingAddress:
                mode.address = mode.addressText.getWord()
                mode.gotAddress = True
                mode.gettingAddress = False
                mode.start = True

    def rgbString(mode, red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)

    def drawWarning(mode,canvas):
        color = mode.rgbString(248,222,126)
        text = "Press Enter\nto move on"
        canvas.create_rectangle(635,280,850,360,fill = color,width = 3)
        canvas.create_text(670,290,text = text, font = 'Arial 20',anchor = 'nw')
    
    def drawTerm(mode,canvas):
        canvas.create_text(215,396,text = mode.term,font = 'Arial 30', anchor = 'nw')
    
    def drawRadius(mode,canvas):
        canvas.create_text(215,542,text = f'{mode.radius}',font = 'Arial 30',anchor = 'nw')
    
    def drawAddress(mode,canvas):
        canvas.create_text(215,688,text = mode.address,font = 'Arial 30',anchor = 'nw')

    def redrawAll(mode,canvas):
        color = mode.rgbString(255,81,0)
        canvas.create_image(0,0,image = ImageTk.PhotoImage(mode.photo),anchor = 'nw')
        mode.drawWarning(canvas)
        if mode.gettingTerm:
            mode.termText.drawWord(canvas)
            canvas.create_rectangle(355,800,650,920,fill = color, width = 0)
        elif mode.gettingRadius:
            mode.drawTerm(canvas)
            mode.radiusText.drawWord(canvas)
            canvas.create_rectangle(355,800,650,920,fill = color, width = 0)
        elif mode.gettingAddress:
            mode.drawTerm(canvas)
            mode.drawRadius(canvas)
            mode.addressText.drawWord(canvas)
            canvas.create_rectangle(355,800,650,920,fill = color, width = 0)
        elif mode.gotTerm and mode.gotRadius and mode.gotAddress:
            mode.drawRadius(canvas)
            mode.drawAddress(canvas)
            mode.drawTerm(canvas)

class MainPage(Mode):
    data = []
    matchName = ''
    matchAddress = ''
    
    def appStarted(mode):
        #lines 327 - 341 were adapted from the yelp api source code and this
        #youtube video https://www.youtube.com/watch?v=GJf7ccRIK4U
        mode.term = StartScreen.term
        mode.radius = StartScreen.radiusMeters
        mode.location = StartScreen.address
        yelpApiKey = 'qMzTBgXXSQuDZ7f1GVxFCCc1neIQxio3q1IS0uXcPcsh5rv5Arz8XO_8hVEPInlzl47qm_hKtRw9f6udj1MNI4XC9ja6ArToO6hzWlBMLnXwxdXYaUcMYn90WiuIXnYx'
        yelpClientId = 'M0kW4joK0wGslAUmWuUSeA'
        businessEndPoint = 'https://api.yelp.com/v3/businesses/search'
        headers = {'Authorization':f'Bearer {yelpApiKey}'}
        parameters = {'term':mode.term,
                    'limit':50,
                    'radius': mode.radius,
                    'location': mode.location}
        normResponse = requests.get(url = businessEndPoint,params = parameters,headers = headers)
        normData = normResponse.json()
        for elem in normData['businesses']:
            mode.profile = yelp(elem,headers)
        MainPage.data = mode.profile.graphData
        mode.graph = Graph()
        mode.moreInfoButton = buttons(60,20,715,818,'blue')
        mode.viewFriendsButton = buttons(60,60,765,928,'pink')
        mode.viewFavoritesButton = buttons(86,82,921,927,'orange')
        mode.addFriendsButton = buttons(60,60,828,929,'brown')
        mode.friendsFavsButton = buttons(60,60,697,929,'green')
        mode.graphButton = buttons(40,40,725,775,'light green')
        mode.profileIndex = 0
        mode.imageIndex = 0
        mode.name = mode.profile.restaurants[mode.profileIndex].name
        mode.price = mode.profile.restaurants[mode.profileIndex].price
        mode.address = mode.profile.restaurants[mode.profileIndex].address
        mode.distance = mode.profile.restaurants[mode.profileIndex].distance
        mode.phone = mode.profile.restaurants[mode.profileIndex].phone
        mode.hours = mode.profile.restaurants[mode.profileIndex].hours
        mode.rating = mode.profile.restaurants[mode.profileIndex].rating
        mode.isOpen = mode.profile.restaurants[mode.profileIndex].isOpen
        mode.profileWidth = mode.width//4
        mode.profileHeight = mode.height//3
        mode.startX,mode.startY = mode.width//2,mode.height//2
        mode.move = False
        mode.match = False
        mode.moreInfo = False
        mode.displayGraph = False
        mode.username = loginPage().username
        mode.currentUser = Profile(mode.username)
        mode.addFavoritesButton = buttons(30,30,mode.startX+mode.profileWidth,mode.startY-mode.profileHeight,'yellow')
        mode.matchX,mode.matchY = 0,0
        mode.backgroundPhoto = Image.open('Match Page.png')
        mode.starPhoto = Image.open('star.png')
        mode.profilePhoto = Image.open('card.png')
        imageUrl = mode.profile.restaurants[mode.profileIndex].photos[mode.imageIndex]
        photo = mode.loadImage(imageUrl)
        mode.photo = photo.resize((2*mode.profileWidth,2*mode.profileWidth))
        mode.moreInfoPhoto = Image.open('more.png')
        mode.iconPhoto = Image.open('icon.png')

    def mousePressed(mode,event):
        if mode.moreInfoButton.findButton(event.x,event.y):
            mode.moreInfo = not mode.moreInfo
            mode.displayGraph = False
        elif mode.viewFriendsButton.findButton(event.x,event.y):
            mode.app.setActiveMode(mode.app.viewFriends)
        elif mode.addFriendsButton.findButton(event.x,event.y):
            mode.app.setActiveMode(mode.app.addFriends)
        elif mode.addFavoritesButton.findButton(event.x,event.y):
            mode.currentUser.addFavorite(mode.profile.restaurants[mode.profileIndex].name)
        elif mode.viewFavoritesButton.findButton(event.x,event.y):
            mode.app.setActiveMode(mode.app.viewMyFavorites)
        elif mode.friendsFavsButton.findButton(event.x,event.y):
            mode.app.setActiveMode(mode.app.findFriends)
        elif mode.graphButton.findButton(event.x,event.y):
            mode.displayGraph = not mode.displayGraph
        if mode.displayGraph:
            value = mode.graph.findDot(event.x,event.y)
            if value != None:
                mode.profileIndex = value
                mode.switchProfile()
                mode.moreInfo = False
                mode.displayGraph = False
    
    def keyPressed(mode,event):
        if event.key == 'Left':
            mode.move = True
            mode.moreInfo = False
            mode.displayGraph = False
        elif event.key == 'Right':
            mode.match = True
            MainPage.matchName = mode.name
            MainPage.matchAddress = mode.address
        elif event.key == 'Up':
            if mode.imageIndex < mode.profile.restaurants[mode.imageIndex].numOfPhotos:
                mode.imageIndex += 1
                imageUrl = mode.profile.restaurants[mode.profileIndex].photos[mode.imageIndex]
                photo = mode.loadImage(imageUrl)
                mode.photo = photo.resize((2*mode.profileWidth,2*mode.profileWidth))
            else:
                mode.imageIndex = 0
                imageUrl = mode.profile.restaurants[mode.profileIndex].photos[mode.imageIndex]
                photo = mode.loadImage(imageUrl)
                mode.photo = photo.resize((2*mode.profileWidth,2*mode.profileWidth))
    
    def timerFired(mode):
        if mode.move:
            mode.moveLeft()
        elif mode.match:
            mode.matchScreen()
    
    def moveLeft(mode):
        mode.startX -= 175
        if (mode.startX+mode.profileWidth) <= 0:
            mode.startX = mode.width//2
            if (len(mode.profile.restaurants) -1) > mode.profileIndex:
                mode.profileIndex += 1
                mode.imageIndex = 0
            else:
                mode.profileIndex = 0
                mode.imageIndex = 0
            imageUrl = mode.profile.restaurants[mode.profileIndex].photos[mode.imageIndex]
            photo = mode.loadImage(imageUrl)
            mode.photo = photo.resize((2*mode.profileWidth,2*mode.profileWidth))
            mode.move = False
            mode.moreInfo = False
            mode.displayGraph = False
            mode.name = mode.profile.restaurants[mode.profileIndex].name
            mode.price = mode.profile.restaurants[mode.profileIndex].price
            mode.address = mode.profile.restaurants[mode.profileIndex].address
            mode.distance = mode.profile.restaurants[mode.profileIndex].distance
            mode.phone = mode.profile.restaurants[mode.profileIndex].phone
            mode.rating = mode.profile.restaurants[mode.profileIndex].rating
            mode.isOpen = mode.profile.restaurants[mode.profileIndex].isOpen

    def yelpRating(mode):
        if mode.profile.restaurants[mode.profileIndex].rate == 0:
            mode.ratingPhoto = Image.open('yelp 0.png')
        elif mode.profile.restaurants[mode.profileIndex].rate == 1:
            mode.ratingPhoto = Image.open('yelp 1.png')
        elif mode.profile.restaurants[mode.profileIndex].rate == 1.5:
            mode.ratingPhoto = Image.open('yelp 1.5.png')
        elif mode.profile.restaurants[mode.profileIndex].rate == 2:
            mode.ratingPhoto = Image.open('yelp 2.png')
        elif mode.profile.restaurants[mode.profileIndex].rate == 2.5:
            mode.ratingPhoto = Image.open('yelp 2.5.png')
        elif mode.profile.restaurants[mode.profileIndex].rate == 3:
            mode.ratingPhoto = Image.open('yelp 3.png')
        elif mode.profile.restaurants[mode.profileIndex].rate == 3.5:
            mode.ratingPhoto = Image.open('yelp 3.5.png')
        elif mode.profile.restaurants[mode.profileIndex].rate == 4:
            mode.ratingPhoto = Image.open('yelp 4.png')
        elif mode.profile.restaurants[mode.profileIndex].rate == 4.5:
            mode.ratingPhoto = Image.open('yelp 4.5.png')
        elif mode.profile.restaurants[mode.profileIndex].rate == 5:
            mode.ratingPhoto = Image.open('yelp 5.png')

    def switchProfile(mode):
        mode.yelpRating()
        mode.name = mode.profile.restaurants[mode.profileIndex].name
        mode.price = mode.profile.restaurants[mode.profileIndex].price
        mode.address = mode.profile.restaurants[mode.profileIndex].address
        mode.distance = mode.profile.restaurants[mode.profileIndex].distance
        mode.phone = mode.profile.restaurants[mode.profileIndex].phone
        mode.hours = mode.profile.restaurants[mode.profileIndex].hours
        mode.rating = mode.profile.restaurants[mode.profileIndex].rating
        mode.isOpen = mode.profile.restaurants[mode.profileIndex].isOpen
        imageUrl = mode.profile.restaurants[mode.profileIndex].photos[mode.imageIndex]
        photo = mode.loadImage(imageUrl)
        mode.photo = photo.resize((2*mode.profileWidth,2*mode.profileWidth))

    def matchScreen(mode):
        mode.matchX += 50
        mode.matchY += 50

        if mode.matchX >= mode.width:
            mode.matchX,mode.matchY = 0,0
            mode.match = False
            mode.app.setActiveMode(mode.app.matchScreen)

    def drawMoreInfo(mode,canvas):
        name = mode.name
        phone = mode.phone
        address = f'Address: \n{mode.address}'
        hours = f'Hours: \n{mode.hours}'
        pic = mode.photo.load()
        x = pic[50,50]
        color = mode.rgbString(x[0],x[1],x[2])
        canvas.create_rectangle(0,0,mode.width,mode.height,fill = color)
        mode.photo = mode.photo.resize((3*mode.profileWidth,3*mode.profileWidth))
        x1,y1,x2,y2 = (mode.startX-mode.profileWidth,mode.startY-.5*mode.profileHeight,
                        mode.startX+mode.profileWidth,mode.startY+mode.profileHeight)
        canvas.create_image(mode.width//2,mode.height//3,image = ImageTk.PhotoImage(mode.photo))
        canvas.create_rectangle(x1,y1,x2,y2,fill = 'white',outline = 'black',width = 3)
        canvas.create_image(715,818,image = ImageTk.PhotoImage(mode.moreInfoPhoto))
        mode.graphButton.drawButton(canvas)
        canvas.create_image(725,775,image = ImageTk.PhotoImage(mode.iconPhoto))
        canvas.create_text(mode.startX,mode.profileHeight + .1*mode.startY,text = name,font = 'Arial 20 bold')
        canvas.create_text(mode.startX,mode.profileHeight + mode.startY//4,text = phone,font = 'Arial 15')
        canvas.create_text(mode.startX,mode.profileHeight + mode.startY//2.5,text = address,font = 'Arial 15')
        canvas.create_text(mode.startX,mode.profileHeight + mode.startY//1.35,text = hours,font = 'Arial 15')

    def drawImage(mode,canvas):
        mode.photo = mode.photo.resize((2*mode.profileWidth,2*mode.profileWidth))
        x1,y1 = (mode.startX-mode.profileWidth+6),(mode.startY-mode.profileHeight+3)
        canvas.create_image(x1,y1,image = ImageTk.PhotoImage(mode.photo),anchor = 'nw')

    def rgbString(mode, red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)

    def drawMatchScreen(mode,canvas):
        matchText = "It's a Match!"
        color = mode.rgbString(208,240,192)
        x1,y1,x2,y2 = (mode.startX-mode.matchX,mode.startY-mode.matchY,
                    mode.startX+mode.matchX,mode.startY+mode.matchY)
        canvas.create_rectangle(x1,y1,x2,y2,fill = color)
        if mode.matchX >= 300:
            canvas.create_text(mode.width//2,mode.height//2,text = "It's a Match", font = 'Arial 70 bold')

    def drawGraph(mode,canvas):
        distance = mode.profile.restaurants[mode.profileIndex].span
        rating = mode.profile.restaurants[mode.profileIndex].rate
        x1,y1,x2,y2 = mode.startX-mode.graph.width,mode.startY-mode.graph.height,mode.startX+mode.graph.width,mode.startY+mode.graph.height
    
        mode.graph.drawGraph(canvas,mode.startX-mode.graph.width,mode.startY-mode.graph.height,mode.startX+mode.graph.width,mode.startY+mode.graph.height)
        mode.graph.drawPoint(canvas,distance,rating,x1,y1,x2,y2,mode.profileIndex,'red')

    def drawProfile(mode,canvas):
        mode.yelpRating()
        username = mode.currentUser.getName()
        name = mode.name
        price = mode.price
        isOpen = mode.isOpen 
        rating = mode.rating 
        distance = mode.distance
        x1,y1,x2,y2 = (mode.startX-mode.profileWidth,mode.startY-mode.profileHeight,
                    mode.startX+mode.profileWidth,mode.startY+mode.profileHeight)
        canvas.create_image(0,0,image = ImageTk.PhotoImage(mode.backgroundPhoto),anchor = 'nw')
        canvas.create_text(mode.width//2,100,text = f'Hello {username}!!',font = 'Arial 40 bold')
        canvas.create_image(x1,y1,image = ImageTk.PhotoImage(mode.profilePhoto),anchor = 'nw')
        canvas.create_text(mode.startX - 0.9*mode.profileWidth,2*mode.profileHeight + .025*mode.startY+5,text = name,font = 'Arial 15 bold',anchor = 'nw')
        canvas.create_text(mode.startX - 0.9*mode.profileWidth,2*mode.profileHeight + .125*mode.startY+5,text = price,font = 'Arial 15', anchor = 'nw')
        canvas.create_image(mode.startX,2*mode.profileHeight + .25*mode.startY+5,image = ImageTk.PhotoImage(mode.ratingPhoto))
        canvas.create_text(mode.startX + 0.9*mode.profileWidth,2*mode.profileHeight + .025*mode.startY+5,text = distance,font = 'Arial 15 bold',anchor = 'ne')
        canvas.create_text(mode.startX + 0.9*mode.profileWidth,2*mode.profileHeight + .125*mode.startY+5,text = isOpen,font = 'Arial 15',anchor = 'ne')
    
    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill = 'light blue')
        mode.drawProfile(canvas)
        if not mode.moreInfo:
            mode.drawProfile(canvas)
            mode.drawImage(canvas)
        if mode.moreInfo == False:
            canvas.create_image(mode.startX+mode.profileWidth,mode.startY-mode.profileHeight,image = ImageTk.PhotoImage(mode.starPhoto))
        if mode.moreInfo:
            mode.drawMoreInfo(canvas)
        if mode.displayGraph:
            mode.drawGraph(canvas)
        if mode.match:
            mode.drawMatchScreen(canvas)

class FindFriendsFavorites(Mode):
    favFriend = ''
    def appStarted(mode):
        user = loginPage().username
        mode.Profile = Profile(user)
        mode.backButton = buttons(98,68,117,96,'blue') 
        mode.userText = text(215,546)
        mode.searchButton = buttons(272,94,500,698,'light blue') 
        mode.removePopUpButton = buttons(76,76,800,525,'red')
        mode.gettingFriend = True
        mode.error = False
        mode.friend = ''
        mode.photo = Image.open('Search Friends Favorites.png')
        mode.errorPhoto = Image.open('Friend Error.png')
    def mousePressed(mode,event):
        if mode.searchButton.findButton(event.x,event.y):
            mode.friend = mode.userText.getWord()
            if mode.friend in Profile.friends:
                FindFriendsFavorites.favFriend = mode.friend
                mode.refresh()
                mode.app.setActiveMode(mode.app.viewFriendsFavorites)
            else:
                mode.error = True
        elif mode.removePopUpButton.findButton(event.x,event.y):
            mode.error = False
        elif mode.backButton.findButton(event.x,event.y):
            mode.refresh()
            mode.app.setActiveMode(mode.app.mainPage)

    def keyPressed(mode,event):
        if mode.gettingFriend:
            mode.userText.keyPressed(event)   

    def refresh(mode):
        mode.gettingFriend = True
        mode.error = False
        mode.friend = ''
        mode.userText.reset()

    def redrawAll(mode,canvas):
        canvas.create_image(0,0,image = ImageTk.PhotoImage(mode.photo),anchor = 'nw')
        mode.userText.drawWord(canvas)
        if mode.error:
            canvas.create_image(mode.width//2,mode.height//2+100,image = ImageTk.PhotoImage(mode.errorPhoto))

class AddFriends(Mode):
    
    def appStarted(mode):
        user = loginPage().username
        mode.profile = Profile(user)
        mode.userText = text(215,546)
        mode.addButton = buttons(272,94,500,698,'light blue')
        mode.backButton = buttons(98,68,117,96,'pink')
        mode.removePopUpButton = buttons(76,76,800,525,'red')
        mode.photo = Image.open('Add Friends Page.png')
        mode.errorPhoto = Image.open('Dont Exist Error.png')
        mode.successPhoto = Image.open('friend added.png')
        mode.gettingFriend = True
        mode.success = False
        mode.error = False
        mode.friend = ''
    
    def mousePressed(mode,event):
        if mode.addButton.findButton(event.x,event.y):
            mode.friend = mode.userText.getWord()
            if mode.profile.addFriend(mode.friend):
                
                mode.success = not mode.success
            else:
                mode.error = not mode.error
        elif mode.removePopUpButton.findButton(event.x,event.y):
            mode.success = False
            mode.error = False
        elif mode.backButton.findButton(event.x,event.y):
            mode.gettingFriend = True
            mode.success = False
            mode.error = False
            mode.friend = ''
            mode.userText.reset()
            mode.app.setActiveMode(mode.app.mainPage)

    def keyPressed(mode,event):
        if mode.gettingFriend:
            mode.userText.keyPressed(event)

    def drawInvalid(mode,canvas):
        x1,y1,x2,y2 = mode.width//2-200,mode.height//2-100,mode.width//2+200,mode.height//2+100
        text = "User Couldn't Be Added :("
        canvas.create_rectangle(x1,y1,x2,y2,fill = 'orange')
        canvas.create_text(mode.width//2,mode.height//2,text = text,font = 'Arial 20')

    def drawValid(mode,canvas):
        x1,y1,x2,y2 = mode.width//2-200,mode.height//2-100,mode.width//2+200,mode.height//2+100
        text = "User Has Been Added :)"
        canvas.create_rectangle(x1,y1,x2,y2,fill = 'light green')
        canvas.create_text(mode.width//2,mode.height//2,text = text,font = 'Arial 20')
    
    def redrawAll(mode,canvas):
        canvas.create_image(0,0,image = ImageTk.PhotoImage(mode.photo),anchor = 'nw')
        mode.userText.drawWord(canvas)
        if mode.error:
            canvas.create_image(mode.width//2,mode.height//2+100,image = ImageTk.PhotoImage(mode.errorPhoto))
        elif mode.success:
            canvas.create_image(mode.width//2,mode.height//2+100,image = ImageTk.PhotoImage(mode.successPhoto))

class ViewFriendsFavorites(Mode):
    def appStarted(mode):
        user = loginPage().username
        mode.Profile = Profile(user)
        mode.backHomeButton = buttons(98,68,117,96,'blue')
        mode.backSearchButton = buttons(105,64,286,100,'red')
        mode.photo = Image.open('See Friends Favorites.png')
    def mousePressed(mode,event):
        if mode.backHomeButton.findButton(event.x,event.y):
            mode.app.setActiveMode(mode.app.mainPage)
        elif mode.backSearchButton.findButton(event.x,event.y):
            mode.app.setActiveMode(mode.app.findFriends)
    def redrawAll(mode,canvas):
        canvas.create_image(0,0,image = ImageTk.PhotoImage(mode.photo),anchor = 'nw')
        mode.Profile.drawFavorites(canvas,FindFriendsFavorites().favFriend,400,200)

class ViewMyFavorites(Mode):
    def appStarted(mode):
        user = loginPage().username
        mode.Profile = Profile(user)
        mode.backButton = buttons(98,68,117,96,'blue')
        mode.photo = Image.open('Your Favorites.png')
    def mousePressed(mode,event):
        if mode.backButton.findButton(event.x,event.y):
            mode.app.setActiveMode(mode.app.mainPage)
    def redrawAll(mode,canvas):
        canvas.create_image(0,0,image = ImageTk.PhotoImage(mode.photo),anchor = 'nw')
        mode.Profile.drawFavorites(canvas,'me',400,250)   

class ViewFriends(Mode):
    def appStarted(mode):
        user = loginPage().username
        mode.Profile = Profile(user)
        mode.backButton = buttons(98,68,117,96,'blue')
        mode.photo = Image.open('Your Friends.png')
    def mousePressed(mode,event):
        if mode.backButton.findButton(event.x,event.y):
            mode.app.setActiveMode(mode.app.mainPage)
    def redrawAll(mode,canvas):
        canvas.create_image(0,0,image = ImageTk.PhotoImage(mode.photo),anchor = 'nw')
        mode.Profile.drawFriends(canvas,400,250)

class Profile(object):
    friends = []
    favorites = []
    visited = []
    @staticmethod
    def split(data):
        if len(data) == 0:
            return []
        elif ',' not in data:
            return [data]
        elif ',' in data:
            return data.split(',')

    def __init__(self,username):
        self.user = username
        self.data = []
        self.name = ''
        self.friends = []
        self.favorites = []
        with open(login_file,'r',newline = '') as f:
            self.userData = dict()
            reader = csv.DictReader(f)
            for row in reader:
                other = dict()
                if row['user'] == self.user:
                    self.userData['user'] = row['user']
                    self.userData['pass'] = row['pass']
                    self.userData['name'] = row['name']
                    self.userData['friends'] = row['friends']
                    self.userData['favorites'] = row['favorites']
                    self.userData['visited'] = row['visited']
                    self.favorites = Profile.split(row['favorites'])
                    self.friends = Profile.split(row['friends'])
                    self.visited = Profile.split(row['visited'])
                else:
                    other['user'] = row['user']
                    other['pass'] = row['pass']
                    other['name'] = row['name']
                    other['friends'] = row['friends']
                    other['favorites'] = row['favorites']
                    other['visited'] = row['visited']
                    self.data.append(other)
        Profile.friends = self.friends
        Profile.favorites = self.favorites
        Profile.visited = self.visited
        self.name = self.userData['name']
            
    

    def getFavorites(self):
        return self.favorites
    
    def getFriends(self):
        return self.friends 
    
    def addFriend(self,friend):
        users = []

        for profiles in self.data:
            users.append(profiles['user'])
        if self.user != friend and friend not in self.friends and friend in users:
            self.friends.append(friend)
            Profile.friends = self.friends
            self.update('friends')
            return True
        else:
            return False
    def addVisited(self,place):
        self.visited.append(place)
        Profile.visited = self.visited
        self.update('visited')
    def addFavorite(self,favorite):
        if favorite not in self.favorites:
            self.favorites.append(favorite)
            Profile.favorites = self.favorites
            self.update('favorites')

    def update(self,field):
        if field == 'friends':
            updating = self.friends
        elif field == 'favorites':
            updating = self.favorites
        elif field == 'visited':
            updating = self.visited
        if len(updating) == 1:
            self.userData[field] = updating[0]
        elif len(updating) > 1:
            elem = ','.join(updating)
            self.userData[field] = elem
        self.data.append(self.userData)
        self.write()
        self.data.pop()
  
    def write(self):
        with open(login_file,'w',newline = '') as f:
            fieldNames = ['user','pass','name','friends','favorites','visited']
            writer = csv.DictWriter(f,fieldNames)
            logins = self.data
            writer.writeheader()
            writer.writerows(logins)

    def getName(self):
        return self.name

    def drawFriends(self,canvas,x,y):
        nullText = "You Currently Have No Friends Added :'("
        if len(Profile.friends) == 0:
            canvas.create_text(500,600,text = nullText,font = 'Arial 30 bold')
        else:
            text = '\n'.join(Profile.friends)
            canvas.create_text(x,y,text = text,font = 'Arial 20',anchor = 'nw')

    def findFriendsFavs(self,user):
        if user in Profile.friends:
            favs = None
            for elem in self.data:
                if elem['user'] == user:
                    favs = elem['favorites']
            return Profile.split(favs)

    def drawFavorites(self,canvas,user,x,y):#call split on other data
        nullText = 'No Favorites Found'
        fav = self.findFriendsFavs(user)
        if user == 'me':
            if len(Profile.favorites) == 0:
                canvas.create_text(500,600,text = nullText,font = 'Arial 50 bold')
            else:
                myFavs = '\n'.join(Profile.favorites)
                canvas.create_text(x,y,text = myFavs,font = 'Arial 20',anchor = 'nw')
        else:
            if len(fav) == 0:
                canvas.create_text(500,500,text = nullText,font = 'Arial 50 bold')
            else:
                friendFavs = '\n'.join(fav)
                canvas.create_text(x,y,text = friendFavs,font = 'Arial 20',anchor = 'nw')

class Graph(object):
    buttonLocations = set()
    def __init__(self):
        self.graphData = MainPage().data
        self.data = sorted(self.graphData, key = lambda x: x[0])
        self.drawLineData = []
        self.maxdistance = StartScreen().radiusMiles
        self.radius = 4
        self.width = 250
        self.height = 250
        self.margin = 50
        self.tickLength = 5

    def findDot(self,x,y):
        for elem in Graph.buttonLocations:
            if elem[0] < x < elem[2] and elem[1] < y < elem[3]:
                return elem[4]

        return None
            
    def drawPoint(self,canvas,distance,rating,x1,y1,x2,y2,index,color):
        x = x1+self.margin+(distance*((x2-x1-2*self.margin)/self.maxdistance))
        y = y2-self.margin-(rating*((y2-y1-2*self.margin)/5))
        x1,y1,x2,y2 = x - self.radius, y - self.radius,x + self.radius, y + self.radius
        Graph.buttonLocations.add((x1,y1,x2,y2,index))
        canvas.create_oval(x1,y1,x2,y2,fill = color)
        return (x,y)

    def drawLine(self,canvas,point1,point2):
        x1,y1 = point1[0], point1[1]
        x2,y2 = point2[0], point2[1]
        if x1 != x2:
            canvas.create_line(x1,y1,x2,y2,width = 3)
        
    def drawYTicks(self,canvas,x1,y1,x2,y2):
        space = (y2-y1-2*self.margin)/5
        for i in range(6):
            text = f'{i}'
            canvas.create_line(x1+self.margin-self.tickLength,y2-self.margin-space*i,x1+self.margin+self.tickLength,y2-self.margin-space*i)
            canvas.create_text(x1+self.margin-2*self.tickLength,y2-self.margin-space*i, text = text, font = 'Arial 10')

    def drawXTicks(self,canvas,x1,y1,x2,y2):
        space = (x2-x1-2*self.margin)//self.maxdistance
        for i in range(self.maxdistance +1):
            text = f'{i}'
            canvas.create_line(x1+self.margin+space*i,y2-self.margin+self.tickLength,x1+self.margin+space*i,y2-self.margin-self.tickLength)
            canvas.create_text(x1+self.margin+space*i,y2-self.margin+2*self.tickLength, text = text, font = 'Arial 10')

    def drawGraph(self,canvas,x1,y1,x2,y2):
        canvas.create_rectangle(x1,y1,x2,y2,fill = 'white')
        canvas.create_line(x1+self.margin,y2-self.margin,x2-self.margin,y2-self.margin)
        canvas.create_line(x1+self.margin,y2-self.margin,x1+self.margin,y1+self.margin)
        canvas.create_text(x1+(self.margin//2),(y1+y2)//2, text = 'Rating', font = 'Arial 8 bold')
        canvas.create_text((x1+x2)//2,y2-(self.margin//2), text = 'Distance (miles)', font = 'Arial 8 bold')
        self.drawXTicks(canvas,x1,y1,x2,y2)
        self.drawYTicks(canvas,x1,y1,x2,y2)
        linePoints = []
        for elem in self.graphData:
            x,y,index = elem[0],elem[1],elem[2]
            x = self.drawPoint(canvas,x,y,x1,y1,x2,y2,index,'black') 
            linePoints.append(x)

class text(object):
    def __init__(self,x1,y1):
        self.x1 = x1
        self.y1 = y1
        self.letters = []
        self.word = ''
        self.hidden = ''
        self.hiddenLetters = []
    def keyPressed(self,event):
        allowed = [',','Space']
        if event.key in string.ascii_letters or event.key in string.digits or event.key in allowed:
            if event.key == 'Space':
                self.letters.append(' ')
                self.hiddenLetters.append('*')
            else:
                self.letters.append(event.key)
                self.hiddenLetters.append('*')
            self.word = ''.join(self.letters)
            self.hidden = ''.join(self.hiddenLetters)
        elif event.key  == 'Backspace':
            if len(self.letters) != 0:
                self.letters.pop()
                self.word = ''.join(self.letters)
                self.hiddenLetters.pop()
                self.hidden = ''.join(self.hiddenLetters)
    def findBox(self,x,y):
        if self.x1 < x < self.x1 + 500 and self.y1 < y < self.y1 + 100:
            return True
    def reset(self):
        self.word = ''
        self.letters = []
        self.hidden = ''
        self.hiddenLetters = []
    def getWord(self):
        return self.word
    def getHidden(self):
        return self.hidden
    def drawhideWord(self,canvas):
        canvas.create_text(self.x1,self.y1,text = self.hidden,font = 'Arial 30',anchor = 'nw')
    def drawWord(self,canvas):
        canvas.create_text(self.x1,self.y1,text = self.word,font = 'Arial 30',anchor = 'nw')

class buttons(object):

    def __init__(self,width,height,cx,cy,color):
        self.width = width
        self.height = height
        self.cx = cx
        self.cy = cy
        self.color = color
        self.x1 = self.cx - self.width//2
        self.y1 = self.cy - self.height//2
    def findButton(self,x,y):
        if (x >= self.x1 and x <= self.x1 + self.width and 
                y >= self.y1 and y<= self.y1 + self.height):
            return True
    def drawButton(self,canvas):
        x1,y1,x2,y2 = (self.cx - self.width//2,self.cy-self.height//2,
                        self.cx+self.width//2,self.cy+self.height//2)
        canvas.create_rectangle(x1,y1,x2,y2,fill = self.color,width = 0)

class yelp(object):
    restaurants = []
    graphData = []
    @staticmethod
    def openHours(openTimes):
        return '\n'.join(openTimes)
    @staticmethod
    def convertDays(num):
        days = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
        return days[num]
    @staticmethod
    def convertTime(milTime):
        noon = 1200
        if milTime <= str(noon):
            if milTime == '0000':
                return '12:00 am'
            elif milTime[0] == '0':
                top,bottom = milTime[1],milTime[2:]
                time = top + ':' + bottom
                return f'{time} am'
            else:
                top,bottom = milTime[:2],milTime[2:]
                time = top + ':' + bottom
                return f'{time} am'
        else:
            milTime = str(int(milTime) - noon)
            mid = len(milTime)//2
            top,bottom = milTime[:mid],milTime[mid:]
            time = top + ':' + bottom
            return f'{time} pm'
    @staticmethod
    def priceConverter(price):
        priceRating = price.count('$')
        if priceRating == 1:
            return 'Price: <$10'
        elif priceRating == 2:
            return 'Price: 11$ - 30$'
        elif priceRating == 3:
            return 'Price: 31$ - 60$'
        else:
            return 'Price: >61$'
    @staticmethod
    def meterToMile(meter):
        meterToMile = 0.000621371
        distance = yelp.roundHalfUp(meter*meterToMile)
        if distance > 1:
            return f'{distance} miles away'
        else:
            return f'{distance} mile away'
    @staticmethod
    def getDistance(value):
        meterToMile = 0.000621371
        distance = yelp.roundHalfUp(value*meterToMile)
        return distance

    @staticmethod
    def doesElemExist(elem,IdData):
        value = IdData.get(elem,'Not Listed')
        return value   
    # taken from : https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html 
    @staticmethod
    def roundHalfUp(d):
        rounding = decimal.ROUND_HALF_UP
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))    
    @staticmethod
    def createTuple(distance,rating,index):
        datapoint = (distance,rating,index)
        yelp.graphData.append(datapoint)
    def __init__(self,elem,headers):
        userDistance = StartScreen().radiusMiles
        user = loginPage().username
        self.isNew = False
        self.hasDistance = False
        self.hasLocation = False
        self.hasHours = False
        self.hasRating = False
        self.id = elem['id']
        IdUrl = f'https://api.yelp.com/v3/businesses/{self.id}'
        IdResponse = requests.get(url = IdUrl, headers = headers)
        IdData = IdResponse.json()
        self.name = yelp.doesElemExist('name',IdData)
        if self.name not in Profile(user).visited:
            self.isNew = True
        money = yelp.doesElemExist('price',IdData)
        if money != 'Not Listed':
            self.price = yelp.priceConverter(money)
        else:
            self.price = None
        address = yelp.doesElemExist('location',IdData)
        if address != 'Not Listed':
            address = ' '.join(IdData['location']['display_address'])
            address = address.split(',')
            self.address = '\n'.join(address)
            self.hasLocation = True
        self.distance = yelp.meterToMile(elem['distance']) 
        distance = yelp.getDistance(elem['distance'])
        if distance < userDistance:
            self.span = distance
            self.hasDistance = True
        phone = yelp.doesElemExist('phone',IdData)
        self.phone = f'Phone: {phone}' 
        rating = yelp.doesElemExist('rating',IdData)
        if rating == 'Not Listed':
            self.rating = None
        else:
            self.rating = f'{rating}/5'
            self.rate = rating
            self.hasRating = True
        self.photos = yelp.doesElemExist('photos',IdData)
        self.numOfPhotos = len(self.photos) - 1
        daysOpen = []
        if yelp.doesElemExist('hours',IdData) == 'Not Listed':
            pass
        else:
            days = len(IdData['hours'][0]['open'])
            self.hasHours = True
            for i in range(days):
                day = yelp.convertDays(IdData['hours'][0]['open'][i]['day'])
                start = yelp.convertTime(IdData['hours'][0]['open'][i]['start'])
                end = yelp.convertTime(IdData['hours'][0]['open'][i]['end'])
                hours = f'{day} {start} - {end}'
                daysOpen.append(hours)
        if len(daysOpen) > 0:
            self.hours = yelp.openHours(daysOpen)
            if IdData['hours'][0]['is_open_now']:
                self.isOpen = 'Open'
            else:
                self.isOpen = 'Closed'
        else:
            self.hours = 'Not Listed'
            self.isOpen = 'Not Listed'
        if self.rating != None and self.price != None and self.hasHours and self.hasLocation and self.hasDistance and self.hasRating and self.isNew:
            yelp.restaurants.append(self)
            index = len(yelp.restaurants) - 1
            yelp.createTuple(distance,rating,index)

class match(Mode):
    def appStarted(mode):
        mode.user = loginPage().username
        mode.name = MainPage().matchName
        mode.address = MainPage().matchAddress
        mode.profile = Profile(mode.user)
        mode.profile.addVisited(mode.name)
    # taken from homework 2
    def rgbString(mode,red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)

    def redrawAll(mode,canvas):
        color = mode.rgbString(208,240,192)
        canvas.create_rectangle(0,0,mode.width,mode.height,fill = color)
        canvas.create_text(mode.width//2,mode.height//4,text = "You Matched With",font = 'Arial 20 bold')
        canvas.create_text(mode.width//2,mode.height//2.5,text = mode.name,font = 'Arial 40 bold')
        canvas.create_text(mode.width//2,mode.height//1.85,text = 'at',font = 'Arial 20 bold')
        canvas.create_text(mode.width//2,mode.height//1.5,text = mode.address, font = 'Arial 25 bold')
        canvas.create_text(mode.width//2,mode.height//1.1,text = "Press 'ENTER' To Go Back",font = 'Arial 15')
    
    def keyPressed(mode,event):
        if event.key == 'Enter':
            mode.app.setActiveMode(mode.app.mainPage)

class RestaurantApp(ModalApp):
    
    def appStarted(app):
        app.mainPage = MainPage()
        app.viewMyFavorites = ViewMyFavorites()
        app.viewFriends = ViewFriends()
        app.addFriends = AddFriends()
        app.findFriends = FindFriendsFavorites()
        app.viewFriendsFavorites = ViewFriendsFavorites()
        app.matchScreen = match()
        app.login = loginPage()
        app.start = StartScreen()
        app.setActiveMode(app.login)

app = RestaurantApp(width = 1000, height = 1000)
        

