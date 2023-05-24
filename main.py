import asyncio
import handlers
import json
import requests
import misc


async def main():
    await misc.bot.delete_webhook(drop_pending_updates=True)
    await misc.dp.start_polling(misc.bot,
                                )


if __name__ == "__main__":
    asyncio.run(main())
