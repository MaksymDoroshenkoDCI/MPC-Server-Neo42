import mongomock
import json

# Initialize a mock MongoDB client
client = mongomock.MongoClient()
db = client.neo42_telemetry
collection = db.server_logs

def init_mongodb():
    """Seed the mock MongoDB with telemetry data."""
    telemetry_data = [
        {
            "hostname": "SRV-PROD-01",
            "cpu_usage": "24%",
            "memory": "16GB/32GB",
            "last_reboot": "2026-05-01",
            "active_processes": ["neo42-agent", "chrome-update", "sqlserver"],
            "network_latency": "12ms"
        },
        {
            "hostname": "WS-DEV-MAX",
            "cpu_usage": "85%",
            "memory": "14GB/16GB",
            "temp": "72C",
            "active_processes": ["pycharm", "docker", "teams"],
            "disk_status": "OK"
        }
    ]
    collection.insert_many(telemetry_data)
    print("Mock MongoDB initialized with telemetry data.")

def get_telemetry(hostname: str):
    """Fetch telemetry from mock MongoDB."""
    result = collection.find_one({"hostname": hostname})
    if result:
        # Remove MongoDB internal _id for clean output
        result.pop('_id', None)
        return json.dumps(result, indent=2)
    return None

if __name__ == "__main__":
    init_mongodb()
