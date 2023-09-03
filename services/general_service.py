def add_to_db(session, obj):
    session.add(obj)
    session.commit()
    session.refresh(obj)
