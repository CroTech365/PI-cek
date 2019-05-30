from decimal import *
import time
from colorama import Fore, Back, Style
import sys
import os
from console_progressbar import ProgressBar
import datetime
import string
import smtplib
import random

#lista s opcijama
vrste = ['BBP-formula','Bellardova formula','Benchmark']

def intro():
    
    os.system('cls||clear')
    logo = '''
    *           /$$                        /$$      
    *          |__/                       | $$      
    *  /$$$$$$  /$$|    /$$$$$$$  /$$$$$$ | $$   /$$
    * /$$__  $$| $$|   /$$_____/ /$$__  $$| $$  /$$/
    *| $$  \ $$| $$|  | $$      | $$$$$$$$| $$$$$$/ 
    *| $$  | $$| $$|  | $$      | $$_____/| $$_  $$ 
    *| $$$$$$$/| $$|  |  $$$$$$$|  $$$$$$$| $$ \  $$
    *| $$____/ |__/    \_______/ \_______/|__/  \__/
    *| $$                                        
    *| $$                                        
    *|__/                                        
    '''
    #bojanje loga
    for i in range(len(logo)):
        if(logo[i]=='*'):
            print('',end='')
        elif(logo[i]=='$'):
            print(Fore.RED + Style.BRIGHT + logo[i],end='')
        else:
            print(Fore.YELLOW + Style.BRIGHT + logo[i],end='')
    print('')

    
    #isipis opcija
    for i in range(len(vrste)):
        print(Fore.RED + Style.BRIGHT +str(i+1)+') '+ Style.RESET_ALL+vrste[i] )


intro()

#od korisnika traži opciju
o = int(input(Fore.YELLOW + Style.BRIGHT +"\nOdabir: "+ Style.RESET_ALL))

#od korisnika traži broj znamenki koji će kasnije generirati
d = int(input(Fore.YELLOW + Style.BRIGHT +"Upisi broj znamenki: "+ Style.RESET_ALL))
#zbog zaokruživanja računa jednu znamenku više
d += 1
#koristeći "decimal" library 
#postavljane broja decimala
getcontext().prec = d


def Bellardova_formula(d):
    #sprema trnutno vrijeme u variablu start
    start = time.time()
    pi = 0
    #postavljanje postavki za ProgressBar
    pb = ProgressBar(total=100,prefix='Početak', suffix='Kraj', decimals=5, length=50, fill='X', zfill='-')
    #računanje pi-a (https://en.wikipedia.org/wiki/Bellard%27s_formula) - formula
    for n in range(d):
        pi = Decimal(pi) + (Decimal((-1)**n)/Decimal(2**(10*n))) * (-(Decimal(2**5)/Decimal((4*n)+1))-(Decimal(1)/Decimal((4*n)+3)) + (Decimal(2**8)/Decimal((10*n)+1)) - (Decimal(2**6)/Decimal((10*n)+3)) - (Decimal(2**2)/Decimal((10*n)+5)) - (Decimal(2**2)/Decimal((10*n)+7)) + (Decimal(1)/Decimal((10*n)+9)))
        #ažuruira ProgressBar
        pb.print_progress_bar((float(n+1)/d)*100)
    #dio računanja pi-a
    pi = Decimal(pi) * Decimal(Decimal(1)/Decimal(2**6))
    #sprema trunutno vrijeme u variablu end
    end = time.time()
    #pretvara pi u string kako bi kasnije mogao pretvoriti u listu
    pi = str(pi)
    #verzija pi-a u stringu
    pi3 = str(pi)
    #pretvara pi u listu radi lakše manipulacije
    pi = list(pi)
    #dobivene podatke sprema u listu
    izlaz = [pi,end-start,pi3]
    return izlaz

def BBP_formula(d):
    #sprema trnutno vrijeme u variablu start
    start = time.time()
    pi = 0
    #postavljanje postavki za ProgressBar
    pb = ProgressBar(total=100,prefix='Početak', suffix='Kraj', decimals=5, length=50, fill='X', zfill='-')
    for k in range(d): #formula (https://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula)
        pi = Decimal(pi) + Decimal((Decimal(1)/Decimal(16**k))*((Decimal(4)/Decimal((8*k)+1)) - (Decimal(2)/Decimal((8*k)+4)) - (Decimal(1)/Decimal((8*k)+5)) - (Decimal(1)/Decimal((8*k)+6)) ))
        pb.print_progress_bar((float(k+1)/d)*100)
    #sprema trnutno vrijeme u variablu start
    end = time.time()
    #isto kao u prošloj funkciji
    pi = str(pi)
    pi3 = str(pi)
    pi = list(pi)
    izlaz = [pi,end-start,pi3]
    return izlaz

