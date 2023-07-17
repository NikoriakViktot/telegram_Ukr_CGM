from driver_selenium.soup_read_file import SoupHtmlFile
from redis_tools.tools import RedisTools

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
def main():
    f = SoupHtmlFile()
    for x in f.telegram_today():
        RedisTools.pub(chanel='telegram_today', **x)

    for x in f.telegram_yesterday():
        RedisTools.pub(chanel='telegram_yesterday', **x)


if __name__ == '__main__':
    # f = SoupHtmlFile()
    # for x in f.telegram_today():
    #     RedisTools.pub(chanel='telegram_today', **x)
    #
    # for x in f.telegram_yesterday():
    #     RedisTools.pub(chanel='telegram_yesterday', **x)
    main()
