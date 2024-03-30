import os
from pymongo import MongoClient
from dotenv import load_dotenv
import lol_api
import certifi
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
ca = certifi.where()


client = MongoClient(os.getenv("MONGO_DB_URI"), tlsCAFile=ca)
db = client["league_discord_bot"]


async def add_summoner(summoner_riot_id):
    puuid = await lol_api.fetch_summoner_puuid_by_riot_id(summoner_riot_id)
    if puuid:
        collection = db.summoners
        document = {
            "name": summoner_riot_id,
            "puuid": puuid,
            "last_checked": 0,
        }
        result = collection.insert_one(document)
        if result.acknowledged:
            print(
                f"Document for summoner '{summoner_riot_id}' was successfully inserted into MongoDB with _id: {result.inserted_id}"
            )
            return True
        else:
            print(
                f"Failed to insert document into MongoDB for summoner '{summoner_riot_id}'."
            )

    return False


async def get_summoners():
    return list(db.summoners.find({}, {"_id": 0, "name": 1, "puuid": 1}))


async def add_guild(guild_name, guild_id):
    collection = db.discord_servers
    document = {"name": guild_name, "guild_id": guild_id, "date_added": datetime.now()}

    result = collection.insert_one(document)
    if result.acknowledged:
        print(
            f"Document for guild '{guild_name}' was successfully inserted into MongoDB with _id: {result.inserted_id}"
        )
    else:
        print(f"Failed to insert document into MongoDB for guild '{guild_name}'.")