def provjera(pi):
    #otvara datoteku pi.txt u modu za čitanje('r')
    f = open('pi.txt','r')
    #sadržaj datoteke pi.txt sprema u variblu cons
    cons = str(f.read())
    t,n = 0,0
    #d-1 jer zbog preciznosti računali smo znamenku viška
    for i in range(d-1):
        #ako je generirana znamenka jednaka znamenki iz potvrđene datoteke
        if(cons[i]==pi[i]):
            continue
        else:
            #netočan = netočan + 1
            n+=1
    return n

#ako je odabrana opcija 1
if(o==1):
    #iz funkcije BBP_formula() dobivamo podatke i spemalo u listu izlaz
    izlaz = BBP_formula(d)
    pi = izlaz[0]
    prolaz = izlaz[1]
    pi3 = izlaz[2]
    n = provjera(pi)
    print('')
    try:
        #pokušat će otvorti dokument, a ako ne postoji stvoriti ga
        dokument = open(str(datetime.datetime.now().strftime('%d.%m.%y-%H:%M:%S'))+'.txt','w+')
        #u dokument zapisati pi
        dokument.write(pi3)
        print(Fore.YELLOW+ Style.BRIGHT+"Datoteka je uspješno kreirana")
        print("Naziv datoteke je " +Fore.RED+ Style.BRIGHT+ str(datetime.datetime.now().strftime('%d.%m.%y-%H:%M:%S'))+'.txt')
    except:
        print("Nešto je pošlo po zlu sorry :(")
    #ako u funkciji provjera() pronađena greška u generiranim znamenkama n!=0
    if(n!=0):
        #ispisivanje pi-a ali tako da se vidi gdje je došlo do pogreške
        #tj decimala koja je pogrešna bit će obojana crveno
        f = open('pi.txt','r')
        cons = str(f.read())
        n = 0
        for i in range(d-1):
            if(cons[i]==pi[i]):
                print(Fore.GREEN + Style.BRIGHT + pi[i],end='')
            else:
                print(Fore.RED + Style.BRIGHT + pi[i],end='')
                n+=1
    print('')
    #isipis vrlo važnih informacija
    print(Style.RESET_ALL+'')
    print(Fore.YELLOW +'od',Style.BRIGHT + str(d-1)+ Style.RESET_ALL,Fore.YELLOW +'znamenki',Fore.GREEN + Style.BRIGHT + str(d-1-n)+ Style.RESET_ALL,Fore.YELLOW +'ih je točno, a',Fore.RED + Style.BRIGHT + str(n)+ Style.RESET_ALL,Fore.YELLOW +'netočno')
    print("Završeno u"+ Fore.YELLOW+ Style.BRIGHT ,prolaz,'s' )

#ako je odabrana opcija 2
elif(o==2):
    #gotovo isto kao kod prošlog if-a
    izlaz = Bellardova_formula(d)
    pi = izlaz[0]
    prolaz = izlaz[1]
    pi3 = izlaz[2]
    n = provjera(pi)
    print('')
    print(Fore.YELLOW+ Style.BRIGHT+"Datoteka je uspješno kreirana")
    print("Naziv datoteke je " +Fore.RED+ Style.BRIGHT+ str(datetime.datetime.now().strftime('%d.%m.%y-%H:%M:%S'))+'.txt')
    dokument = open(str(datetime.datetime.now().strftime('%d.%m.%y-%H:%M:%S'))+'.txt','w+')
    dokument.write(pi3)
    if(n!=0):
        f = open('pi.txt','r')
        cons = str(f.read())
        n = 0
        for i in range(d-1):
            if(cons[i]==pi[i]):
                print(Fore.GREEN + Style.BRIGHT + pi[i],end='')
            else:
                print(Fore.RED + Style.BRIGHT + pi[i],end='')
                n+=1
    print('')

    print(Style.RESET_ALL+'')
    print(Fore.YELLOW +'od',Style.BRIGHT + str(d-1)+ Style.RESET_ALL,Fore.YELLOW +'znamenki',Fore.GREEN + Style.BRIGHT + str(d-1-n)+ Style.RESET_ALL,Fore.YELLOW +'ih je točno, a',Fore.RED + Style.BRIGHT + str(n)+ Style.RESET_ALL,Fore.YELLOW +'netočno')
    print("Završeno u"+ Fore.YELLOW+ Style.BRIGHT ,prolaz,'s' )

