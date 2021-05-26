# unify-logging-for-gunicorn-uvicorn-with-loguru

```python

import sys

import uvicorn
from loguru import logger
from ulogcorn import UvicornHandler
from uvicorn import Server
from uvicorn.supervisors import ChangeReload, Multiprocess


# server.py

class Configure(uvicorn.Config):
    def configure_logging(self):
        super().configure_logging()
        UvicornHandler().setup()


def run(app, **kwargs):
    config = Configure(app, **kwargs)
    server = Server(config=config)

    if (config.reload or config.workers > 1) and not isinstance(config.app, str):
        logger.warning(
            "You must pass the application as an import string to enable 'reload' or  'workers'."
        )
        sys.exit(1)

    if config.should_reload:
        sock = config.bind_socket()
        supervisor = ChangeReload(config, target=server.run, sockets=[sock])
        supervisor.run()
    elif config.workers > 1:
        sock = config.bind_socket()
        supervisor = Multiprocess(config, target=server.run, sockets=[sock])
        supervisor.run()
    else:
        server.run()


```

```python

# main.py
from fastapi import FastAPI, Request
import server

app = FastAPI()


@app.get("/")
async def monitor():
    logger.info("Service is running")
    return {"status": "Service is running"}


if __name__ == '__main__':
    server.run(app='main:app', host='0.0.0.0', port=8000, debug=True, reload=True)
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