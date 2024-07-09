def create_database(mongo_client, database_name):
    """
    Create a database if it does not exist.

    :param mongo_client: MongoClient instance connected to MongoDB Atlas
    :param database_name: Name of the database to create_with_pay
    :return: The created database instance
    """
    db = mongo_client[database_name]
    return db
