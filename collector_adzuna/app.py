import requests

def app_logic():
    request = requests.get('https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id=2fcbe42d&app_key=dca0e1f6a8240307499ecf6afb168a2d%09&what=git&title_only=software%20developer&location0=UK&location1=North%20East%20England')

    return request.json()

print(app_logic())
