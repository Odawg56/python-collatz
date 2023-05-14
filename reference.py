import os, db, kivy, random, webbrowser, datetime
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, Property

class login(Screen):
    def on_enter(self,*args):
        Window.size = (460, 760)
        loc = self.manager.get_screen("login")
        loc.username.text = ''
        loc.password.text = ''
    def loginPressed(self):
        loc = self.manager.get_screen("login")
        acc = db.checkAccountExists(conn, loc.username.text, loc.password.text) #acc exists, password correct, acc type, id
        if acc[0] == True and acc[1] == True:
            print("Access Granted;",acc[3])
            if acc[2] == 'normal':
                self.manager.current = "mainScreen"
                self.manager.transition.direction = "left" #go to the main screen
                loc = self.manager.get_screen("mainScreen")
                loc.backloc = "login"
                loc.activeUser = acc[3]
            else:
                self.manager.current = "adminView"
                self.manager.transition.direction = "left" #go to the main screen
                loc = self.manager.get_screen("adminView")
                loc.backloc = "login"
                loc.activeUser = acc[3]
        elif acc[0] == True and acc[1] == False:
            print("Password Incorrect!!")
        elif acc[0] == False:
            print("Account Not Found.")

class createAccount(Screen):
    def on_enter(self,*args):
        Window.size = (460, 760)
        loc = self.manager.get_screen("createAccount")
        loc.username.text = ''
        loc.password.text = ''
    def createAccPressed(self):
        loc = self.manager.get_screen("createAccount")
        acc = db.checkAccountExists(conn, loc.username.text, loc.password.text, "createAccount") #acc exists
        if acc:
            print("Account Already Exists!")
        else:
            val = False
            knownIDs = db.getIDs(conn)
            while val == False:
                proposedID = random.randint(1,9999999)
                val = True
                if proposedID in knownIDs:
                    val = False
            newUser = [proposedID,loc.username.text,loc.password.text,'normal']
            db.enterData(conn, "users", newUser)
            self.manager.current = "login"
            self.manager.transition.direction = "left"
class mainScreen(Screen):
    def on_enter(self,*args):
        Window.size = (460, 760)
    def logoutPressed(self):
        loc = self.manager.get_screen("mainScreen")
        loc.activeUser = "None"
        print("Successfully Logged Out")
        self.manager.current = "login"
        self.manager.transition.direction = "right"
    def searchPressed(self):
        self.manager.get_screen("search").activeUser = self.manager.get_screen("mainScreen").activeUser
        self.manager.current = "search"
        self.manager.transition.direction = "right"

class saved(Screen):
    def goBack(self):
        self.manager.current = self.manager.get_screen("saved").backLoc
        self.manager.transition.direction = "right"
    def on_enter(self,*args):
        Window.size = (460, 760)
        loc = self.manager.get_screen("saved")
        loc.field.clear_widgets()
        Parks = db.getSaved(conn,self.manager.get_screen("mainScreen").activeUser)
        for p in Parks:
            class b(Button):
                def __init__(self,**kwargs): #
                    super().__init__(**kwargs)
                    self.text=str(p[1]).title() +"\n"+p[0]
                    self.background_color=loc.buttonColor
                    self.background_normal=""
                    self.color=(0,0,0,1)
                    self.id_prop=Property(p[0])
                    self.bind(on_press=self.pressed)
                def pressed(instance,value): #function to assign a screen property to this buttons' linked id (to be used later)
                    spot = self.manager.get_screen("search")
                    spot.selectedButton = value.id_prop.defaultvalue
                    self.manager.get_screen("details").activeID=spot.selectedButton
                    self.manager.get_screen("details").backLoc="saved"
                    self.manager.current = "details"
                    self.manager.transition.direction = "left"
            loc.field.add_widget(b())

class search(Screen):
    def goBack(self):
        self.manager.current = self.manager.get_screen("search").backLoc
        self.manager.transition.direction = "right"
    def refresh_results(self, *args,results=[]):
        loc = self.manager.get_screen("search")
        loc.field.clear_widgets()
        if results == []:
            results = db.getSearched(conn,"%QUAN%")
        for result in results:
            class b(Button):
                def __init__(self,**kwargs): #
                    super().__init__(**kwargs)
                    self.text=str(result[1]).title() +"\n"+result[0]
                    self.background_color=loc.buttonColor
                    self.background_normal=""
                    self.color=(0,0,0,1)
                    self.id_prop=Property(result[0])
                    self.bind(on_press=self.pressed)
                def pressed(instance,value): #function to assign a screen property to this buttons' linked id (to be used later)
                    spot = self.manager.get_screen("search")
                    spot.selectedButton = value.id_prop.defaultvalue
                    self.manager.get_screen("details").activeID=spot.selectedButton
                    self.manager.get_screen("details").backLoc="search"
                    self.manager.current = "details"
                    self.manager.transition.direction = "left"
            loc.field.add_widget(b())
    def on_enter(self, *args):
        Window.size = (460, 760)
        search.refresh_results(self,*args)
        self.manager.get_screen("search").searchField.text = ""
    def submit_search(self): #algorithm getSearchParameters()
        loc = self.manager.get_screen("search")
        sP = "%" + loc.searchField.text.upper() + "%" #get search phrase & convert with wildcards
        search.refresh_results(self,results=db.getSearched(conn, sP))
