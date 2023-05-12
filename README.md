# SQLTABLEMUSICMATE

Using SQLAlchemy we can make this table that we integrate with the api. Basically we can know the user activity now for example if the user idle. And we can connect it to the session. Or just make another firebase collection to store the data

The table will be created if new user just login with new id.

#Function login that have create table

@app.post("/login") async def login(request: Request, username: str = Body(...), password: str = Body(...), email: str = Body(...)): try: 

    # Generate session ID
    session_id = str(uuid.uuid4())

    # Store session data in Firestore
    doc_ref = db.collection("sessions").document(session_id)
    doc_ref.set({"username": username, "email": email})

    # Check if user_activity table exists, create it if it doesn't
    try:
        get_db().query(UserActivity).first()
    except:
        create_tables()

    # Add user activity record
    user_activity = UserActivity(user_id=username, activity_type="login")
    db_session = get_db()
    db_session.add(user_activity)
    db_session.commit()

    # Set session ID in response header
    response = JSONResponse({"message": "Login successful."})
    response.set_cookie(key="session_id", value=session_id)
    return response
except Exception as e:
    return {"error": str(e)}


so as you can see in this function we push first to database for username and email that is login to the session. After that we create the table if not created yet

We also give post create table that is also stored in mysql database on local user's storage. 

With that information we will use it to push it to our firebase.

Note: The table is the same when user login

      But this table is updated so we can really update what user doing FE.: Idle,Posting,Reading,Scrolling, and also Searching
      
      Why this important? To kick user if they already been idle/in the session for too long. Other use: just cool can see what user do now.
      
![image](https://github.com/Andrean2305/SQLTABLEMUSICMATE/assets/91464375/b3ad1dd0-f325-452b-8ea3-546bb5f29f24)

