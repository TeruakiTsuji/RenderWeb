def userID_session(session, session_name):
    if 'userID' in session:
        userID = session['userID']
    else:
        user = session.get(session_name)
        if user is not None:
            userID = user['userID']
        else:
            userID = None
    return userID
