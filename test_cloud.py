import time
import uiautomator2 as u2
from datetime import datetime
import logging
from hykb_interface import HykbUtils

class TestCloud:

    def setup_class(self):
        """
            类初始化函数
        """
<<<<<<< HEAD
        self.d = u2.connect("")
        # 创建截图保存目录
        os.makedirs("error_screenshots", exist_ok=True)


    def handle_popups(self):
        """
            处理启动流程的各种弹窗
        """
        buttons = ["同意，进入使用","允许", "同意", "我知道了", "跳过", "关闭"]
        for button in buttons:
            if self.d(text=button).exists:
                self.d(text=button).click()
                time.sleep(0.5)
        
        # 处理可能的系统权限弹窗
        if self.d.xpath('//*[@text="允许"]').exists:
            self.d.xpath('//*[@text="允许"]').click()
        if self.d.xpath('//*[@text="始终允许"]').exists:
            self.d.xpath('//*[@text="始终允许"]').click()
        # 处理首页推送弹窗
        if self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/dialog_home_notice_image_close"]').exists:
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/dialog_home_notice_image_close"]').click()    
        if self.d.xpath('//android.widget.FrameLayout[2]').exists:
            self.d.click(0.905, 0.966)

    def login(self):
        """
        执行登录操作
        Returns:
            bool: 登录是否成功
        """
        try:
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始登录流程")
            # 点击首页的"我的"按钮
            if self.d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[5]/android.widget.ImageView[1]').exists:
                self.d.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[5]/android.widget.ImageView[1]').click()
            elif self.d(text="我的").exists:
                self.d(text="我的").click()
            else:
                self.d.click(0.9, 0.95)
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 通过坐标点击'我的'按钮")
            # 等待点击登录/注册按钮出现，点击登录
            time.sleep(2)
            self.d(resourceId="com.xmcy.hykb:id/login").click()
            # 等待登录页加载完成，使用手机号登录
            time.sleep(2)
            # 选择泰国地区号码登录
            self.d(resourceId="com.xmcy.hykb:id/login_area_tv").click()
            time.sleep(2)
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/area_phone_recycler"]/android.widget.FrameLayout[8]').click()
            time.sleep(2)
            # 输入固定手机号
            phone_input = self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/phone_input_login_et_phone_number"]')
            phone_input.set_text("")
            phone_input.set_text("383938391060")
            time.sleep(3)
            # 点击获取验证码按钮
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/tv_get_verification_code"]').click()
            # 等待隐私政策弹窗弹出，点击同意用户协议
            time.sleep(2)
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/bt_agree"]').click()
            # 等待验证码输入框出现并输入
            time.sleep(3)
            code_input = self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/verify_code_edit"]')
            if code_input.exists:
                code_input.set_text("")
                code_input.set_text("123456")
            else:
                # 添加截图
                screenshot_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                self.d.screenshot(f"error_screenshots/cloud_game_fail_{screenshot_time}未找到验证码输入框.png")
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 未找到验证码输入框")
                return False
            # 验证登录结果
            if self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/nickname"]').wait(timeout=5):
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 登录成功！")
                time.sleep(2)
                if self.d.xpath('//*[@text="我知道了"]').exists:
                    self.d.xpath('//*[@text="我知道了"]').click()
                return True
            else:
                # 添加截图
                screenshot_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                self.d.screenshot(f"error_screenshots/cloud_game_fail_{screenshot_time}登录失败.png")
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 登录失败")
                return False
                
        except Exception as e:
            logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 登录过程发生异常: {str(e)}")
            return False
    

    def start_cloud_game(self, game_element):
        """
        启动云游戏并进行游戏测试
        Args:
            game_element: 游戏元素的xpath对象
        Returns:
            bool: 云游戏是否启动成功
        """
        try:
            # 点击云游戏
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击云玩启动按钮...")
            game_element.click()
            time.sleep(2)
            # 处理可能遇到的温馨提示弹窗
            if self.d(resourceId="com.xmcy.hykb:id/left_button").exists:
                self.d(resourceId="com.xmcy.hykb:id/left_button").click()
            if self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').exists:
                self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[3]').click()
            # 等待插件加载并启动游戏
            if self.d(resourceId="com.xmcy.hykb:id/cloud_game_start_tv").wait(timeout=120):
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载成功，开始启动游戏")
                time.sleep(2)
                # 点击开始云玩
                self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/cloud_game_start_tv"]').click()
                logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击开始云玩")
                # 检测边玩边下按钮/云玩顶部带宽延迟元素判断是否进入云玩成功
                if (self.d(resourceId="com.hykb.yuanshenmap:id/ping_view").wait(timeout=120) or 
                    self.d(resourceId="com.hykb.yuanshenmap:id/tv_download_btw").wait(timeout=120)):
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 成功进入云玩")
                    time.sleep(2)
                    # 使用系统返回按钮退出
                    self.d.press("back")
                    time.sleep(1)
                    self.d(resourceId="com.hykb.yuanshenmap:id/cloud_game_dialog_right_tv").click()
                    logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 游戏已退出")
                    return True
                else:
                    # 添加截图
                    screenshot_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                    self.d.screenshot(f"error_screenshots/cloud_game_fail_{screenshot_time}进入云玩失败.png")
                    logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 进入云玩失败")
                    return False
            else:
                # 添加截图
                screenshot_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                self.d.screenshot(f"error_screenshots/cloud_game_fail_{screenshot_time}插件加载失败.png")
                logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 插件加载失败")
                return False
                
        except Exception as e:
            logging.error(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动云游戏过程发生异常: {str(e)}")
            return False
=======
        self.hykb = HykbUtils("5bf8ee8e")
        self.d = self.hykb.d
>>>>>>> 38bd6c5af27bfab4ed8cce0cf16e925dcf77ef65

    def test_cloud_game(self):
        try:
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动好游快爆")
            self.d.app_start("com.xmcy.hykb")   
            # 处理启动弹窗
            start_time = time.time()
            while time.time() - start_time < 30:
                self.hykb.handle_popups()
                time.sleep(1)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 启动完成，弹窗处理结束")
            #调用登录函数
            self.hykb.login()
            # 点击进入我的收藏
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 点击进入我的收藏")
            self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/core_function_view"]/androidx.recyclerview.widget.RecyclerView[1]/android.view.ViewGroup[3]/android.widget.ImageView[1]').click()
            time.sleep(2)
            #调用云玩启动函数
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 测试手游《原神》S6线路")
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]'))
            time.sleep(3)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 测试手游《王者荣耀》S7线路")
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[2]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]'))
            time.sleep(3)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 测试手游《蛋仔派对》S1线路")
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[3]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]'))
            time.sleep(3)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 测试端游《骑马与砍杀》S4_20线路")
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]'))
            time.sleep(3)
            logging.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 测试页游《黄金矿工-页游》S4_1线路")
            self.hykb.start_cloud_game(self.d.xpath('//*[@resource-id="com.xmcy.hykb:id/item_collect_game_union_rlview"]/android.widget.LinearLayout[5]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]'))
        
        finally:
            # 清理数据
            self.hykb.clean_app_data("com.xmcy.hykb")

