```python

import uvicorn
from fastapi import FastAPI
from loguru import logger
from uvicorn import Config
from ulogcorn import UnifyHandler

app = FastAPI()


@app.get("/")
async def monitor():
    logger.info("Service is running")
    return {"status": "Service is running"}


if __name__ == '__main__':
    server = uvicorn.Server(
        config=Config(app="main:app", host='0.0.0.0', port=8080, reload=True, debug=True)
    )
    UnifyHandler().setup()
    server.run()
```