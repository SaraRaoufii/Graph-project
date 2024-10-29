import json
from queue import Queue
class graph:
    def __init__(self):
        self.users={}
    def insert(self,user):
        self.users[user.id]=user
    def readdata(self,file):
        self.users={}
        with open(file,'r') as obj:
          data=json.load(obj)
        for user in data:
            user_=detail_user(user["id"],user["name"],user["dateOfBirth"],user["universityLocation"],user["field"],user["workplace"],user["specialties"],user["connectionId"])
            self.insert(user_)
    def print(self,user_):
        user=self.users.get(user_)
        print("user_id=",user.id)
        print("user_name=",user.name)
        print("user_dateOfBirth=",user.dateOfBirth)
        print("user_universityLocation=",user.universityLocation)
        print("user_field=", user.field)
        print("user_workplace=",user.workplace)
        print("user_specialties=",user.specialties)
        print("user_connectionId=",user.connectionId)
        print("*"*100)
    def delete(self,user_id):
        del self.users[user_id]
        for user in self.users:
            user=self.users.get(user)
            if user_id in user.connectionId:
                user.connectionId.remove(user_id)
    def path(self,user1,user2):
        visit=[]
        q=Queue()
        q.put((user1,0))
        degree=0
        while q and degree<=5:
            n_user,degree=q.get()
            if n_user==user2:
                return degree
            visit.append(n_user)
            n_user=self.users.get(n_user)
            for connect in n_user.connectionId:
                if connect not in visit:
                    q.put((connect,degree+1))
        return False
# this def is for suggesting a list of user for connecting
    def suggest_c(self,user_id,number=20):
        weight_field=6
        weight_uni=5
        weight_specialties=4
        weight_workp=3
        weight_degree=2
        weight_connect=1
        user_t=self.users.get(user_id)
        suggest=[]
        for user in self.users:
            user=self.users.get(user)
            if user.id != user_t.id and user.id not in user_t.connectionId:
                degree=self.path(user_t.id,user.id)
                if degree!=False:
                    Priority=0
                    if user_t.field==user.field:
                        Priority=weight_field+Priority
                    if user_t.universityLocation==user.universityLocation:
                        Priority=weight_uni+Priority
                    sp=len(list(set(user_t.specialties).intersection(user.specialties)))
                    Priority=weight_specialties*sp+Priority
                    if user_t.workplace==user.workplace:
                        Priority=weight_workp+Priority
                    Priority=Priority+degree*weight_degree
                    c=len(list(set(user_t.connectionId).intersection(user.connectionId)))
                    Priority=Priority+c
                suggest.append((user.id,Priority))
        suggest.sort(key=lambda x: x[1], reverse=True)
        suggestion=[]
        for i in range(number):
            suggestion.append(suggest[i][0])
        return suggestion


class detail_user:
    def __init__(self,id,name,birth,university,field,work,specialties,connectionId):
        self.id=id
        self.name=name
        self.dateOfBirth=birth
        self.universityLocation=university
        self.field=field
        self.workplace=work
        self.specialties=specialties
        self.connectionId=connectionId

