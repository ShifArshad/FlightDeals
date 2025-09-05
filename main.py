from data_manager import DataManager

data_manager = DataManager()
data_sheet = data_manager.get_destination_data()
print(data_sheet)

if data_sheet[0]["iataCode"] == "":
    from flight_search import FlightSearch
    flight_search = FlightSearch()
    for row in data_sheet:
        row["iataCode"] = flight_search.get_destination_code(row["city"])


    data_manager.destination_data = data_sheet
    data_manager.update_code()


