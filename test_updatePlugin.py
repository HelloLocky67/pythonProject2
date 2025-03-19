import time
import uiautomator2 as u2
from datetime import datetime
import logging
from hykb_interface import HykbUtils

class TestCloud:

    def setup_class(self):
        """
        初始化函数
        """
        self.hykb = HykbUtils("5bf8ee8e")
        self.d = self.hykb.d

    def test_update_plugin(self):
        try:
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动好游快爆")
            self.d.app_start("com.xmcy.hykb")
            # 处理启动弹窗
            start_time = time.time()
            while time.time() - start_time < 30:
                self.hykb.handle_popups()
                time.sleep(1)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动完成，弹窗处理结束")
            time.sleep(2)
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/recyclerview_homeindex_item_often_play"]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.ImageView[1]'))
            time.sleep(2)
            self.d.app_stop("com.xmcy.hykb")
            time.sleep(2)
            self.d.app_start("com.xmcy.hykb")
            # 处理启动弹窗
            start_time = time.time()
            while time.time() - start_time < 30:
                self.hykb.handle_popups()
                time.sleep(1)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动完成，弹窗处理结束")
            time.sleep(2)
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/recyclerview_homeindex_item_often_play"]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.ImageView[1]'))

        finally:
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始卸载插件...")
            try:
                time.sleep(2)
                self.d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[5]/android.view.ViewGroup[1]/android.widget.ImageView[1]').click()
                time.sleep(2)
                self.d(resourceId="com.xmcy.hykb:id/settings_icon").click()
                time.sleep(2)
                self.d(resourceId="com.xmcy.hykb:id/text_setting_download_install").click()
                time.sleep(2)
                self.d(resourceId="com.xmcy.hykb:id/cg_plugin").click()
                time.sleep(2)
                self.d(resourceId="com.xmcy.hykb:id/right_button").click()
                time.sleep(2)
                if self.d(text="卸载云玩&地图工具组件").exists:
                    logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 删除云玩插件失败")
                else:
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 云玩插件已卸载")
                time.sleep(2)
                # 先停止应用
                self.d.app_stop("com.xmcy.hykb")
                time.sleep(2)
            except Exception as e:
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 删除云玩插件失败: {str(e)}")
                self.d.app_stop("com.xmcy.hykb")
                time.sleep(2)
