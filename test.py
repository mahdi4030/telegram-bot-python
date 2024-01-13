import requests

# Set the URL for the POST request
url = 'https://p55-maildomainws.icloud.com/v1/hme/generate'

# Define the headers and cookies
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',  # Example header
    'Content-Type': 'application/json',  # Example header
    'X-Apple-Twosv-Trust-Token': 'HSARMTKNSRVXWFlaxiufPHaLA/yY/e2xmqVNuPMQOG+iHav5smb8p1TJD11QXTM98G13E8I4s2n7ByD8xPMz4Op+K7pECGxtroUfiC9MdlZlB2Wm9o1SK4vMeXvAKOus5nhwPHjkeqO5tNYOTNIR874/RMMb6iCqhJe1z8zF2TwJNlJcftY3hpYfHujuLuO4bh270+w/uCHS5oz9f/JAfZLf2ubr6pTs8f7lDPmgvQ==SRVX',
    'Accept': 'application/json, text/plain, */*',
    'X-Apple-Session-Token': 'izJzAA5Cwz3DeCx3bxwfYsV1VQW7ZMUokchcEpnjAz1HN/7gwW/lK7zVhYp1O5r6syB82yNlJZwhJ5D7zTdWlCRgSRO8jDzJgv2fuVT6vPmeWItaUpFQw8KBFNE+Loahk6T2K0YTXJEqZILdsur5F1LCb/9eP0zRck7bPmRCXNltnvRZLk8zwjEfQ+OkBrRkwQagniowIRWWxT9pP4KXt1F0lon88TyUE25LxTAw5jbO1NQi5TxNKXcua8l3ryZJoX6DKRVgtjbRXYNkfMQGDk0lfj1+5HiCVWdrlej18315rz9d3EVu/smy6iA4TZHoncHjcknu85jE8NrrNS/qX6FmzHutOvvKlGeNX8HSSnotZFeXk7JxmSlWBQT+tzQ9UwUiO51PZ1FUE7dcQlCOkcIybe9TQh5Xu6/MjCwG8avlF5aNHHwDnwtCX0yzQWNuY3saxS9NKvdmUrfqDJ9tHLuzYhIlzUNelIvVIikY023bXQPJQhvsw9KOvuZuCq2BScmg06ryyOkdz9R/Yk+RkcQXvfeVvXyvJtk8SnoAIytJIcOsVuvBVxYS1oy6J8zL+g1Rp9Zak94mRXuONtEmKIYDvsEpR9jVc/bL06xU152KlnlQjqyBimOWLr4XBWL8Sr9ORaxLHLazyOUY02yfFY0kcM0S/tX32x/dAZD8lTGQ+XkFcOL+3WdcbbOPCTwwnmv3krHpgUU2HXeraQqY2pmMEbcM3VjBLlFzZUrQrpB2NqY6jN7xPXplN/5HQUgitbIHnppsZ2eJeUEE7/sNdZeoXukwBZ9YoP0cNIT/CIrUZpqY7P16ddNoavIS+eOacqr17UaSeAcRiqroW4NmB2o1DZc9MIThIo2bChLQ3EpMTWHLIiYzJArIeFaqthnQi4WyejQ9fqLAOWs44rJmONlqa2Ov5wAb7GhTgXl/+m/2H8suoubNXYQl97vmJVE7AdBkQNU/Z+/rY/MWByrBqVcccOzbV/nhYAk50YR0roN12571+L5mVPn2H/DPwrvcf6DmUNMqBcwOPV9micBmCfYXBlHucJ6yDf2QbY4sFBFeEjAbmAa5sNkEHjxfWKU56qqQxW/SlFE6hOrpAWcZHKbgxpFwRaCZrQ1FPuNbU/sd42mawoW+ngbPWpKO+HesZc+NYppbHGLPqUKG75d50agGHQvJlpFiJFOGIhW3WwQZcKqyeWswn1c282aWs+SMAQ2UACM3YZ8q1Bo=',
    'X-Apple-Id-Account-Country': 'FRA',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://www.icloud.com',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
    'Referer': 'https://www.icloud.com/',
    'Connection': 'close'
}

