import asyncio

from telegram.error import NetworkError, TimedOut


async def reply_retry(message, text, attempts=3):
    for percobaan in range(attempts):
        try:
            return await message.reply_text(text)

        except (NetworkError, TimedOut) as e:
            if percobaan == attempts - 1:
                print(f"❌ Gagal mengirim pesan: {e}")
                return None

            print(
                f"⚠️ Koneksi Telegram bermasalah. "
                f"Retry {percobaan + 1}/{attempts}..."
            )

            await asyncio.sleep(2)
