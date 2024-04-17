import pymongo
import pandas as pd
import json

class MongoDBManagement:

    def __init__(self, username, password):
        """
        This function sets the required url
        """
        try:
            self.username = username
            self.password = password
            self.url = "mongodb+srv://{}:{}@testcluster.fjvlj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(
                self.username, self.password)
            # self.url = 'localhost:27017'
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initiation process\n" + str(e))

    def getMongoDBClientObject(self):
        """
        This function creates the client object for connection purpose
        """
        try:
            mongoClient = pymongo.MongoClient(self.url)
            return mongoClient
        except Exception as e:
            raise Exception("(getMongoDBClientObject): Something went wrong on creation of client object\n" + str(e))
    
    def closeMongoDBConnection(self, mongoClient):
        """
        This function closes the connection of client
        :return:
        """
        try:
            mongoClient.close()
        except Exception as e:
            raise Exception(f"Something went wrong on closing connection\n" + str(e))

    def isDatabasePresent(self, dbname):
        """
        This function checks if the database is present or not.
        :param dbname:
        :return:
        """
        try:
            mongoClient = self.getMongoDBClientObject()
            if dbname in mongoClient.list_database_names():
                mongoClient.close()
                return True
            else:
                mongoClient.close()
                return False
        except Exception as e:
            raise Exception("(isDatabasePresent): Failed on checking if the database is present or not \n" + str(e))
    
    def createDatabase(self, dbname):
        """
        This function creates database.
        :param dbname:
        :return:
        """
        try:
            databaseCheckStatus = self.isDatabasePresent(dbname=dbname)
            if not databaseCheckStatus:
                mongoClient = self.getMongoDBClientObject()
                database = mongoClient[dbname]
                mongoClient.close()
                return database
            else:
                mongoClient = self.getMongoDBClientObject()
                database = mongoClient[dbname]
                mongoClient.close()
                return database
        except Exception as e:
            raise Exception(f"(dropDatabase): Failed to delete database {dbname}\n" + str(e))
    
    def getDatabase(self, dbname):
        """
        This returns databases.
        """
        try:
            mongoClient = self.getMongoDBClientObject()
            mongoClient.close()
            return mongoClient[dbname]
        except Exception as e:
            raise Exception(f"(getDatabase): Failed to get the database list")
    
    def getCollection(self, collection_name, dbname):
        """
        This returns collection.
        :return:
        """
        try:
            database = self.getDatabase(dbname)
            return database[collection_name]
        except Exception as e:
            raise Exception(f"(getCollection): Failed to get the database list.")
    
    def isCollectionPresent(self, collection_name, dbname):
        """
        This checks if collection is present or not.
        :param collection_name:
        :param dbname:
        :return:
        """
        try:
            database_status = self.isDatabasePresent(dbname=dbname)
            if database_status:
                database = self.getDatabase(dbname=dbname)
                if collection_name in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise Exception(f"(isCollectionPresent): Failed to check collection\n" + str(e))
    
    def createCollection(self, collection_name, dbname):
        """
        This function creates the collection in the database given.
        :param collection_name:
        :param dbname:
        :return:
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, dbname=dbname)
            if not collection_check_status:
                database = self.getDatabase(dbname=dbname)
                collection = database[collection_name]
                return collection
        except Exception as e:
            raise Exception(f"(createCollection): Failed to create collection {collection_name}\n" + str(e))

    def dropCollection(self, collection_name, dbname):
        """
        This function drops the collection
        :param collection_name:
        :param dbname:
        :return:
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, dbname=dbname)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name, dbname=dbname)
                collection.drop()
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(dropCollection): Failed to drop collection {collection_name}")
    
    def insertRecord(self, dbname, collection_name, record):
        """
        This inserts a record.
        :param dbname:
        :param collection_name:
        :param record:
        :return:
        """
        try:
            # collection_check_status = self.isCollectionPresent(collection_name=collection_name,dbname=dbname)
            # print(collection_check_status)
            # if collection_check_status:
            collection = self.getCollection(collection_name=collection_name, dbname=dbname)
            collection.insert_one(record)
            sum = 0
            return f"rows inserted "
        except Exception as e:
            raise Exception(f"(insertRecord): Something went wrong on inserting record\n" + str(e))
    
    def insertRecords(self, dbname, collection_name, records):
        """
        This inserts a record.
        :param dbname:
        :param collection_name:
        :param record:
        :return:
        """
        try:
            # collection_check_status = self.isCollectionPresent(collection_name=collection_name,dbname=dbname)
            # print(collection_check_status)
            # if collection_check_status:
            collection = self.getCollection(collection_name=collection_name, dbname=dbname)
            record = list(records.values())
            collection.insert_many(record)
            sum = 0
            return f"rows inserted "
        except Exception as e:
            raise Exception(f"(insertRecords): Something went wrong on inserting record\n" + str(e))
    
    def findfirstRecord(self, dbname, collection_name,query=None):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, dbname=dbname)
            print(collection_check_status)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name, dbname=dbname)
                print(collection)
                firstRecord = collection.find_one(query)
                return firstRecord
        except Exception as e:
            raise Exception(f"(findRecord): Failed to find record for the given collection and database\n" + str(e))

    def findAllRecords(self, dbname, collection_name):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, dbname=dbname)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name, dbname=dbname)
                findAllRecords = collection.find()
                return findAllRecords
        except Exception as e:
            raise Exception(f"(findAllRecords): Failed to find record for the given collection and database\n" + str(e))
    
    def findRecordOnQuery(self, dbname, collection_name, query):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, dbname=dbname)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name, dbname=dbname)
                findRecords = collection.find(query)
                return findRecords
        except Exception as e:
            raise Exception(f"(findRecordOnQuery): Failed to find record for given query,collection or database\n" + str(e))
    
    def updateOneRecord(self, dbname, collection_name, query):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, dbname=dbname)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name, dbname=dbname)
                previous_records = self.findAllRecords(dbname=dbname, collection_name=collection_name)
                new_records = query
                updated_record = collection.update_one(previous_records, new_records)
                return updated_record
        except Exception as e:
            raise Exception(f"(updateRecord): Failed to update the records with given collection query or database name.\n" + str(e))
    
    def updateMultipleRecords(self, dbname, collection_name, query):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, dbname=dbname)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name, dbname=dbname)
                previous_records = self.findAllRecords(dbname=dbname, collection_name=collection_name)
                new_records = query
                updated_records = collection.update_many(previous_records, new_records)
                return updated_records
        except Exception as e:
            raise Exception(f"(updateMultipleRecord): Failed to update the records with given collection query or database name.\n" + str(e))
    
    def deleteRecord(self, dbname, collection_name, query):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, dbname=dbname)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name, dbname=dbname)
                collection.delete_one(query)
                return "1 row deleted"
        except Exception as e:
            raise Exception(f"(deleteRecord): Failed to update the records with given collection query or database name.\n" + str(e))
    
    def deleteRecords(self, dbname, collection_name, query):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, dbname=dbname)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name, dbname=dbname)
                collection.delete_many(query)
                return "Multiple rows deleted"
        except Exception as e:
            raise Exception(f"(deleteRecords): Failed to update the records with given collection query or database name.\n" + str(e))
    
    def getDataFrameOfCollection(self, dbname, collection_name):
        """
        """
        try:
            all_Records = self.findAllRecords(collection_name=collection_name, dbname=dbname)
            dataframe = pd.DataFrame(all_Records)
            return dataframe
        except Exception as e:
            raise Exception(f"(getDataFrameOfCollection): Failed to get DatFrame from provided collection and database.\n" + str(e))
    
    def saveDataFrameIntoCollection(self, collection_name, dbname, dataframe):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, dbname=dbname)
            dataframe_dict = json.loads(dataframe.T.to_json())
            if collection_check_status:
                self.insertRecords(collection_name=collection_name, dbname=dbname, records=dataframe_dict)
                return "Inserted"
            else:
                self.createDatabase(dbname=dbname)
                self.createCollection(collection_name=collection_name, dbname=dbname)
                self.insertRecords(dbname=dbname, collection_name=collection_name, records=dataframe_dict)
                return "Inserted"
        except Exception as e:
            raise Exception(f"(saveDataFrameIntoCollection): Failed to save dataframe value into collection.\n" + str(e))

    def getResultToDisplayOnBrowser(self, dbname, collection_name):
        """
        This function returns the final result to display on browser.
        """
        try:
            response = self.findAllRecords(dbname=dbname, collection_name=collection_name)
            result = [i for i in response]
            return result
        except Exception as e:
            raise Exception(f"(getResultToDisplayOnBrowser) - Something went wrong on getting result from database.\n" + str(e))