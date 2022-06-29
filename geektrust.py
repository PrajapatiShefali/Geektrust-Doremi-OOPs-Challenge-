
from sys import argv
import datetime
from unicodedata import category
from dateutil.relativedelta import relativedelta


class Date:
    
    def __init__(self) -> None:
        self.date=None 
    
    def validate(self,date):
        if not (1<=int(date[0])<=31 and 1<=int(date[1])<=12 and 1000<=int(date[2])<=9999):
            return False 
        return True 
        
              
    def set_date(self,date):
        lst=date.split("-")
        if self.validate(lst):
            self.date=datetime.date(int(lst[2]),int(lst[1]),int(lst[0]))
            return self.date
        else:
            print("INVALID_DATE")
            return None
        


class Plan:
    def __init__(self) -> None:
        pass
    
    def __init__(self,name=None,duration=None,amount=None,date=None):
        self.name=name 
        self.Duration=duration
        self.price=amount 
        self.devices=1 
        self.end_date=date

    def get_price(self):
        return self.price
    def change_date(self,month):
        self.end_date=self.end_date+relativedelta(months=+month)
    
    def set_reminder(self,category):
        renewal=self.end_date-datetime.timedelta(10)
        format=str(renewal).split("-")[::-1]
        
        print("RENEWAL_REMINDER "+category+" "+"-".join(format))

class Plan_values:
    MUSIC_FREE_DURATION=1
    MUSIC_FREE_PRICE=0
    MUSIC_PERSONAL_DURATION=1
    MUSIC_PREMIUM_DURATION=3
    MUSIC_PREMIUM_PRICE=250
    MUSIC_PERSONAL_PRICE=100

    VIDEO_FREE_DURATION=1
    VIDEO_FREE_PRICE=0
    VIDEO_PERSONAL_DURATION=1
    VIDEO_PREMIUM_DURATION=3
    VIDEO_PREMIUM_PRICE=500
    VIDEO_PERSONAL_PRICE=200

    PODCAST_FREE_DURATION=1
    PODCAST_FREE_PRICE=0
    PODCAST_PREMIUM_PRICE=300
    PODCAST_PERSONAL_PRICE=100
    PODCAST_PERSONAL_DURATION=1
    PODCAST_PREMIUM_DURATION=3

    FOUR_DEVICE_PRICE=50
    TEN_DEVICE_PRICE=100

class Category(Plan):
    def __init__(self,category=None,plan=None) -> None:
        Plan().__init__()
        Date().__init__()
        self.plan_taken=Plan(self)
        self.category=None

    def set_plan_music(self,plan_name,date):
        if plan_name=="FREE":
            self.plan_taken=Plan(plan_name,Plan_values.MUSIC_FREE_DURATION,Plan_values.MUSIC_FREE_PRICE,date)
        elif plan_name=="PERSONAL":
            self.plan_taken=Plan(plan_name,Plan_values.MUSIC_PERSONAL_DURATION,Plan_values.MUSIC_PERSONAL_PRICE,date)
        elif plan_name=="PREMIUM":
            self.plan_taken=Plan(plan_name,Plan_values.MUSIC_PREMIUM_DURATION,Plan_values.MUSIC_PREMIUM_PRICE,date)
    
    def set_plan_video(self,plan_name,date):
        if plan_name=="FREE":
                self.plan_taken=Plan(plan_name,Plan_values.VIDEO_FREE_DURATION,Plan_values.VIDEO_FREE_PRICE,date)
        elif plan_name=="PERSONAL":
            self.plan_taken=Plan(plan_name,Plan_values.VIDEO_PERSONAL_DURATION,Plan_values.VIDEO_PERSONAL_PRICE,date)
        elif plan_name=="PREMIUM":
            self.plan_taken=Plan(plan_name,Plan_values.VIDEO_PREMIUM_DURATION,Plan_values.VIDEO_PREMIUM_PRICE,date)

    def set_plan_podcast(self,plan_name,date):
        if plan_name=="FREE":
                self.plan_taken=Plan(plan_name,Plan_values.PODCAST_FREE_DURATION,Plan_values.PODCAST_FREE_PRICE,date)
        elif plan_name=="PERSONAL":
                self.plan_taken=Plan(plan_name,Plan_values.PODCAST_PERSONAL_DURATION,Plan_values.PODCAST_PERSONAL_PRICE,date)
        elif plan_name=="PREMIUM":
                self.plan_taken=Plan(plan_name,Plan_values.PODCAST_PREMIUM_DURATION,Plan_values.PODCAST_PREMIUM_PRICE,date)

    def setPlan(self,cat,plan_name,date):
        self.category=cat 
        if cat=="MUSIC":
            self.set_plan_music(plan_name,date)
        elif cat=="VIDEO":
            self.set_plan_video(plan_name,date)
        elif cat=="PODCAST":
            self.set_plan_podcast(plan_name,date)

        self.plan_taken.change_date(self.plan_taken.Duration)
        return self.plan_taken

