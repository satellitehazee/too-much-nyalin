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

indent_range = 10
updown_range = 40

before = [". ", " L", "[ ", "( ", " ("]
after = [".", "l", "[", "(", "("]
keyw = ["import", "from", "def", "if", "else", "return", "try", "catch", "except", "for", "while"]
broken = ["@", "0", "F", "DD", "O", "E", "G"]

def pyEnhancer(line):
    enhanced_line = str()
    if len(line) < 3:
        return
    for l in broken:
        if line == "DD" or line == "def":
            return
        if line[0] == l:
            for k in keyw:
                if k in line:
                    enhanced_line = line[1::]
                    break
                else:
                    enhanced_line = line
            break
        else:
            enhanced_line = line

    for i in range(len(before)):
        enhanced_line = enhanced_line.replace(before[i], after[i])
    return enhanced_line

def ocrBrute():


    computervision_client = ComputerVisionClient(URL, CognitiveServicesCredentials(API_KEY))

    print("===== Read File - remote =====")
    # Open the image

    read_image = open("temp.png", "rb")

    read_response = computervision_client.read_in_stream(read_image, raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)


    extra_tab = 0
    prev_indent = int()
    prev_whitespace = int()
    result = str()
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                if (line.bounding_box[1] - prev_whitespace) > updown_range:
                    result += "\n"
                if (prev_indent - line.bounding_box[0]) > indent_range:
                    extra_tab -= 1
                prev_indent = line.bounding_box[0]
                prev_whitespace = line.bounding_box[1]

                tab = "\t" * extra_tab

                text_enhanced = pyEnhancer(line.text)
                if text_enhanced:
                    result += tab + text_enhanced + "\n"
                # print(line.bounding_box)

                if ":" in line.text:
                    extra_tab += 1
    # os.remove("temp.png")
    return result


# im = ImageGrab.grabclipboard()
# im.save('temp.png', 'PNG')

# ocrBrute()