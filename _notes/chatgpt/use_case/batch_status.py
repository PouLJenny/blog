import os
from openai import OpenAI

os.environ['http_proxy'] = 'socks5://localhost:1080'
os.environ['https_proxy'] = 'socks5://localhost:1080'

with open('/Users/poul/.openai/api_key', 'r') as file:
    api_key_1= file.read().lstrip().rstrip()

client = OpenAI(
  api_key=api_key_1
)


out = client.batches.retrieve("batch_YAotZ9raAwNNIC73IMuIg6xV").to_json()


print(out)


"""
STATUS	DESCRIPTION
validating	the input file is being validated before the batch can begin
failed	    the input file has failed the validation process
in_progress	the input file was successfully validated and the batch is currently being run
finalizing	the batch has completed and the results are being prepared
completed	  the batch has been completed and the results are ready
expired	    the batch was not able to be completed within the 24-hour time window
cancelling	cancellation of the batch has been initiated
cancelled	  the batch was cancelled
"""

