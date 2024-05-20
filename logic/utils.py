def validate_time_format(time_str):
    try:
        hours, minutes = time_str.split(":")
        if len(hours) != 2 or len(minutes) != 2:
            return False
        if not 0 <= int(hours) <= 23 or not 0 <= int(minutes) <= 59:
            return False
        return True
    except ValueError:
        return False
    
def validate_datetime_format(datetime_str):
    try:
        date_str, time_str = datetime_str.split()
        day, month, year = date_str.split(".")
        hours, minutes = time_str.split(":")
        if len(day) != 2 or len(month) != 2 or len(year) != 2 or len(hours) != 2 or len(minutes) != 2:
            return False
        if not 0 <= int(day) <= 31 or not 0 <= int(month) <= 12 or not 0 <= int(year) <= 99:
            return False
        if not 0 <= int(hours) <= 23 or not 0 <= int(minutes) <= 59:
            return False
        return True
    except ValueError:
        return False