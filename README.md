# unify-logging-for-gunicorn-uvicorn-with-loguru

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

```python

# gunicorn.conf.py

import os
from loguru import logger
from ulogcorn import UnifyHandler

logger_class = os.getenv("LOGGER_CLASS", "ulogcorn.logger.StubbedGunicornLogger")


def setup():
    UnifyHandler().setup()
    logger.add("all.log", rotation="00:00", retention="10 days", encoding="utf-8", enqueue=True, compression="zip")


setup()

```
```shell

gunicorn -c "$GUNICORN_CONF" "$APP_MODULE"

```