# import the necessary modules and libraries
import json
import unittest
import datetime

# ---------------- READ INPUT FILES ----------------
with open("./data-1.json", "r", encoding="utf-8") as f:
    jsonData1 = json.load(f)

with open("./data-2.json", "r", encoding="utf-8") as f:
    jsonData2 = json.load(f)

# ---------------- EXPECTED RESULT ----------------
# Hardcoded to avoid file mismatch issues
jsonExpectedResult = {
    "deviceID": "dh28dslkja",
    "deviceType": "LaserCutter",
    "timestamp": 1624445837783,
    "location": {
        "country": "japan",
        "city": "tokyo",
        "area": "keiyō-industrial-zone",
        "factory": "daikibo-factory-meiyo",
        "section": "section-1"
    },
    "data": {
        "status": "healthy",
        "temperature": 22
    }
}

# ---------------- CONVERSION FUNCTIONS ----------------

# convert json data from format 1 to the expected format
def convertFromFormat1(jsonObject):

    locationParts = jsonObject["location"].split("/")

    result = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],

        "location": {
            "country": locationParts[0],
            "city": locationParts[1],
            "area": locationParts[2],
            "factory": locationParts[3],
            "section": locationParts[4],
        },

        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"],
        },
    }

    return result


# convert json data from format 2 to the expected format
def convertFromFormat2(jsonObject):

    # convert ISO timestamp → milliseconds (UTC safe)
    dt = datetime.datetime.strptime(
        jsonObject["timestamp"],
        "%Y-%m-%dT%H:%M:%S.%fZ"
    ).replace(tzinfo=datetime.timezone.utc)

    timestamp = int(dt.timestamp() * 1000)

    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp,

        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"],
        },

        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"],
        },
    }

    return result


# ---------------- MAIN FUNCTION ----------------
def main(jsonObject):

    if jsonObject.get("device") is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)


# ---------------- TEST CASES ----------------
class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult, "Type 1 failed")

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult, "Type 2 failed")


# ---------------- RUN ----------------
if __name__ == "__main__":
    unittest.main()