class details(Screen):
    def on_enter(self,*args):
        loc = self.manager.get_screen("details")
        loc.featureField1.clear_widgets()
        loc.featureField2.clear_widgets()
        data = db.getDetails(conn,loc.activeID)
        loc.activeUser = self.manager.get_screen("mainScreen").activeUser
        loc.saveState = db.checkSaved(conn, loc.activeID, loc.activeUser)
        if loc.saveState == False: #'retexture' the save button
            loc.saveButton.text = "Save <3"
        elif loc.saveState == True:
            loc.saveButton.text = "Unsave :("
        loc.lat.text = "Latitude: "+ str(data["lat"])
        loc.long.text = "Longitude: "+ str(data["long"])
        loc.title.text = str(data["name"]).title()
        
        known = []
        good = []
        for feat in data["features"]:
            if feat[1] == "d" and feat[0] not in known:
                known.append(feat[0])
                good.append(feat[0])
        i = 0
        for g in good:
            class l(Label):
                def __init__(self,**kwargs): 
                    super().__init__(**kwargs)
                    self.text="-  "+str(g).title()
                    self.background_color=loc.buttonColor
                    self.background_normal=""
                    self.color=(0,0,0,1)
                    self.font_size=10
            if i > (len(good)/2):
                loc.featureField2.add_widget(l())
            else:
                loc.featureField1.add_widget(l())
            i += 1
        
    def goBack(self):
        self.manager.current = self.manager.get_screen("details").backLoc
        self.manager.transition.direction = "right"
    def savePressed(self):
        loc = self.manager.get_screen("details")
        currentId = loc.activeID
        currentUser = loc.activeUser
        if loc.saveState == False:
            db.savePark(conn, currentId, currentUser, loc.saveState)
            loc.saveState = True
            loc.saveButton.text = "Unsave :("
        elif loc.saveState == True:
            db.savePark(conn, currentId, currentUser, loc.saveState)
            loc.saveState = False
            loc.saveButton.text = "Save <3"
    def goMaps(self):
        link = 'https://www.google.com/maps/search/?api=1&query={0},{1}'
        loc = self.manager.get_screen("details")
        data = db.getDetails(conn,loc.activeID)
        link = link.format(str(data["lat"]),str(data["long"]))
        webbrowser.open(link)
class adminView(Screen):
    def on_enter(self,*args):
        Window.size = (1600, 900)
        adminView.refreshValues(self,conn)
    def goBack(self):
        self.manager.current = self.manager.get_screen("adminView").backLoc
        self.manager.transition.direction = "right"
    def backup(self):
        print("Initiating backup...")
        d = datetime.datetime.now()
        name = "export_"+str(d.year)+"_"+str(d.month)+"_"+str(d.day)+"_"+str(d.hour)+"_"+str(d.minute)+"_"+str(d.second)+".csv"
        db.exportNew(name,conn)
        print("Export completed as",name)

    def refreshValues(self,conn):
        loc = self.manager.get_screen("adminView")
        loc.all.clear_widgets() #clear results to make room and stop duplication
        loc.users.clear_widgets()
        loc.parks.clear_widgets()
        #loc.features.clear_widgets()  #this has been disabled, as Kivy cannot handle 108,000+ widgets
        loc.savedParks.clear_widgets()
        dict = {"all":loc.all,"users":loc.users,"parks":loc.parks,"savedParks":loc.savedParks} #REMOVED: "features":loc.features,
        def addEntries(conn, place, s): #function is used to compact code
            data = db.getAdminData(conn, s)
            for d in data:
                class l(Label):
                    def __init__(self,**kwargs): 
                        super().__init__(**kwargs)
                        self.text=str(d)
                        self.color=(0,0,0,1)
                        self.font_size=14
                place.add_widget(l())                
        for sect in dict.keys(): # actually add widgets to the tabs
            if sect == 'all':
                for sect2 in dict.keys(): #get data from all tables and add it
                    if sect2 != 'all':
                        addEntries(conn, loc.all, sect2)
            else:
                addEntries(conn, dict[sect], sect) #get data from specific table with name of dict.key
class MyApp(App):
    def build(self):
        sm = ScreenManager() #add all of the screens to the screen manager
        sm.add_widget(login())
        sm.add_widget(createAccount())
        sm.add_widget(mainScreen())
        sm.add_widget(saved())
        sm.add_widget(search())
        sm.add_widget(details())
        sm.add_widget(adminView())
        return sm

def dbsetup():
    dbDir = db.define_path("main.db")
    # if there is data in the database, do nothing. if there is none, try to import from new file, if all else fails, import from old file.
    oldDataDir = db.define_path("parkData.csv")
    newDataDir = db.define_path("export.csv")
    nExists = os.path.exists(newDataDir)
    dbExists = os.path.exists(dbDir)
    if not dbExists:
        conn = db.getConnection(dbDir)
        db.execSQL(conn,"createTables.txt")
        if nExists:
            db.importNew(newDataDir,conn)
        else:
            db.fullImportOld(oldDataDir, conn)
    else:
        conn = db.getConnection(dbDir)
    return conn
    #db.exportNew("export.csv",conn)

if __name__=="__main__":
    conn = dbsetup()
    MyApp().run()