"""
quotes-capture database

This program will allow you to manage quotes in a firestore Cloud
database.

"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore  
from firebase_admin import db
import os

cred = credentials.Certificate("C:/Users/ccono/OneDrive/Craig Conover/BYUI/CSE310 - Applied Programming/Sprint 1/quotes-capture-firebase-adminsdk-niz56-0f0aee5d1a.json")

# firebase_admin.initialize_app(cred)
firebase_admin.initialize_app(cred, {
        'projectId': 'quotes-capture',
    })

# db = firestore.client('quotes-capture')
db = firestore.client()


def add_new_s_quote(db):
    '''
    Prompt the user for a new quote to add to the quotes database.  The
    quote title must be unique (firestore document id).   
    '''

    title = input("Quote Title: ")
    quote = input("Quote: ")
    type = "Spiritual"
    author = input("Author: ")
    status = "New"

    # Check for an already existing quote with the same title.
    # The document ID must be unique in Firestore.
    result = db.collection("quotes").document(title).get()
    if result.exists:
        print("Quote already exists.")
        return

    # Build a dictionary to hold the contents of the firestore document.
    data = {"title" : title, 
            "quote" : quote,
            "type" : type,
            "author" : author,
            "status" : status
           }
    db.collection("quotes").document(title).set(data) 

    # Save this in the log collection in Firestore       
    log_transaction(db, f"Added {title} -- {quote}")


def add_new_m_quote(db):
    '''
    Prompt the user for a new quote to add to the quotes database.  The
    quote title must be unique (firestore document id).  
    '''

    title = input("Quote Title: ")
    quote = input("Quote: ")
    type = "Motivation"
    author = input("Author: ")
    status = "New"

    # Check for an already existing quote with the same title.
    # The document ID must be unique in Firestore.
    result = db.collection("quotes").document(title).get()
    if result.exists:
        print("Quote already exists.")
        return

    # Build a dictionary to hold the contents of the firestore document.
    data = {"title" : title, 
            "quote" : quote,
            "type" : type,
            "author" : author,
            "status" : status
           }
    db.collection("quotes").document(title).set(data) 

    # Save this in the log collection in Firestore       
    log_transaction(db, f"Added {title} -- {quote}")

def change_status(db):
    '''
    Prompt the user to change the status of an already existing quote in the
    quotes database.  
    '''

    title = input("Quote Title: ")
    # add_status = input("Status (New, Used): ")

    # Check for an already existing quote with the same title.
    # The document ID must be unique in Firestore.
    result = db.collection("quotes").document(title).get()
    if not result.exists:
        print("Invalid Quote Title")
        return

    add_status = input("Status (New, Used): ")
    # Convert data read from the firestore document to a dictionary
    data = result.to_dict()

    # Update the dictionary with the new quanity and then save the 
    # updated dictionary to Firestore.
    data["status"] = add_status
    db.collection("quotes").document(title).set(data)

    # Save this in the log collection in Firestore
    log_transaction(db, f"Changed Status to {add_status} for {title}")


def search_quotes(db):
    '''
    Search the database in multiple ways.
    '''

    print("Select Query")
    print("1) Show All Quotes")        
    print("2) Show Only Spiritual Quotes")
    print("3) Show Only Motivation Quotes")
    choice = input("> ")
    print()

    # Build and execute the query based on the request made
    if choice == "1":
        results = db.collection("quotes").get()
    elif choice == "2":
        results = db.collection("quotes").where("type","==","Spiritual").get()
    elif choice == "3":
        results = db.collection("quotes").where("type","==","Motivation").get()
    else:
        print("Invalid Selection")
        return
    
    # Display all the results from any of the queries
    print("")
    print("Search Results")
    print(f"{'Title':<20}  {'Quote':<10}  {'Type':<10}  {'Author':<10}  {'Status':<10}")
    for result in results:
        item = result.to_dict()
        print(f"{result.id:<20}  {item['quote']:<10}  {item['type']:<10}  {item['author']:<10}  {item['status']:<10}")
    print()     


def delete_quote(db):
    '''
    Prompt the user to delete existing quote in the
    quotes database.  
    '''

    title = input("Quote Title: ")

    # Check for an already existing quote with the same title.
    # The document ID must be unique in Firestore.
    result = db.collection("quotes").document(title).get()
    if not result.exists:
        print("Invalid Quote Title")
        return

    # Delete quote from Firestore.
    db.collection("quotes").document(title).delete()

    # Save this in the log collection in Firestore
    log_transaction(db, f"Deleted {title}")
  

def log_transaction(db, message):
    '''
    Save a message with current timestamp to the log collection in the
    Firestore database.
    '''
    data = {"message" : message, "timestamp" : firestore.SERVER_TIMESTAMP}
    db.collection("log").add(data)   


def main():
    # db = initialize_firestore()
    choice = None
    while choice != "0":
        print()
        print("0) Exit")
        print("1) Add New Spiritual Quote")
        print("2) Add New Motivational Quote")
        print("3) Change Status")
        print("4) Search Quotes")
        print("5) Delete Quote")
        choice = input(f"> ")
        print()
        if choice == "1":
            add_new_s_quote(db)
        elif choice == "2":
            add_new_m_quote(db)
        elif choice == "3":
            change_status(db)
        elif choice == "4":
            search_quotes(db)        
        elif choice == "5":
            delete_quote(db)  

if __name__ == "__main__":
    main()
