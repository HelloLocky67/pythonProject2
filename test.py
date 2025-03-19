import time
import uiautomator2 as u2
from datetime import datetime

d = u2.connect()
d.app_start("com.xmcy.hykb")
screenshot_time = datetime.now().strftime('%Y%m%d_%H%M%S')
d.screenshot(f"d:\\pythonproject\\pythonProject2\\error_screenshots\\cloud_game_fail_{screenshot_time}.png")
print("截图")