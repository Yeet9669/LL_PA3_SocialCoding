import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "FEL8LzoNMtLFzRrXvi1lZOCMIESmnMlL"  # Replace with your MapQuest key

while True:
    orig = input("Starting Location: ")
    if orig.lower() in ["quit", "q"]:
        break
    dest = input("Destination: ")
    if dest.lower() in ["quit", "q"]:
        break

    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    print("URL: " + url)

    response = requests.get(url)
    json_data = response.json()

    # Get the `statuscode` from the response's `info` section
    json_status = json_data.get("info", {}).get("statuscode", None)

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=============================================")
        print("Directions from " + orig + " to " + dest)
        print("Trip Duration: " + json_data["route"]["formattedTime"])
        print("Miles: " + str(json_data["route"]["distance"]))
        print("=============================================\n")
        print("Kilometers:" + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
    else:
        print("Error with the API request. Status code:", json_status)
