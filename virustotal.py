import os
import requests

API_KEY = os.getenv("virustotalkey")


def check_url(url):

    headers = {
        "x-apikey": API_KEY
    }

    params = {
        "url": url
    }

    try:

        # Submit URL for scanning
        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data=params
        )

        if response.status_code != 200:
            return None

        analysis_id = response.json()["data"]["id"]

        # Get analysis result
        analysis = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers
        )

        if analysis.status_code != 200:
            return None

        stats = analysis.json()["data"]["attributes"]["stats"]

        return stats

    except Exception as e:

        print("VirusTotal Error:", e)

        return None
    
if __name__ == "__main__":

    result = check_url("https://www.google.com")

    print(result)
