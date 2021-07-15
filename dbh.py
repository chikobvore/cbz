
#this script handles the database connections
import pymongo

# client = pymongo.MongoClient("mongodb+srv://ladsroot:ladsroot@lads.f97uh.mongodb.net/tau?retryWrites=true&w=majority")
# db = client.tau


client = pymongo.MongoClient("mongodb+srv://ladsroot:ladsroot@lads.f97uh.mongodb.net/tau?retryWrites=true&w=majority")
db = client.tau
