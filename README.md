# novel_client_py
A python client for the novel API

## Installation
```sh
pip install novel_client_py
```
If that doesn't work, try using a python alias:
```sh
python3 -m pip install novel_client_py
python -m pip install novel_client_py
```

## Example usage
```py
import asyncio
from novel_client_py import APIClient

async def main():
    base_url = 'http://localhost:15634'
    client = await APIClient(base_url)

    try:
        auth_response = await client.request_authentication('admin', 'admin')
        print(f"Authentication Response: {auth_response}")

        status_response = await client.make_raw_request('status', method='POST', data={'client': 'py'})
        print(f"Status Response: {status_response}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        await client.session.close()

asyncio.run(main())
```