#odabrana je opcija 3
elif(o==3):
    os.system('cls||clear')
    
    logo2 = '''  
     /$$$$$$$                                /$$                                         /$$      
    | $$__  $$                              | $$                                        | $$    
    | $$  \ $$  /$$$$$$  /$$$$$$$   /$$$$$$$| $$$$$$$  /$$$$$$/$$$$   /$$$$$$   /$$$$$$ | $$   /$$|
    | $$$$$$$  /$$__  $$| $$__  $$ /$$_____/| $$__  $$| $$_  $$_  $$ |____  $$ /$$__  $$| $$  /$$/
    | $$__  $$| $$$$$$$$| $$  \ $$| $$      | $$  \ $$| $$ \ $$ \ $$  /$$$$$$$| $$  \__/| $$$$$$/ 
    | $$  \ $$| $$_____/| $$  | $$| $$      | $$  | $$| $$ | $$ | $$ /$$__  $$| $$      | $$_  $$ 
    | $$$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$$| $$  | $$| $$ | $$ | $$|  $$$$$$$| $$      | $$ \  $$
    |_______/  \_______/|__/  |__/ \_______/|__/  |__/|__/ |__/ |__/ \_______/|__/      |__/  \__/'''
    #printanje loga u boji
    for i in range(len(logo2)):
        if(logo2[i]=='*'):
            print('',end='')
        elif(logo2[i]=='$'):
            print(Fore.YELLOW + Style.BRIGHT + logo2[i],end='')
        else:
            print(Fore.BLACK + Style.BRIGHT + logo2[i],end='')
    print('\n\n\n')

    print(Fore.GREEN + Style.BRIGHT + "Benchmark je počeo na " + Fore.YELLOW + Style.BRIGHT + str(d-1) + Fore.GREEN + Style.BRIGHT+ ' decimale')
    print('\n')
    

    def Benchmark(naziv,izlaz): 
        #ako nema grešaka pri generiranju pi-a
        if(provjera(izlaz[0])==0):
            #ispisuje se trajanje generiranja i jesu li sve znamenke točne (kvačica na kraju(\u2713))
            print(Fore.YELLOW + Style.BRIGHT +'- '+naziv,Fore.GREEN + Style.BRIGHT + str(izlaz[1]) + 's '+'\u2713')
        else:
            #ako nisu točne ispiši križić (\u2717)
            print(Fore.YELLOW + Style.BRIGHT +'- '+naziv,Fore.GREEN + Style.BRIGHT + str(izlaz[1]) + 's '+ Fore.RED + Style.BRIGHT +'\u2717')
    
    #naziv formule pomoću koje se generira
    print(Fore.YELLOW + Style.BRIGHT +'- '+vrste[0],Fore.RED + Style.BRIGHT)
    Benchmark(vrste[0],BBP_formula(d))
    print('\n')
    print(Fore.YELLOW + Style.BRIGHT +'- '+vrste[1],Fore.RED + Style.BRIGHT)
    Benchmark(vrste[1],Bellardova_formula(d))
    

else:
    print(Fore.YELLOW + Style.BRIGHT +"\u26A0  "+Fore.RED + Style.BRIGHT + "Opcija koju ste unjeli ne postoji")






























# pi = Decimal(3)
# bc = 1
# a = 2
# b = 3
# c = 4
# for i in range(1,d**2):
#     if(bc%2!=0):
#         pi = Decimal(pi) + Decimal(4)/Decimal((a)*(b)*(c))
#         print(a,b,c)
#         a = c
#         b = a + 1
#         c = b + 1
#     else:
#         pi = Decimal(pi) - Decimal(4)/Decimal((a)*(b)*(c))
#         a = c
#         b = a + 1
#         c = b + 1
#         print(a,b,c)

# print(pi)






















# def fact(n):
#     f = 1
#     for i in range(1,n-1):
#         f = f * i
#     return f
# pi = 0
# for n in range(d**2):
#     #pb.print_progress_bar(((n+1)/float(d))*100)
#     pi = Decimal(pi) + Decimal(Decimal((-1)**n)/Decimal(2**(10*n))) * Decimal(-1 * Decimal(2**5/(4*n+1))-Decimal(1/(4*n+3))+Decimal(2**8/(10*n+1))-Decimal(2**6/((10*n)+3))-Decimal(2**2/((10*n)+5))-Decimal(2**2/((10*n)+7))+Decimal(1/((10*n)+9)))
#     #print(Decimal(pi) * (Decimal(1)/Decimal(2**6)))
# pi = Decimal(pi) * (Decimal(1)/Decimal(2**6))

# print(pi)

