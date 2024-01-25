from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .s3_util import S3
from .file_processing import FileProcessing
from .util import filter_date_range_filter
import json


@csrf_exempt
@require_http_methods(["POST"])
def search_text_view(request):
    # Create an S3 object

    s3 = S3()
    # read request data

    data = json.loads(request.body)
    match_string = data.get("keyword")
    start_date = data.get("from")
    end_date = data.get("to")

    # get all date folders of the bucket
    bucket_folders = s3.fetch_details_from_s3()

    # filter all folders which lie in the search range
    time_range_folders = filter_date_range_filter(start_date, end_date, bucket_folders)

    list_of_files = s3.fetch_details_from_s3(time_range_folders)

    file_processing = FileProcessing(s3)
    response = file_processing.process_files(list_of_files, match_string)

    return HttpResponse(response)