class Topup:
    def __init__(self,name="",price=0) -> None:
        self.name=name
        self.cost=price

    def set_topup(self,name,month=1):
        if name=="FOUR_DEVICE":
            self.cost=month*Plan_values.FOUR_DEVICE_PRICE
        elif name=="TEN_DEVICE":
            self.cost=month*Plan_values.TEN_DEVICE_PRICE
        
    def get_topup(self):
        return self.cost
                

class  Doremi():
    def __init__(self) -> None:

        self.total_price=0
        self.topup_exist=False
        self.topup_amount=0
        self.subscriptions={}
    
    def add_plan(self,name,plan):
        if name not in self.subscriptions:
            self.subscriptions[name]=plan
        else:
            self.setPrice(-plan.get_price())
            self.print_message("ADD_SUBSCRIPTION_FAILED DUPLICATE_CATEGORY")
            

    def get_plan(self,name):
        return self.subscriptions[name]
   

    def get_price(self):
        return self.total_price

    def setPrice(self,value):
        self.total_price+=value

    def add_Subscription(self,input):
        object=Category()
        if not self.date:
            self.print_message("ADD_SUBSCRIPTION_FAILED INVALID_DATE")
            return 
        plan=object.setPlan(input[1],input[2],self.date)
        self.setPrice(plan.get_price())
        self.add_plan(input[1],plan)
        

    def is_subscription_exists(self):
        if not self.subscriptions:
            return True 
        else:
            return False
        
    def print_message(self,msg):
        print(msg)
    def invalid_date(self,date):
        if not date:
            return True 
        else:
            return False

    def add_topup(self,input,date):
        objT=Topup()
        if self.invalid_date(date):
            self.print_message("ADD_TOPUP_FAILED INVALID_DATE")
            return 
        if not self.topup_exist:
                if self.is_subscription_exists():
                    self.print_message("ADD_TOPUP_FAILED SUBSCRIPTIONS_NOT_FOUND")
                    return 
                objT.set_topup(input[1],int(input[2]))
                self.setPrice(objT.get_topup())
                self.topup_exist=input 
                self.topup_amount=objT.get_topup()
        else:
                self.print_message("ADD_TOPUP_FAILED DUPLICATE_TOPUP")

    def print_renewal_details(self,input):
        if self.is_subscription_exists():
            self.print_message("SUBSCRIPTIONS_NOT_FOUND")
        else:
            for category in self.subscriptions:
                plan=self.get_plan(category)
                plan.set_reminder(category)
            self.print_message("RENEWAL_AMOUNT "+str(self.total_price))
    
    def User_input(self,fp):
        input_list = []
        
        
        while True:
            input=fp.readline()
            if not input:
                break
            input_list.append(input)
        for i in range(len(input_list)):
            if i!=len(input_list)-1 or len(input_list)==1:
                input_list[i]=input_list[i][:-1]
            take_input=input_list[i].split(" ")
            # print(input_list[i],take_input)
            if take_input[0]=="START_SUBSCRIPTION":
                obj=Date()
                self.date=obj.set_date(take_input[1])

            elif take_input[0]=="ADD_SUBSCRIPTION":
                self.add_Subscription(take_input)

            elif take_input[0]=="ADD_TOPUP":
                self.add_topup(take_input,self.date)
                
            elif take_input[0]=="PRINT_RENEWAL_DETAILS":
                self.print_renewal_details(take_input)

import sys
def main():
    fp=open(sys.argv[1])
    d=Doremi()
    d.User_input(fp)
    
if __name__ == "__main__":
    main()