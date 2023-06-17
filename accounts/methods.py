from datetime import datetime

def calculate_nights(start_date, end_date):
    # Convert the date strings to datetime objects
    start_date_obj = datetime.strptime(start_date, "%d/%m/%Y")
    end_date_obj = datetime.strptime(end_date, "%d/%m/%Y")
    
    # Calculate the difference between the two dates
    duration = end_date_obj - start_date_obj
    
    # Extract the number of nights from the duration
    nights = duration.days
    
    return nights

def dconvert(date_string):

    date_object = datetime.strptime(date_string, "%d/%m/%Y").strftime("%Y-%m-%d")
    return date_object

# Assuming you have a model instance called `your_model_instance`

