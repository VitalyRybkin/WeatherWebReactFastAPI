def to_json(table):
    """
    Function. Convert table to json
    """
    return {col.name: getattr(table, col.name) for col in table.__table__.columns}
