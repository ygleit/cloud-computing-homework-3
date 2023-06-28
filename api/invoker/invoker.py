import requests

class Invoker:
    def __init__(self) -> None:
        self.target_url = "https://api.api-ninjas.com/v1/nutrition?query={}"
        self.key = "+O3KY/uJO+hwU0C3rZalvA==tcnPdfanjSZv4S6e"

    def invoke(self, name: str):
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(name)
        response = requests.get(api_url, headers={'X-Api-Key': '{}'.format(self.key)})
        return response 
