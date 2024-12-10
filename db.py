import requests

# API endpoint you want to access
url = "https://mytelkomselprod.api.useinsider.com/ins.js?id=10006045"

# Authorization header with the token
headers = {
    "Cookie" : "_gcl_au=1.1.870086312.1733727270; _tguatd=eyJzYyI6IihkaXJlY3QpIiwiZnRzIjoiKGRpcmVjdCkifQ==; _tgpc=5e198421-4a23-5dfa-adfe-bff2cb88d714; _tgidts=eyJzaCI6ImQ0MWQ4Y2Q5OGYwMGIyMDRlOTgwMDk5OGVjZjg0MjdlIiwiY2kiOiIxNzA0M2ExMi0yMTU5LTVmN2QtOGM4Ny04OTVmNzY2M2RlY2EiLCJzaSI6IjY5NzM5OGVjLTRhNzMtNWJhYi05YWJjLTc5ZThkOWZhNTcwNSJ9; _gid=GA1.2.1900556890.1733727271; _ga=GA1.3.421156819.1733727271; _gid=GA1.3.1900556890.1733727271; _fbp=fb.1.1733727270906.9862307035702989; _tt_enable_cookie=1; _ttp=gFwQcPQfC0N4v2wvl4grmFhGzBI.tt.1; _tglksd=eyJzIjoiNjk3Mzk4ZWMtNGE3My01YmFiLTlhYmMtNzllOGQ5ZmE1NzA1Iiwic3QiOjE3MzM3MjcyNzA1NjIsInNvZCI6IihkaXJlY3QpIiwic29kdCI6MTczMzcyNzI3MDU2Miwic29kcyI6ImMiLCJzb2RzdCI6MTczMzcyNzQ1MDQyOX0=; _ga=GA1.2.421156819.1733727271; _tgsid=eyJscGQiOiJ7XCJscHVcIjpcImh0dHBzOi8vbXkudGVsa29tc2VsLmNvbSUyRmxvZ2luJTJGd2ViXCIsXCJscHRcIjpcIk1hc3VrJTIwJTdDJTIwTXlUZWxrb21zZWxcIixcImxwclwiOlwiXCJ9IiwicHMiOiJlZmM1ZjBiOS02Y2UyLTQ1NTItOGZlZi00OTk0Nzg1Y2Y4M2MiLCJwdmMiOiI2Iiwic2MiOiI2OTczOThlYy00YTczLTViYWItOWFiYy03OWU4ZDlmYTU3MDU6LTEiLCJlYyI6IjgiLCJwdiI6IjEiLCJ0aW0iOiI2OTczOThlYy00YTczLTViYWItOWFiYy03OWU4ZDlmYTU3MDU6MTczMzcyNzI3Mzg4NjotMSJ9; _dc_gtm_UA-17788221-7=1; _ga_YC9EDZ12VF=GS1.1.1733727870.2.1.1733728077.60.0.0; _ga_MM0KBCEX5V=GS1.1.1733727270.1.1.1733728077.59.0.0",
    "Content-Type": "application/json"
}

# Make the request
response = requests.get(url, headers=headers)

# Check response
if response.status_code == 200:
    print("Data:", response.json())
else:
    print("Error:", response.status_code, response.text)
