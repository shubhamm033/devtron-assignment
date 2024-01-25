

def filter_date_range_filter(start_date, end_date, bucket_folders):
    time_range_folders = []

    for day in bucket_folders:
        day_ = day[:-1]

        if start_date <= day_ <= end_date:
            time_range_folders.append(day)
    return time_range_folders
