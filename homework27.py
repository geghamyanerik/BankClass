# 1․ Գրել BankUser class, որը․
#    - __init__() -ում կընդունի մարդու անունը, ազգանունը, տարիքը, էլեկտրոնային փոստը, քարտը, գումարը քարտի վրա, pin կոդը,
#    - մինչ ինիցիալիզացնելը, կստուգի, որ ընդունված արգումենտները ճիշտ են մուտքագրված՝
#      -- անունը և ազգանունը - տառերից բաղկացած,
#      -- տարիքը - բնական թիվ,
#      -- էլեկտրոնային փոստ - տեքստ (գրեք նվազագույն պայմաններ էլեկտրոնային փոստի ճշտությունը ստուգելու համար),
#      -- քարտի համարը - 16 թվանշանից բաղկացած (xxxx xxxx xxxx xxxx կամ xxxxxxxxxxxxxxxx ֆորմատով),
#                        քարտի համարի ճշտությունը ստուգեք Լունայի ալգորիտմի միջոցով 
#                      (https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%9B%D1%83%D0%BD%D0%B0)
#      -- գումարը - դրական թիվ,
#      -- pin կոդը - 4 թվանշանից բաղկացած տեքստ,
#    - անունը, ազգանունը, տարիքը և էլեկտրոնային փոստը կլինեն այնպիսի ատրիբուտներ, որոնց ուղիղ հասանելիությունը կլինի պաշտպանված,
#    - քարտի համարը, գումարը և pin կոդը կլինեն այնպիսի ատրիբուտներ, որոնց ուղիղ հասանելիությունը կլինի արգելված,
#    - կունենա մեթոդ, որը կվերադարձնի մարդու անունը և ազգանունը,
#    - կունենա մեթոդ, որը կվերադարձնի քարտի համարը և գումարը, բայց միայն ճիշտ pin կոդը հավաքելուց հետո,
#    - կունենա մեթոդ, որը կավելացնի գումար հաշվին, բայց միայն ճիշտ pin կոդը հավաքելուց հետո,
#    - կունենա մեթոդ, որը կհանի գումար հաշվից, բայց միայն ճիշտ pin կոդը հավաքելուց հետո,
#      հաշվի առեք, որ գումարը բացասական չի կարող լինել,
#    - 3 անգամ սխալ pin կոդը հավաքելուց հետո տվյալ user-ի համար հասանելիությունը class-ի ամբողջ ֆունկցիոնալությանը կլինի արգելված,
#    - կունենա մեթոդ, որի միջոցով կվերականգնվի հասանելիությունը 6-անիշ թիվ մուտքագրելու դեպքում, որը կուղարկվի էլ․ փոստին (կարող եք օգտագործել smtplib գրադարանը պատահական 6-անիշ թիվ գեներացնելու և էլ․ փոստին ուղարկելու համար)։

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