class userinterface:
    def __init__(self,users):   
        self.users=users
        self.person=None
    def insert_user(self,newuser):
       user_=detail_user(newuser["id"],newuser["name"],newuser["dateOfBirth"],newuser["universityLocation"],newuser["field"],newuser["workplace"],newuser["specialties"],newuser["connectionId"])
       social_network.insert(user_)
    def check(self,user_id):
        if user_id in social_network.users:
            social_network.print(user_id)
        else:
            print(user_id,"did not find")
    def find(self, user_):
        for user in social_network.users:
            user=social_network.users.get(user)
            if user.id==user_ or user.name==user_:
                social_network.print(user.id)
    def login(self,user_id):
        for user in social_network.users:
            user=social_network.users.get(user)
            if user.id==user_id:
                self.person=user_id
                print("You logged in")
                return
        print("the user_id did not find")
 #this def is for connecting with other user.       
    def connect(self,user1,user2):
        if user1 in social_network.users and user2 in social_network.users:
            user1=social_network.users.get(user1)
            user2=social_network.users.get(user2)
            user1.connectionId.append(user2.id)
            user2.connectionId.append(user1.id)
            print("These two users are connected")
        else:
            print("user1 or user2 did not find")
    def disconnect(self,user1,user2):
        if user1 in social_network.users and user2 in social_network.users:
            user1=social_network.users.get(user1)
            user2=social_network.users.get(user2)
            if user1.id in user2.connectionId or user2.id in user1.connectionId:
                user1.connectionId.remove(user2.id)
                user2.connectionId.remove(user1.id)
                print("These two users are no longer connected")
            else:
              print("user1 and user2 do not have connection")
        else:
            print("user1 or user2 did not find")

#In this part, the user enters the input, and according to that the corresponding function is executed.
social_network=graph()
file=input("enter file_name= ")
social_network.readdata(file)
user_interface=userinterface(social_network.users)
while True:
    print("1:add new user , 2:go to your panel , 3:View a user's profile , 4:view all users , 5:search a user , 6:connect users , 7:disconnect users , 8:recommend connections , 9:delete acount , 10:exit")
    work=input("Enter your choise= ")
    
    if work=="1":
        print("complete the form")
        id=input("enter your user id= ")
        if id in social_network.users:
            print("this id exists , enter another id")
            break
        name=input("enter your name= ")
        birth=input("enter your data of birth= ")
        university=input("enter your university= ")
        field=input("enter your field= ")
        workplace=input("enter your workplace= ")
        specialties=list(input("enter your specialties= ").split())
        connectionId=[]
        newuser={"id":id ,"name":name,"dateOfBirth":birth,"universityLocation":university,"field":field,"workplace":workplace,"specialties":specialties,"connectionId":connectionId}
        user_interface.insert_user(newuser)
        print("your account creat")
        
    elif work=="2":
        user_id=input("enter your user_id=")
        user_interface.login(user_id)
        while True:
            print("1:view your information , 2:logout , 3:delete your acount , 4:recommend connections , 5:connect a user , 6:disconnect a user")
            choise=input("enter your choise= ")
            if choise=="1":
                print("your information is:")
                social_network.print(user_interface.person)
            
            elif choise=="2":
                user_interface.person=None
                break
            
            elif choise=="3":
                social_network.delete(user_interface.person)
                user_interface.person=None
                print("Your account has been deleted")
                break
            
            elif choise=="4":
                suggest=social_network.suggest_c(user_interface.person)
                print("your suggest connections are:")
                print(suggest)
            
            elif choise=="5":
                userid=input("enter the user id=")
                user_interface.connect(user_interface.person,userid)
            
            elif choise=="6":
                userid=input("enter the user id=")
                user_interface.disconnect(user_interface.person,userid)

    elif work=="3":
        userid=input("enter user_id= ")
        user_interface.check(userid)
    
    elif work=="4":
        for user in social_network.users:
            print(user)
    
    elif work=="5":
        user=input("enter user_id or user_name= ")
        user_interface.find(user)
    
    elif work=="6":
        user1=input("enter user1 id= ")
        user2=input("enter user2 id=")
        user_interface.connect(user1,user2)
    
    elif work=="7":
        user1=input("enter user1 id= ")
        user2=input("enter user2 id=")
        user_interface.disconnect(user1,user2)
    
    elif work=="8":
        user_id=input("enter user id=")
        if user_id in social_network.users:
          suggest=social_network.suggest_c(user_id)
          print("the user's suggest:")
          print(suggest)
        else:
            print("the user_id did not find")
    
    elif work=="9":
        user_id=input("enter user id=")
        if user_id in social_network.users:
           social_network.delete(user_id)
           print("the user id was deleted")
        else:
            print("the user_id did not find")
    
    elif work=="10":
        break





