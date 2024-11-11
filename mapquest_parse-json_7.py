import urllib.parse
import requests
from colorama import Fore, Style
from tabulate import tabulate
from datetime import datetime, timedelta

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "FEL8LzoNMtLFzRrXvi1lZOCMIESmnMlL"  # Replace with your MapQuest key

print(Fore.CYAN + Style.BRIGHT + "Welcome to the MapQuest Route Finder!" + Style.RESET_ALL)
print("Enter 'quit' or 'q' at any time to exit.\n")

while True:
    orig = input("Starting Location: ")
    if orig.lower() in ["quit", "q"]:
        print(Fore.YELLOW + "\nThank you for using MapQuest Route Finder. Safe travels!" + Style.RESET_ALL)
        break

    dest = input("Destination: ")
    if dest.lower() in ["quit", "q"]:
        print(Fore.YELLOW + "\nThank you for using MapQuest Route Finder. Safe travels!" + Style.RESET_ALL)
        break

    unit = input("Would you like distance in kilometers (K) or miles (M)?: ").strip().upper()
    
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    response = requests.get(url)
    json_data = response.json()
    json_status = json_data.get("info", {}).get("statuscode", None)
    
    if json_status == 0:
        print(Fore.GREEN + "\nDirections found successfully!" + Style.RESET_ALL)
        print("=============================================")
        print(Fore.BLUE + f"Route from {orig} to {dest}" + Style.RESET_ALL)
        print("=============================================")

        directions = []
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            distance = each["distance"] * 1.61 if unit == "K" else each["distance"]
            unit_label = "km" if unit == "K" else "miles"
            directions.append([each["narrative"], f"{distance:.2f} {unit_label}"])

        print(tabulate(directions, headers=["Step-by-Step Directions", "Distance"], tablefmt="fancy_grid"))

        # Displaying a summary at the end of the directions
        total_distance = json_data["route"]["distance"] * 1.61 if unit == "K" else json_data["route"]["distance"]
        total_time = json_data["route"]["formattedTime"]
        arrival_time = datetime.now() + timedelta(seconds=json_data["route"]["time"])

        print("\n" + "="*45)
        print(Fore.GREEN + "Route Summary" + Style.RESET_ALL)
        print("="*45)
        print(f"Total Distance: {total_distance:.2f} {unit_label}")
        print(f"Estimated Travel Time: {total_time}")
        print(f"Estimated Arrival Time: {arrival_time.strftime('%I:%M %p')}")

        print("\n" + Fore.CYAN + "="*45 + Style.RESET_ALL)

        # Option to save route to file
        save_option = input("\nWould you like to save this route to a file? (Y/N): ").strip().upper()
        if save_option == "Y":
            filename = f"Route_from_{orig}_to_{dest}.txt"
            with open(filename, "w") as file:
                file.write(f"Route from {orig} to {dest}\n")
                file.write("="*45 + "\n")
                file.write(f"Total Distance: {total_distance:.2f} {unit_label}\n")
                file.write(f"Estimated Travel Time: {total_time}\n")
                file.write(f"Estimated Arrival Time: {arrival_time.strftime('%I:%M %p')}\n")
                file.write("="*45 + "\n\n")
                file.write("Directions:\n")
                for each in directions:
                    file.write(f"{each[0]} - {each[1]}\n")
                print(Fore.GREEN + f"Route saved to {filename}" + Style.RESET_ALL)

    elif json_status == 402:
        print(Fore.RED + "\nInvalid user inputs for one or both locations. Please try again with valid addresses." + Style.RESET_ALL)
    elif json_status == 611:
        print(Fore.RED + "\nMissing entry for one or both locations. Ensure both starting and destination locations are entered." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"\nError! Status Code: {json_status}. Please refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes" + Style.RESET_ALL)

    print("\n" + "="*45 + "\n")