class BankUser():
    @staticmethod
    def _validate_name(name,lastName):
        return name.isalpha() and lastName.isalpha()
    @staticmethod
    def _isDigit(n):
        return isinstance(n, int) and n >0
    @staticmethod
    def _valid_email(email):
        return "@" in email
    @staticmethod
    def _isvalid_card(card_number):
        card_number = str(card_number)
        card_number = card_number.replace(" ", "")
    
        if not card_number.isdigit():
            return False

        total = 0
        reverse_digits = card_number[::-1]
        for i,value in enumerate(reverse_digits):
            n = int(value)
            if i %2 ==1:
               
                n*=2
                if n >9:
                    n-=9
            total += n
        return len(card_number) == 16 and total % 10 == 0
    @staticmethod
    def _valid_money(money):
        return money>=0
    @staticmethod
    def _valis_pin(pin):
        if not   isinstance(pin, int):
            return False
        return len(str(pin)) ==4


    def __init__(self,name,last_name,age,email,card,money,pin):
        if BankUser._validate_name(name,last_name):
            self._name = name
            self._last_name = last_name
        else:
            raise ValueError("Eror")
        if BankUser._isDigit(age):
            self._age = age
        else:
            raise ValueError("false")
        if BankUser._valid_email(email):
            self._email = email
        else:
            raise ValueError("Wrong Email")
        if BankUser._isvalid_card(card):
            self.__card = card
        else:
            raise ValueError("Wrong Card")
        if BankUser._valid_money(money):
            self.__money = money
        else:
            raise ValueError("Wrong Money")
        if BankUser._valis_pin(pin):
            self.__pin = pin
        else:
            raise ValueError("Wrong Pin")
        self.__block = False
        self.__tries = 0
    def __check_access(self):
            if self.__block:
                print("Հասանելիությունը արգելափակված է:")
                return False
            return True
    def return_name(self):
        if self.__check_access():
            return f"{self._name} - {self._last_name} "
    
    
    
    def is_valid_pin(self,pin):
        if not self.__check_access():
            return False
        if pin == self.__pin:
            self.__tries = 0
            return True
        else:
            self.__tries +=1
            print(f"Սխալ PIN: Մնաց փորձերի քանակը՝ {3 - self.__tries}")
            if self.__tries >=3:
                self.__block = True
                print("Քարտը արգելափակվեց:")
            return False
            
         

    def return_card_money(self,pin):
        if self.is_valid_pin(pin):
             return f"{self.__card, self.__money}"
    def add_money(self,pin,money):
        if self.is_valid_pin(pin):
            self.__money += money
    def withdraw_money(self,pin,money):
        if self.is_valid_pin(pin):
            if self.__money < money:
                print("Anbavarar mijocner")
            else:
                self.__money  -= money
                print(f"hashivy kazmum e {self.__money} hanvec -{money}")
    def send_recovery_email(self):
   
        self.__recovery_code = random.randint(100000, 999999)
    
    
        sender_email = "er089542@gmail.com"
        app_password = "" 
        receiver_email = self._email

 
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Bank Account Recovery Code"
    
        body = f"Բարև ձեզ, Ձեր վերականգնման կոդն է՝ {self.__recovery_code}"
        message.attach(MIMEText(body, "plain"))

        try:
        
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  
                server.login(sender_email, app_password)
                server.send_message(message)
                print(f" Վերականգնման կոդն ուղարկվեց {self._email} հասցեին:")
        except Exception as e:
            print(f" Սխալ՝ նամակը չուղարկվեց: {e}")
    def recover_access(self, code):
        
        if str(code) == str(self.__recovery_code):
            self.__block = False
            self.__tries = 0
            self.__recovery_code = None
            print(" Հասանելիությունը վերականգնվեց (Доступ восстановлен):")
            return True
        print(" Սխալ կոդ ")
        return False
user = BankUser("Ero", "Geghamyan", 19, "erik.geghamyan@mail.ru", 4083060040281582, 100, 1234)

while True:
    print("\n--- Մենյու ---")
    print("1. Տեսնել անունը\n2. Տեսնել քարտի տվյալները\n3. Վերականգնել մուտքը (եթե բլոկ է) \n4. ավելացնել գումար \n5.հանել գումար\n6 Ելք")
    choice = input("Ընտրեք գործողությունը: ")

    if choice == "1":
        print(user.return_name())
    
    elif choice == "2":
        
            p = int(input("Մուտքագրեք PIN: "))
            res = user.return_card_money(p)
            if res: print(res)
        
            
            
    elif choice == "3":
        user.send_recovery_email()
        rec_code = input("Մուտքագրեք էլ. փոստին եկած 6-անիշ կոդը: ")
        user.recover_access(rec_code)
    elif choice =="4":
        money = int(input("mutqagreq gumaryi chapy "))
        pin = int(input("Մուտքագրեք PIN: "))
        user.add_money(pin,money)
    elif choice =="5":
        money = int(input("mutqagreq gumaryi chapy "))
        pin = int(input("Մուտքագրեք PIN: "))
        user.withdraw_money(pin,money)
    elif choice == "6":
        break