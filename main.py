import os, kivy, collatzDB, collatz, random, datetime
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty, Property
print({'profile_name': 'test profile 2', 'even_angle': 20.0, 'odd_angle': 20.0, 'stroke_length': 10, 'x_start': 15, 'y_start': 15,
    'pen_size': 10, 'perspective': 'Default', 'bgColor': 'Black', 'additive': True, 'start_i': 1, 'finish_i': 200}.keys())
class mainScreen(Screen):
    def on_pre_enter(self, *args):
        Window.size = (1280,720)
        mainScreen.searchConfirm(self,True)
        return super().on_pre_enter(*args)
    def get_details(self):
        loc = self.manager.get_screen("mainScreen")
        try:
            fields = {"profile_name":str(loc.profile_name.text),"even_angle":float(loc.even_angle.text),
                    "odd_angle":float(loc.odd_angle.text),"stroke_length":int(loc.stroke_length.text),
                    "x_start":int(loc.x_start.text),"y_start":int(loc.y_start.text),"pen_size":int(loc.pen_size.text)}
            return fields
        except ValueError as e:
            return e
    def load_details(self,profile_name):
        loc = self.manager.get_screen("mainScreen")
        details = collatzDB.execSelect(conn,"pullDetails.txt",profile_name)[0]
        loc.profile_name.text = str(details[0]) #actually set text content of detail slots
        loc.even_angle.text = str(details[1])
        loc.odd_angle.text = str(details[2])
        loc.stroke_length.text = str(details[3])
        loc.x_start.text = str(details[4])
        loc.y_start.text = str(details[5])
        loc.pen_size.text = str(details[6])
    def searchConfirm(self,mode=False):
        loc = self.manager.get_screen("mainScreen")
        term = loc.searchBox.text
        print(f"Search Term Confirmed: {term}")
        term = "%"+term+"%"
        if not mode: 
            results = collatzDB.execSelect(conn,"getSearched.txt",term)
        else:
            results = collatzDB.execSelect(conn,"getDefault.txt",'')
        #print(results)
        loc.profile_list.clear_widgets()
        for p in results:
            class b(Button):
                def __init__(self,**kwargs): #
                    super().__init__(**kwargs)
                    self.text=str(p[0])
                    self.background_color=loc.buttonColor
                    self.background_normal=""
                    self.font_size=24
                    self.color=(0,0,0,1)
                    self.id_prop=Property(p[0])
                    self.bind(on_press=self.pressed)
                def pressed(instance,value):
                    self.manager.get_screen('mainScreen').selectedProfile = str(value.id_prop.defaultvalue)
                    #print("selected profile changed to:", self.manager.get_screen('mainScreen').selectedProfile)
                    mainScreen.load_details(self,value.id_prop.defaultvalue)
            loc.profile_list.add_widget(b())
    def clearFields(self):
        loc = self.manager.get_screen("mainScreen")
        fields = ["profile_name","even_angle","odd_angle","stroke_length","x_start","y_start","pen_size"]
        loc.profile_name.text = ''
        loc.even_angle.text = ''
        loc.odd_angle.text = ''
        loc.stroke_length.text = ''
        loc.x_start.text = ''
        loc.y_start.text = ''
        loc.pen_size.text = ''
    def SaveAsNew(self):
        print("Saving as new profile...")
        fields = mainScreen.get_details(self)
        print(collatzDB.execAddProfile(conn,fields))
        mainScreen.searchConfirm(self)
    def SaveUpdate(self): 
        print("Updating existing entry with changes...")
        loc = self.manager.get_screen("mainScreen")
        fields = mainScreen.get_details(self)
        print(collatzDB.execUpdateProfile(conn, (loc.selectedProfile,)+tuple(fields.values())))
        mainScreen.searchConfirm(self)
    def perspective_clicked(self,value):
        print("persp clicked")
    def bgColor_clicked(self,value):
        print("bg colour clicked")
    def startCollatz(self):
        print("Starting Collatz Render...")
        details1 = mainScreen.get_details(self)
        if type(details1) == dict:
            loc = self.manager.get_screen("mainScreen")
            details1["perspective"] = loc.ids.perspective.text
            details1["bgColor"] = loc.ids.bgColor.text
            details1["additive"] = bool(loc.ids.additiveBox.active)
            details1["start_i"] = int(loc.ids.start_i.text)
            details1["finish_i"] = int(loc.ids.finish_i.text)
            print(details1)
            collatz.drawCollatz(details1)
        else:
            print(f"Error in field data collection: {details1}")
class CustomDropDown(DropDown):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager() #add all of the screens to the screen manager
        sm.add_widget(mainScreen())
        return sm

if __name__=="__main__":
    dbDir = collatzDB.define_path("profiles.db")
    conn = collatzDB.getConnection(dbDir)
    collatzDB.execSQL(conn,"tables.txt")
    MyApp().run()