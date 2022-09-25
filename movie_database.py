
# ----------------------------------------------- initializing sql connection ---------------------------------------------
import mysql.connector
import sys
from secrets import password

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=password
)
cur = mydb.cursor(dictionary=True)

# ----------------------------------------------- creating a new database -----------------------------------------------------
exist=0
cur.execute("show databases");
res=cur.fetchall()
for x in res:
    if(x['Database']=='mulesoft'):
        print("Database Exists")
        exist=1
        break
if(exist==0):
    cur.execute("create database mulesoft");
cur.execute("use mulesoft")
cur.execute("show tables")
exist=0
res=cur.fetchall()

# lead actor, actress, year of release and the director name
# --------------------------------------------- creating table movies -----------------------------------------------------
cur.execute("show tables")
exist=0
res=cur.fetchall()
for x in res:
    if(x['Tables_in_mulesoft']=='movies'):
        print("Table Exists")
        exist=1
        break
if(exist==0):
    cur.execute("CREATE TABLE movies (id INT AUTO_INCREMENT PRIMARY KEY,movie VARCHAR(50), actor VARCHAR(30), actress VARCHAR(30),release_year Int,director VARCHAR(30))");
    print("created table")

# -------------------------------------------- adding some data to table movies-----------------------------------------------
val = [
    ('The Dark Knight', 'Christian Bale','Maggie Gyllenhaal',2008,'Christopher Nolan'),
    ('Avengers: Infinity War', 'Robert Downey Jr','Scarlett Johansson',2018,'Anthony Russo'),
    ('Spider-Man: Into the Spider-Verse', 'Shameik Moore','Hailee Steinfeld',2018,'Bob Persichetti'),
    ('Top Gun: Maverick ','Tom Cruise','Jennifer Connelly',2022,'Joseph Kosinski'),
    ('Logan', 'Hugh Jackman','Dafne Keen',2017,'James Mangold'),
]
for x in val:
    cur.execute("INSERT INTO movies (movie,actor, actress,release_year,director) VALUES {}".format(x))

mydb.commit()

choice=1
try:
    choice=int(input("Enter \n0:to exit\n1:To add new movie\n2:To get all the data\n3:To query\n"))
    while(choice!=0):
        if(choice==0): #exiting program
            sys.exit(0)

        elif(choice==1): #adding new movie
            movie=input("Enter name of the movie: ")
            actor=input("Enter name of actor: ")
            actress=input("Enter name of actress: ")
            year=input("Enter year of release: ")
            director=input("Enter name of director: ")
            movie="NULL" if(movie=="") else movie
            actor="NULL" if(actor=="") else actor
            actress="NULL" if(actress=="") else actress
            year="NULL" if(year=="") else int(year)
            director="NULL" if(director=="") else director
            cur.execute("INSERT INTO movies (movie,actor, actress,release_year,director) VALUES ('{}','{}','{}',{},'{}')".format(movie,actor,actress,year,director))
            mydb.commit()
            
            
        elif(choice==2):
            print("movie\t\t\tactor\t\t\tactress\t\t\tyear\t\t\tdirector")
            cur.execute("select * from movies")
            for x in cur.fetchall():
                print("{} \t {} \t {} \t {} \t {}".format(x['movie'],x['actor'],x['actress'],x['release_year'],x['director']))
            
        elif(choice==3): # query
            movie=input("Enter name of the movie or LEAVE BLANK: ")
            actor=input("Enter name of actoror LEAVE BLANK: ")
            actress=input("Enter name of actressor LEAVE BLANK: ")
            year=input("Enter year of releaseor LEAVE BLANK: ")
            director=input("Enter name of directoror LEAVE BLANK: ")
            if(movie!=""):
                cur.execute("select * from movies where actor ='{}';".format(movie))
            elif(actor!=""):
                cur.execute("select * from movies where actor ='{}';".format(actor))
            elif(actress!=""):
                cur.execute("select * from movies where actress ='{}';".format(actress))
            elif(year!=""):
                year=int(year)
                cur.execute("select * from movies where release_year ={};".format(year))
                print('ok')
            elif(director!=""):
                cur.execute("select * from movies where director ='{}';".format(director))
            print("movie\t\t\tactor\t\t\tactress\t\t\tyear\t\t\tdirector")
            for x in cur.fetchall():
                print("{} \t {} \t {} \t {} \t {}".format(x['movie'],x['actor'],x['actress'],x['release_year'],x['director']))
        choice=int(input("\nEnter \n0:to exit\n1:To add new movie\n2:To query\n"))
                
except:
    print("Error occured")
