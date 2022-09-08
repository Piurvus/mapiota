import iota_client
import pandas as pd
import json

class IotaClient:
    """Represents an Iota client"""

    def __init__(self):
        """Initializes the Iota client with a connection to the devnet Tangle."""
        self.client = iota_client.Client(
            nodes_name_password=[['https://api.thin-hornet-0.h.chrysalis-devnet.iota.cafe/']])

    def get_message_by_id(self, message_id) -> dict:
        """Gets a message from the Tangle by its message ID"""
        return self.client.get_message_data(message_id)

    def get_message_payload(self, message: dict) -> dict:
        """Gets a messages payload"""
        payload: list = message['payload']['indexation']
        parsed_payload = {}
        for i, entry in enumerate(payload):
            data = entry['data']
            parsed_index = str(bytes.fromhex((entry['index'])).decode('utf-8'))
            parsed_text = ''.join(chr(i) for i in data)
            parsed_payload[parsed_index] = parsed_text
        return parsed_payload

    def send_message(self, index: str, value: str) -> str:
        """Sends a message to the Tangle. Returns the sent messages id."""
        message = self.client.message(index=index, data_str=value)
        return message['message_id']

    def get_messages_by_index(self, index: str):
        """Gets a list of messages from the Tangle with a given index"""
        return self.client.find_messages(indexation_keys=[index])


"""Functions for easier Data Management"""

def getDataframe(indList):
    """Returns the DataFrame with all the Data"""
    payloads = retrieveData(indList)
    return pd.DataFrame.from_dict(payloads)

def retrieveData(indList):
    """Retrieves Data from the given IndexList"""
    client = IotaClient()

    payloads = []

    for ind in indList:
        msgs = client.get_messages_by_index(ind)
        payloads = payloads + [json.loads(client.get_message_payload(msg)[ind]) for msg in msgs]

    return payloads


