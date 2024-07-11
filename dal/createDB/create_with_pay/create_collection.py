def create_or_get_collection(db, collection_name):
    """
    Create a collection if it does not exist.

    :param db: The database instance where the collection will be created
    :param collection_name: Name of the collection to create_with_pay
    :return: The created collection instance
    """
    if collection_name not in db.list_collection_names():
        collection = db.create_collection(collection_name)
    else:
        collection = db[collection_name]
    return collection
