import sqlite3

def creating_reviews(review):
      conn = sqlite3.connect('reviews.db')
      print ("Opened database successfully")

      conn.execute("INSERT INTO sentic_reviews (review) VALUES (?)", (review,))
      conn.commit()
      print ("Records created successfully")
      conn.close()