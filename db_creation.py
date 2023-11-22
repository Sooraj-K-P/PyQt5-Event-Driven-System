import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="trackeradmin",
  password="trackpass",
  database="trackerrose"
)

print(mydb)

mycursor = mydb.cursor()

mycursor.execute("DROP TABLE IF EXISTS TrackerDetails")
mycursor.execute("DROP TABLE IF EXISTS TrackerSummary")
mycursor.execute("DROP TABLE IF EXISTS UserDetails")

sql = "CREATE TABLE UserDetails (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
      "username TEXT, " \
      "password VARCHAR(255)," \
      "phone BIGINT, " \
      "email VARCHAR(255))" 

mycursor.execute(sql)

sql = "CREATE TABLE TrackerSummary ("\
    "tracker_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"\
    "date DATE ,"\
    "start_time timestamp NULL DEFAULT NULL,"\
    "end_time timestamp NULL DEFAULT NULL,"\
    "total_alphanumeric_keys INT DEFAULT NULL,"\
    "total_special_keys INT DEFAULT NULL,"\
    "user_id INT NOT NULL,"\
    "FOREIGN KEY (user_id) REFERENCES UserDetails(id))"

mycursor.execute(sql)

sql = "CREATE TABLE TrackerDetails ("\
      "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"\
      "Keys_pressed TEXT, "\
      "summary_id INT NOT NULL,"\
      "FOREIGN KEY (summary_id) REFERENCES TrackerSummary(tracker_id) ON DELETE CASCADE)"

mycursor.execute(sql)

mycursor.execute("SELECT * FROM UserDetails")
myresult = mycursor.fetchall()
print(myresult)

mycursor.execute("SELECT * FROM TrackerSummary")
myresult = mycursor.fetchall()
print(myresult)

mycursor.execute("SELECT * FROM TrackerDetails")
myresult = mycursor.fetchall()
print(myresult)

