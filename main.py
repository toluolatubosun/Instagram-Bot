from Bot import InstagramBot
import time

bot = InstagramBot("username", "password")
time.sleep(3)
bot.get_follow_count()

