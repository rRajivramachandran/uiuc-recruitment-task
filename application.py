import json
import datetime
import sys

def read_trainings_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    training_dict = {}

    for entry in data:
        name = entry["name"]
        completions = entry["completions"]

        for completion in completions:
            training_name = completion["name"]
            timestamp = completion["timestamp"]
            expires = completion["expires"]

            if training_name not in training_dict:
                training_dict[training_name] = {}

            if name not in training_dict[training_name]:
                training_dict[training_name][name] = {"timestamp": None, "expires": None}

            # Convert timestamps to comparable format (assuming the format is MM/DD/YYYY)
            timestamp_datetime = datetime.datetime.strptime(timestamp, "%m/%d/%Y")

            # Update entry only if the current completion is more recent
            if (
                training_dict[training_name][name]["timestamp"] is None
                or timestamp_datetime > training_dict[training_name][name]["timestamp"]
            ):
                training_dict[training_name][name] = {"timestamp": timestamp_datetime, "expires": expires}

    return training_dict



def dump_completed_trainings(training_dict, output_file):
    summary = []

    for training, participants in training_dict.items():
        summary_dict = {}
        summary_dict["name"] = training
        summary_dict["count"] = len(participants.keys())
        summary.append(summary_dict)
    with open(output_file, 'w') as file:
        json.dump({"completed_trainings": summary}, file, indent=2)
        
def get_fiscal_year(timestamp):
    date_object = datetime.datetime.strptime(timestamp, "%m/%d/%Y")
    if date_object.month >= 7:
        return date_object.year + 1
    else:
        return date_object.year
        
def get_completed_in_fiscal_year(file_dict, training_name, fiscal_year):
    completed_names = []

    if training_name in file_dict:
        for participant, details in file_dict[training_name].items():
            timestamp = details["timestamp"]

            fiscal_year_completion = get_fiscal_year(timestamp.strftime("%m/%d/%Y"))

            if fiscal_year_completion is not None and fiscal_year_completion == fiscal_year:
                completed_names.append(participant)

    return completed_names

def dump_completed_in_fiscal_year(trainings, fiscal_year, output_file, file_dict):
    completed_in_fiscal_year = {}

    for training_name in trainings:
        completed_names = get_completed_in_fiscal_year(file_dict, training_name, fiscal_year)
        completed_in_fiscal_year[training_name] = completed_names

    with open(output_file, 'w') as file:
        json.dump(completed_in_fiscal_year, file, indent=2)
        
def validate_date_format(date_string):
    try:
        datetime.datetime.strptime(date_string, "%m/%d/%Y")
    except ValueError:
        print("Error: Invalid date format. Please use the format MM/DD/YYYY.")
        sys.exit(1)
        
def dump_expired_trainings(file_dict, date_string, output_file):
    validate_date_format(date_string)
    # Convert the input date string to a datetime object
    input_date = datetime.datetime.strptime(date_string, "%m/%d/%Y")

    # Calculate the date one month from the specified date
    one_month_later = input_date + datetime.timedelta(days=30)

    expired_trainings = {}

    for training_name, participants in file_dict.items():
        for participant, details in participants.items():
            timestamp = details["timestamp"]
            expires = details["expires"]

            # Check if the training has already expired or will expire within one month
            if expires is not None:
                expires_date = datetime.datetime.strptime(expires, "%m/%d/%Y")
                if expires_date <= one_month_later:
                    if participant not in expired_trainings:
                        expired_trainings[participant] = []

                    status = "Expired" if expires_date < input_date else "Expires Soon"
                    expired_trainings[participant].append({
                        "training_name": training_name,
                        "timestamp": timestamp.strftime("%m/%d/%Y"),
                        "expires": expires,
                        "status": status
                    })

    with open(output_file, 'w') as file:
        json.dump(expired_trainings, file, indent=2)
        

if __name__ == "__main__":
    file_path = 'trainings.txt'
    file_dict = read_trainings_file(file_path)
    
    dump_completed_trainings(file_dict, "completed_trainings.json")
    
    trainings_list = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
    fiscal_year = 2024
    dump_completed_in_fiscal_year(trainings_list, fiscal_year, "completed_fiscal_year.json", file_dict)
    
    date_string = "10/01/2023"
    dump_expired_trainings(file_dict, date_string, "expired_trainings.json")
