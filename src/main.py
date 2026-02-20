from fastapi import FastAPI

app = FastAPI()


@app.get('/healthcheck')
async def healthcheck() -> None:
    pass
