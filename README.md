# SQLTABLEMUSICMATE

Using SQLAlchemy we can make this table that we integrate with the api. Basically we can know the user activity now for example if the user idle. And we can connect it to the session. Or just make another firebase collection to store the data

The table will be created if new user just login with new id.

@app.post("/login")
async def login(request: Request, username: str = Body(...), password: str = Body(...), email: str = Body(...)):
    try:
        # Authenticate user
        # ...

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
