import requests

class ChemAPIClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/api"
        self.token = None

    def login(self, username, password):
        url = f"{self.base_url}/token/"
        try:
            response = requests.post(url, json={"username": username, "password": password})
            if response.status_code == 200:
                self.token = response.json()['access']
                return True
            return False
        except:
            return False

    def upload_csv(self, file_path):
        url = f"{self.base_url}/upload/"
        headers = {"Authorization": f"Bearer {self.token}"}
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, headers=headers, files=files)
        return response.json()

    #  Fetch History
    def get_history(self):
        url = f"{self.base_url}/history/"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        return response.json()

    #  Download PDF 
    def download_pdf(self, record_id):
        url = f"{self.base_url}/pdf/{record_id}/"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content  # Returns the raw PDF bytes
        return None