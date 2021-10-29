from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image, ImageGrab
import sys
import time

URL = "https://ocrhocktest.cognitiveservices.azure.com/"
API_KEY = "7467e13d48eb4c318b83e10214daaedb"

computervision_client = ComputerVisionClient(URL, CognitiveServicesCredentials(API_KEY))

print("===== Read File - remote =====")
# Open the image
im = ImageGrab.grabclipboard()
im.save('temp.png', 'PNG')
read_image = open("../temp.png", "rb")



# Call API with URL and raw response (allows you to get the operation location)
read_response = computervision_client.read_in_stream(read_image, raw=True)

# Get the operation location (URL with an ID at the end) from the response
read_operation_location = read_response.headers["Operation-Location"]

# Grab the ID from the URL
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text, line by line
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            # print(line.bounding_box)
print()