cookies = {
    'X_APPLE_WEB_KB-WFWZ4PBNDP9ETPOF8M5CCU-DQ74': 'v=1: t=Gg==BST_IAAAAAAABLwIAAAAAGTM3tARDmdzLmljbG91ZC5hdXRovQC_RYRPMNyM9ZEOdpESCsk24IEjSPOmRobtD7NzSXTq_xVPoIGVkHTw_QKQS39ya9Hea9Ddu7TBureEsuzGEE5wHkKVhnhwaUP8EmtNGEYFZ4yrhrq7Wk1vssPOEDx17Wn_ijGMHmKbptOPDwSoiFZno3I4TA~~',  # Example cookie
    'X-APPLE-WEBAUTH-HSA-TRUST': '876be86a633b92cecdc2bf3ee2a52fb7b45d557026b765fbc708d1165f2b660f_HSARMTKNSRVXWFlaXDh+kzSuLx6nRWuuh90xRUjT5Zm+hGfaw8Cr6M8GBMRo+ttUy+ySJfSUzS71HiubXAALi7wfpdFxviQV2wQs1wg4gP1iDmiS69ixR0f14D0jXDq1r3hCUIn0M8cCTYI33l2U9Qw/NQXATb3jy/ixuNe25/SRIWOZgjCI1Qx+/teUkkJjBvd+iaf8BhclIjds/GRuHPRRKOhQAlKC3zeuAbCxCw==SRVX',  # Example cookie
    'X-APPLE-WEBAUTH-USER': 'v=1:s=1:d=18319617384',
    'X-APPLE-DS-WEB-SESSION-TOKEN': 'AQGzmdNXEm+yq0+V7peD9ARhID7W7OqP3TZYplPJMtsJBw7PMUCOB6CDdfKuIjB4Qf8k1ydnzVjnbhKvJ2bC5AxMkILdiiM46QGSzeYC7GmMwl51dAt5KB3psOBu1h3hY1JX6KMAVVwPQJKltI0vKPBvtJ1w5xVfaXRKPUshVcMkfCJXJvewvgjltLlLbENtFtxXv/0Pl3/IuTrBYjbbV3VwT/Bcp5Ceu5kdDbKRTJS/Csb5lq0QmEA/vt2DxqYW1thP4jpEsZRigM+h8y+rh2ZzmWgMtymeCJhul1zTCZE+IOiqMEmk9OGc9+ESuZhUciGbKQjyUMWc1EzFOkjD1vDfbxP2lIhkEF0toWjZmx4JQ08wxiegQQ1td76T0EyeshSunP6eOMMd7KzZkjwsMDviq/qPgGz4ICFKW8cxF4eL3H4NhV0Sx0RFFCSW+PltlLhCd+2KsCPgZ+IRvOp4kY9unUrYkYS/s5XSOgZ/0qI0dCNqXhqUI8xPECfnVZjaUVPTTNH95/rJ+3ERbyR4BiBkVnM3gCXyFAxaxx5EGBFjfYXpZkskdDc7X6V8hXRrwdGxZ33p++n9MfdfacWXClYEZa2fP6naZaaowtG+XWskKo4nxNn+JolYEp5a2lOQyBEoUnWZUak/iUP58bfrZl61qEVSsqCqVmLr8O50AzfXt6vDFMlxUH3vXrAdxFuHfbuL0Em/Yt7OBxTqygW/uxKYHZJeG3t94K3z0w82+olNtzGB/ZztQSzDcLpwZmQGPlZKlDHn4qKMCGqmdENkJfERznJmbQWi3/rXYA==',
    'X-APPLE-WEBAUTH-PCS-Documents': 'TGlzdEFwcGw6MTpBcHBsOjE6AeUsbBpNG0kxP+kB1RHcfMyOY6LFr15TpuASkFh6qVU/YzHpHvTpPDznyQ+Y3iqxigze0DJYmW5CArahekkPqvmlytC9URY6P9EygrcRXNZgp7GsqgMx2nTn/wZs19Tmrk9H+mzNaPtvmdXaUIIt9cv/7iCIDWBT7oyADc/w48TpR3FmFtFqNw==',
    'X-APPLE-WEBAUTH-PCS-Photos': 'TGlzdEFwcGw6MTpBcHBsOjE6AfYw8o8NlXNoIdbh8HxrZsXNIoCLvVO+8DZQAqPdcopGdYokNPSQIonm9MMYX+QcwAdjPJlJS5J5fPr1X9RS4pXu3tEMz/rK4E8JUcIApbOlKjhRJSKEXi70ATj7rxFv6U54TAX5GbaWHzkIwZzKmU1x7euiL153XZkwMIali9r3aOemzLI3FQ==',
    'X-APPLE-WEBAUTH-PCS-Cloudkit': 'TGlzdEFwcGw6MTpBcHBsOjE6AcqEb4+NIe4QGdcVsUTKwUGw08VEaR6YSBk+ZZh0l3TKQm7WPelCIqACsUHf22lXzHFRfpf/8QhI9BwI2L46XmcRp4x2UZMufZH8J//N3f3NwbYipzdIUqLLc0ABsVoqvjZPc3HQw67bkfukp5ClCuPDxwQBK0+cxP7J0Ha81DIVV9UXBTpYcg==',
    'X-APPLE-WEBAUTH-PCS-Safari': 'TGlzdEFwcGw6MTpBcHBsOjE6AZtr2V4kiOWKJNSXM9Q4TmRhVoJHyNFWerEyi4HPG1vLeylh0+BqJIxkN6Aia2AMYOAzIU14FTs1p0gv048mUyTXSb9hQwQvnyD2NJQW7L1X9HczdKcXqGY1RInl0u/y07PjL9PGDiHh/Bv88ysWEvOYitime43CyZEl1MQRTJ3Lm0BtGQpjJg==',
    'X-APPLE-WEBAUTH-PCS-Mail': 'TGlzdEFwcGw6MTpBcHBsOjE6AYPsQ+V8f3tSYYFf12rxDGQqqlDMgMU5rq+wzMP7LmMH0JIzSuSoDGcL1o7IKei1M+opfJlCYpvNtQA1osXMeDOAJzHDhD+7rV/wt3V3aXBeU2Aa6F1ugfLvpKGXynuHDUYY2P4yI7wAEwFYAdq+1uuZUuvbi8bUZxkV5LQ9dXdsm+xyATV0GQ==',
    'X-APPLE-WEBAUTH-PCS-Notes': 'TGlzdEFwcGw6MTpBcHBsOjE6Aaj19yWLzeNrvkvRyffmXSrOQ8l837pAAQOz8LK9ImCMg62JCjT8dw08BCfx3VBcqSHZeNRRlPu2A7l3rZCiYWV1fjTyZuaags97c1tCpkIcNPxhZ5TCoIShqfedJtXbkcCDdn+MuyxRM+VSKQpZ9RuSqi1J10fgeCIJw4DXH+benyLi/Tp62w==',
    'X-APPLE-WEBAUTH-PCS-News': 'TGlzdEFwcGw6MTpBcHBsOjE6AcEjFDZ7WcK23wKNg4+QKM8DT9rl1IkLjnQ0KnJ9J5rFSKGgmVZdbTC8vwPwzQrdTEx7y9R86psJQUFMi4JOL44Xje03U4zULXw19X0qWNFwJdkrNsLtyeQ78BPaSSNy4vblztJc9MnXsGZmgU8Ty/ELkuAtLBGms9+ejlFsLSkljsAVDgRN3A==',
    'X-APPLE-WEBAUTH-PCS-Sharing': 'TGlzdEFwcGw6MTpBcHBsOjE6AXnJe/2Y6fDxfy121O4PIUF9tFZYCNPmNx6Aojx3AyB25QvZQBwcMUEcra6z3Kjt7FMeK44YvZKI1IvcttFM2BWXM8OJAfZ3yn+8Vj+pJJpRd3XY6jdDEQ9Q6ecAbfBv3wm/heyD81M95Sin52ANMbMZhDBiHoZmp0Ftk515Wwuh3IDLnJjNUw==',
    'X-APPLE-WEBAUTH-TOKEN': 'v=2:t=GA==BST_IAAAAAAABLwIAAAAAGTM9KYRDmdzLmljbG91ZC5hdXRovQDdieEZ51ZPqgtZQynLvGd9Wl-_AWUyx_PzFlFNPXVmdvHPzg24_4co006Vz9i1BUer0493R1PbAL-l6dmxmSoH0xMLns_WKDkS962qEvUxT45F94Cp0fSf8uFwfGCETgDFOF9es_nYTndb4z5hpQgJJPAlmA~~',
    'X-APPLE-WEBAUTH-VALIDATE': 'v=1:t=GA==BST_IAAAAAAABLwIAAAAAGTM9KYRDmdzLmljbG91ZC5hdXRovQDdieEZ51ZPqgtZQynLvGd9Wl-_AWUyx_PzFlFNPXVmdvHPzg24_4co006Vz9i1BUer0493R1PbAL-l6dmxmSoH0xMLns_WKDkS962qEvUxT5SAbbAbVpitwH3csHs3b1oYxI3NU3eDs3ncqvgyYuNYinNaMA~~'
}

# Send the POST request with the defined cookies, headers, and payload
response = requests.post(url, headers=headers, cookies=cookies)
response_json = response.json()

# Check the response status code
if response_json["success"]:
    created_mail = response_json["result"]["hme"]

    url = "https://p55-maildomainws.icloud.com/v1/hme/reserve"
    payload = {
    'hme': created_mail,  # Example payload data
    'label': 'settings',
    'note': 'Generated through the iCloud Telegram bot'
    }

    response = requests.post(url, headers=headers, cookies=cookies, json=payload)
    response_json = response.json()
    if response_json["success"]:
        # Get the response content
        response_json = response.json()
        print(response_json["result"]["hme"]["hme"])
    else:
        print('Request failed hme reserve:', response.text)
else:
    print('Request failed hme generate:', response.text)
