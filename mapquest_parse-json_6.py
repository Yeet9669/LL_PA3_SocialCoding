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
        for each in json_data["route"]["legs"][0]["maneuvers"]:
        print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
        print("=============================================\n")
    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")
    else:
        print("************************************************************************")
        print("For Staus Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")
