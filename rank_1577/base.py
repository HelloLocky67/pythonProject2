import json
import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


class BaseRank:
    def __init__(self) -> None:
        super().__init__()

        self.level = "level-4"
        # self.dev = True
        self.dev = False  # False OT

        self.dev_web_host = "https://dev.admin.newsapp.5054399.com"
        self.dev_web_cookie = {"PHPSESSID": "hhih7miora767201vnmsimlm01"}
        self.ot_web_host = "http://ot.admin.newsapp.5054399.com"
        self.ot_web_cookie = {"PHPSESSID": "ol0l5edok1kgn8vdhshn11acs3"}

        self.dev_huodong_host = "http://t-huodong2.3839.com"
        self.ot_huodong_host = "https://huodong2.3839.com"

        # bbs 论坛后台
        self.ot_bbs_host = "http://ot.admin.bbs3839.5054399.com"
        self.ot_bbs_cookie = {"_bbsadmin3839_v2_": '1731632668.b4bbab4af7d6ceeec004038262263037l3en418'}

        self.dev_bbs_host = "http://t.bbs.admin.3839.com"
        self.dev_bbs_cookie = {"_bbsadmin3839_v2_": '1731380137.b0174d20e4ec73a473c948a0206a46c9xiDY278'}

        # app 用户信息
        self.dev_app_bbs_host = "https://bbs.3839app.com"
        self.dev_app_user_id = "69300080"  # 用户 user_id
        self.dev_app_user_token = "6a4c805dbd2c48ab08701eb6d134c18e"

        self.ot_app_user_id = "69300080"
        self.ot_app_user_token = "6a4c805dbd2c48ab08701eb6d134c18e"
        self.ot_app_bbs_host = "https://bbs.3839app.com"

        self.dev_app_comment_host = "http://t.comment.3839app.com"
        # self.ot_app_comment_host = "https://comment.3839app.com" # 正式环境
        self.ot_app_comment_host = "http://ot.comment.3839app.com"

        self.dev_api_3839_app_host = "https://api.3839app.com"
        self.ot_api_3839_app_host = "https://api.3839app.com"

        self.dev_news_app_host = "http://t.newsapp.5054399.com"
        self.ot_news_app_host = "http://ot.newsapp.5054399.com"

        self.open_id = "383938391003"
        self.devices = "kbA6328540D7AC8BFA1E575139C76E5932"

        # 5566  设备
        self.header = {
            "User-Agent": "Androidkb/1.5.7.507(android;auto;7.1.2;1080x1920;WiFi);at"
        }

        if self.dev:
            self.web_host = self.dev_web_host
            self.web_cookie = self.dev_web_cookie

            self.app_user_token = self.dev_app_user_token
            self.app_user_id = self.dev_app_user_id

            self.app_bbs_host = self.dev_app_bbs_host
            self.huodong_host = self.dev_huodong_host

            self.bbs_host = self.ot_bbs_host
            self.bbs_cookie = self.ot_bbs_cookie

            self.app_comment_host = self.dev_app_comment_host

            self.api_3839_app_host = self.dev_api_3839_app_host

            self.news_app_host = self.dev_news_app_host

        else:

            self.web_host = self.ot_web_host
            self.web_cookie = self.ot_web_cookie

            self.app_user_token = self.ot_app_user_token
            self.app_user_id = self.ot_app_user_id

            self.app_bbs_host = self.ot_app_bbs_host
            self.huodong_host = self.ot_huodong_host

            self.bbs_host = self.dev_bbs_host
            self.bbs_cookie = self.dev_bbs_cookie

            self.app_comment_host = self.ot_app_comment_host
            self.api_3839_app_host = self.ot_api_3839_app_host

            self.news_app_host = self.ot_news_app_host

    def get_kb_web_rank_data(self, rank_title, rank_type):
        """
            获取榜单的 自然排序页面 数据
        """
        # print(f"=============  爬取快爆 {tag_item['title']} 榜单页面 数据   ==================")
        # web_rank_url = self.web_host + f'/other/other.top.v2.php?ac=l&typeid={tag_item["type"].replace("type", "")}'
        #                            "/other/other.top.v2.php?ac=org_l&typeid=69" 自然排序
        # result = requests.get(url=web_rank_url, cookies=self.web_cookie)
        # if result.status_code == 200:
        #     detail_soup = BeautifulSoup(result.content, 'html5lib')
        #     detail = detail_soup.select("table")
        #     print("a")
        #
        print(f"=============  爬取快爆 {rank_title} 榜单 自然排序页面 数据   ==================")
        rank_list = []

        url = self.web_host + f'/other/other.top.v2.php?ac=org_l&typeid={rank_type}'
        result = requests.get(url=url, cookies=self.web_cookie)
        if result.status_code == 200:
            result_soup = BeautifulSoup(result.content, 'html5lib')
            trs = result_soup.select("table.table-hover > tbody > tr")
            for index in range(1, len(trs)):
                tr = trs[index]
                rank_list.append({"rank": tr.select("td")[0].text, "game_id": tr.select("td")[1].text,
                                  "game_name": tr.select("td")[2].text, "values": tr.select("td")[3].text})
        else:
            print(f"=============  爬取快爆 {rank_title} 榜单 自然排序页面 数据  失败   ==================")
        return rank_list

    # Todo: 获取预约数据
    def get_pre_data(self, game_name, game_id, time_list):
        print(f"=========== 《 获取预约数据 》  game_name = {game_name} = {game_id} ======")

        pre_appointment_number_list = []

        # date_to_convert = "2024-08-08"  # 需要转换的日期
        btime = int(datetime.timestamp(datetime.strptime(time_list[-1], "%Y-%m-%d")))
        etime = int(datetime.timestamp(datetime.strptime(time_list[0], "%Y-%m-%d"))) + 24 * 60 * 60 - 1

        try:
            game_pre_detail_url = self.web_host + "/other/other.yuyue.php"
            data = {
                "ac": "get_detail",
                "gid": game_id,
                "btime": btime,
                "etime": etime
            }
            game_pre_detail_result = requests.post(url=game_pre_detail_url, data=data, cookies=self.web_cookie)
            if game_pre_detail_result.status_code == 200:
                result = game_pre_detail_result.json()
                for _time in time_list:
                    if _time in result['result']:
                        pre_appointment_number_list.append(int(result['result'][_time]))
                    else:
                        pre_appointment_number_list.append(0)

        except Exception as e:
            print(f"==  爬取失败!!!  == 获取预约数据 game_name:{game_name} ==== {game_id} ==== e: {e}======")
        return pre_appointment_number_list

    # 获取 时间列表
    def get_days_time_list(self, _days):
        # _days 多少天
        # 获取当前日期
        current_date = datetime.now()
        date_list = []
        # 生成近七天的日期
        for i in range(0, _days):
            date = current_date - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            date_list.append(date_str)
        print(date_list)
        # ['2024-08-08', '2024-08-07', '2024-08-06', '2024-08-05', '2024-08-04', '2024-08-03', '2024-08-02'] 7天
        return date_list

    def get_game_event_time(self, game_id, distance_days):
        X = 0  # 事件时间系数
        number = 0  # 重要程度系数
        type = ""  # 采用_"首发时间系数" 、采用_"更新时间系数"
        first_time = ""  # 最早事件更新时间
        game_event_time = ""  # 游戏事件最新日期  # chengshi gdp ba
        try:
            url = self.web_host + f"/games/game.android.v2.php?ac=edit&id={game_id}"
            print(f"=====获取 游戏事件最新日期 ============ {game_id} ============= ")
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                trs = soup.select("tr")
                for tr in trs:
                    '''  
                         >>> 当「最新事件更新日期-首次事件更新日期 <= 3day」时，该款游戏视为「新开预约游戏」，执行「首发时间系数」逻辑
                         >>> 当「最新事件更新日期-首次事件更新日期 > 3day」时，该款游戏视为「新更新预约游戏」，执行「更新时间系数」逻辑
                    '''
                    if "游戏开启时间记录（格式为: [日期]文案）" in tr.text:  # 重要程度系数
                        if not tr.select("td")[1].text.strip() is None and len(tr.select("td")[1].text.strip()) > 0:
                            # 重要程度系数
                            if "尚在研发中" in tr.select("td")[1].text.strip().split("\n")[0]:  # 尚在研发中，测试时间待定
                                number = 0.5
                            else:
                                number = 1.0
                            # importance_time = get_time(tr.select("td")[1].text.strip())
                            print(f"重要程度系数为:{number}")
                            first_time = tr.select("td")[1].text.strip().split("\n")[-1].split("]")[0][1:].replace(".",
                                                                                                                   "-")

                    if "游戏事件最新日期" in tr.text:
                        game_event_time = tr.select("td")[1].text.strip()
                        print("游戏事件最新日期:", game_event_time)

                if len(game_event_time.strip()) < 3:
                    # 事件更新时间为空时，时间系数取 X = 1
                    type = "事件时间系数-游戏事件最新日期 == Null(为空 类型)"
                    X = 0
                else:

                    # 定义日期格式  旧算法
                    date_format = "%Y-%m-%d"
                    # 将字符串转换为datetime对象
                    game_event_time_dt = datetime.strptime(game_event_time, date_format)
                    # 将datetime对象转换为时间戳
                    game_event_time_int = int(game_event_time_dt.timestamp())
                    # print(game_event_time_int)

                    # 将字符串转换为datetime对象
                    first_time_dt = datetime.strptime(first_time, date_format)
                    # 将datetime对象转换为时间戳
                    first_time_int = int(first_time_dt.timestamp())
                    # print(first_time_int)

                    if game_event_time_int - first_time_int <= distance_days * 24 * 60 * 60:
                        '''
                         >>> 首发 时间间隔天数X=当前时间-首次事件更新日期+1；如：5月3日为最新事件更新时间，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推                     
                        '''
                        type = "事件时间系数-首发时间系数"

                        current_time = datetime.now()
                        # 计算间隔天数X
                        days_difference = (current_time - first_time_dt).days + 1
                        print(f'当前时间：{current_time.strftime("%Y-%m-%d")}')
                        print(f'首发时间系数：{first_time_dt.strftime("%Y-%m-%d")}')
                        print(f'时间间隔天数：{days_difference}')
                        if 0 < days_difference <= 1:
                            X = 25
                        elif 1 < days_difference <= 2:
                            X = 15
                        elif 2 < days_difference <= 3:
                            X = 10
                        elif 3 < days_difference <= 7:
                            X = 8
                        elif 7 < days_difference <= 14:
                            X = 3
                        elif days_difference > 14:
                            X = 1
                        print(f'{type} X：{X}')
                        '''                      
                         >>> 0<X≤1对应的首发时间系数为25  
                         >>> 1<X≤2对应的首发时间系数为15
                         >>> 2<X≤3对应的首发时间系数为10
                         >>> 3<X≤7对应的首发时间系数为8
                         >>> 7<X≤14对应的首发时间系数为3
                         >>> X>14对应的首发时间系数为1  
                        '''

                    else:

                        '''
                         >>> 更新时间间隔天数X=当前时间-最新事件更新时间+1；如：5月3日为最新事件更新时间，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推                    
                        '''
                        type = "事件时间系数-更新时间系数"

                        current_time = datetime.now()
                        # 计算间隔天数X
                        days_difference = (current_time - game_event_time_dt).days + 1
                        print(f'当前时间：{current_time.strftime("%Y-%m-%d")}')
                        print(f'事件最新时间：{game_event_time_dt.strftime("%Y-%m-%d")}')
                        print(f'时间间隔天数：{days_difference}')
                        if 0 < days_difference <= 2:
                            X = 5
                        elif 2 < days_difference <= 7:
                            X = 3
                        elif days_difference > 7:
                            X = 1
                        print(f'{type} X：{X}')
                        '''                       
                         >>> 0<X≤2对应的更新时间系数为5
                         >>> 2<X≤7对应的更新时间系数为3
                         >>> X>7对应的更新时间系数为1    
                        '''
            else:
                print(
                    f"===  获取  == 游戏事件最新日期  失败   status_code : {game_info_result.status_code} ==============")
        except Exception as e:
            print(f"===  获取  == 游戏事件最新日期  失败 === e : {e} ============")
        # print(f"游戏事件最新日期:{game_event_time}")

        ['事件时间系数', '重要程度系数', '采用那种算法', "最早游戏事件时间", "游戏事件最新时间"]
        return [X, number, type, first_time, game_event_time]

    # 获取 普通游戏 下载量 及 更新量 快玩量
    def get_game_download_data(self, game_id, game_name, time_list, game_type):
        name = quote(game_name)
        download_number = 0  # 下载量
        update_number = 0  # 更新数量
        fast_download_number = 0  # 快玩量
        try:
            url = self.web_host + f'/tongji/tongji.downstat.php?date_range={time_list[-1]}+%7E+{time_list[0]}&name={name}&pagenum=&c2=1&query=1'
            print(
                f"=====获取 普通游戏 下载数据 ===== {time_list[-1]}至{time_list[0]} ======= {game_id} _  {game_name}============= ")
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                tbody = soup.select("table.table-hover > tbody")
                if tbody is None:
                    print(
                        f"=====获取 普通游戏 下载数据 失败：tbody ============ {game_id} _  {game_name}============= ")
                else:
                    trs = soup.select("table.table-hover > tbody > tr")
                    _index = -1
                    for index, tr in enumerate(trs):
                        if len(tr.select("td")) > 0:
                            if str(game_id) in tr.select("td")[2].text:
                                _index = index

                    if _index > -1:
                        if game_type is None:
                            if "80371" in game_id:
                                print(11)
                            # 普通
                            download_number = int(
                                trs[_index].select("td")[3].text.replace("\t", "").replace("明细", "").strip())
                            update_number = int(
                                trs[_index].select("td")[5].text.replace("\t", "").replace("明细", "").strip())
                            # if len(trs[1].select("td")[7].text.strip()) == 0:
                            #     fast_download_number = 0
                            # else:
                            #     fast_download_number = int(
                            #         trs[1].select("td")[7].text.replace("\t", "").replace("明细", "").strip())
                        elif game_type == "fast":
                            # 只有 快玩也一样
                            download_number = int(
                                trs[_index].select("td")[3].text.replace("\t", "").replace("明细", "").strip())
                            update_number = int(
                                trs[_index].select("td")[5].text.replace("\t", "").replace("明细", "").strip())
                            # if len(trs[1].select("td")[7].text.strip()) == 0:
                            #     fast_download_number = 0
                            # else:
                            #     fast_download_number = int(
                            #         trs[1].select("td")[7].text.replace("\t", "").replace("明细", "").strip())

                        elif game_type == "cloud":
                            download_number = int(
                                trs[1].select("td")[3].text.replace("\t", "").replace("明细", "").strip())
                            update_number = int(
                                trs[1].select("td")[5].text.replace("\t", "").replace("明细", "").strip())
                            # if len(trs[1].select("td")[7].text.strip()) == 0:
                            #     fast_download_number = 0
                            # else:
                            #     fast_download_number = int(
                            #         trs[1].select("td")[7].text.replace("\t", "").replace("明细", "").strip())
                        else:
                            # 小游戏
                            download_number = int(
                                trs[_index].select("td")[3].text.replace("\t", "").replace("明细", "").strip())
                            update_number = int(
                                trs[_index].select("td")[5].text.replace("\t", "").replace("明细", "").strip())
                            # if len(trs[1].select("td")[7].text.strip()) == 0:
                            #     fast_download_number = 0
                            # else:
                            #     fast_download_number = int(
                            #         trs[1].select("td")[7].text.replace("\t", "").replace("明细", "").strip())

                    else:
                        print(f"普通游戏:{game_name}___该段时间内__无__下载数据")
            else:
                print(
                    f"=====获取 普通游戏 下载数据 失败 status_code： {game_info_result.status_code}============ {game_id} _  {game_name}============= ")
        except Exception as e:
            print(f"=====获取 普通游戏 下载数据 异常 ： {str(e)}============ {game_id} _  {game_name}============= ")

        result = {"download_number": download_number, "update_number": update_number,
                  "fast_download_number": fast_download_number}
        print(result)
        return result

    # 获取 快玩游戏 下载量 及 更新量
    def get_fast_game_download_data(self, game_id, game_name, time_list):
        fast_download_number = 0  # 下载量
        fast_update_number = 0  # 更新数量

        try:
            url = self.web_host + f"/tongji/tongji.fast.game.php?ac=list&gid={game_id}&title=&date_range={time_list[-1]}+%7E+{time_list[0]}&order=1&pagenum="
            print(
                f"=====获取 快玩游戏 下载数据 ==== {time_list[-1]}至{time_list[0]} ======== {game_id} _  {game_name}============= ")
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                tbody = soup.select("table.table-hover > tbody")
                if tbody is None:
                    print(
                        f"=====获取 快玩游戏 下载数据 失败：tbody ============ {game_id} _  {game_name}============= ")
                else:
                    trs = soup.select("table.table-hover > tbody > tr")

                    _index = -1
                    for index, tr in enumerate(trs):
                        if len(tr.select("td")) > 0:
                            if str(game_id) in tr.select("td")[2].text or str(game_id) in tr.select("td")[0].text:
                                _index = index

                    if _index > -1:
                        fast_download_number = int(trs[_index].select("td")[2].text.strip())
                        fast_update_number = int(trs[_index].select("td")[7].text.strip())
                    else:
                        print(f"快玩游戏:{game_name}___该段时间内__无__下载数据")
            else:
                print(
                    f"=====获取 快玩游戏 下载数据 失败 status_code： {game_info_result.status_code}============ {game_id} _  {game_name}============= ")
        except Exception as e:
            print(f"=====获取 快玩游戏 下载数据 异常 ： {str(e)}============ {game_id} _  {game_name}============= ")

        result = {"fast_download_number": fast_download_number, "fast_update_number": fast_update_number}
        print(result)
        return result

    # todo: app 获取评论 的加密
    def get_comment_token(self, data):
        headers = {
            # 正常的UA末尾加上";at"用于区分是否是自动化的脚本
            'User-Agent': 'Androidkb/1.5.5.205(android;HLK-AL00;10;1080x2340;WIFI);at'
        }
        url = "http://t.admin.newsapp.5054399.com/apiat.php?type=4"
        res = json.loads(requests.request("POST", url, data=data).text)
        data = res['result']
        return data

    # 获取 APP游戏详情页中的 评分数据
    def get_app_game_detail_data(self, game_type, game_id, status):
        score_data = {}
        # status = 普 云 快 小
        if "普" not in status and "云" not in status and "小" not in status and "快" in status:
            # 只包含了 快 取 快玩游戏详情页的 评分数据
            # 快玩
            url = self.app_comment_host + f"/app/comment.php?m=comment&ac=get_comment_list&v=1.0&last_id=0&pid=1&fid={game_id}&cursor=0&customize_tag_id=0&sort=default&kb_game_type=fast&limit=20&list_type=all"
            data = {
                "device": self.devices,
                "last_id": "0",
                "pid": "1",
                "_url": url,
                "fid": game_id,
                "cursor": "0",
                "app_name": "1.5.7.7_debug",
                "list_type": "all",
                "device_system_version": "7.1.2",
                "ts": str(int(time.time())),
                "app_version": "351",
                "permission_storage": "1",
                "device_name": "auto",
                "sort": "default",
                "customize_tag_id": "0",
                "kb_game_type": "fast",
                "isNightMode": "0",
                "limit": "20",
                "level": "4"
            }
            data = self.get_comment_token(data)
            score_data = self.get_app_game_detail_list(url, data, game_id, "快玩")
        else:
            # 云 快 小 取 普游戏详情页的
            # 普通游戏  Normal
            url = self.app_comment_host + f'/app/comment.php?m=comment&ac=get_comment_list&v=1.0&last_id=0&pid=1&fid={game_id}&cursor=0&customize_tag_id=0&sort=default&limit=20&list_type=all'
            data = {
                "device": self.devices,
                "last_id": "0",
                "pid": "1",
                "_url": url,
                "fid": game_id,
                "cursor": "0",
                "app_name": "1.5.7.7_debug",
                "list_type": "all",
                "device_system_version": "7.1.2",
                "ts": str(int(time.time())),
                "app_version": "351",
                "permission_storage": "1",
                "device_name": "auto",
                "sort": "default",
                "customize_tag_id": "0",
                "isNightMode": "0",
                "limit": "20",
                "level": "4"
            }
            data = self.get_comment_token(data)
            score_data = self.get_app_game_detail_list(url, data, game_id, "普通游戏")

        if False:
            if game_type is None:
                # 普通游戏  Normal
                url = self.app_comment_host + f'/app/comment.php?m=comment&ac=get_comment_list&v=1.0&last_id=0&pid=1&fid={game_id}&cursor=0&customize_tag_id=0&sort=default&limit=20&list_type=all'
                data = {
                    "device": self.devices,
                    "last_id": "0",
                    "pid": "1",
                    "_url": url,
                    "fid": game_id,
                    "cursor": "0",
                    "app_name": "1.5.7.7_debug",
                    "list_type": "all",
                    "device_system_version": "7.1.2",
                    "ts": str(int(time.time())),
                    "app_version": "351",
                    "permission_storage": "1",
                    "device_name": "auto",
                    "sort": "default",
                    "customize_tag_id": "0",
                    "isNightMode": "0",
                    "limit": "20",
                    "level": "4"
                }
                data = self.get_comment_token(data)
                score_data = self.get_app_game_detail_list(url, data, game_id, "普通游戏")


            elif game_type == "fast":
                # 快玩
                url = self.app_comment_host + f"/app/comment.php?m=comment&ac=get_comment_list&v=1.0&last_id=0&pid=1&fid={game_id}&cursor=0&customize_tag_id=0&sort=default&kb_game_type={game_type}&limit=20&list_type=all"
                data = {
                    "device": self.devices,
                    "last_id": "0",
                    "pid": "1",
                    "_url": url,
                    "fid": game_id,
                    "cursor": "0",
                    "app_name": "1.5.7.7_debug",
                    "list_type": "all",
                    "device_system_version": "7.1.2",
                    "ts": str(int(time.time())),
                    "app_version": "351",
                    "permission_storage": "1",
                    "device_name": "auto",
                    "sort": "default",
                    "customize_tag_id": "0",
                    "kb_game_type": "fast",
                    "isNightMode": "0",
                    "limit": "20",
                    "level": "4"
                }
                data = self.get_comment_token(data)
                score_data = self.get_app_game_detail_list(url, data, game_id, "快玩")


            elif game_type == "cloud":
                # 云玩
                url = self.app_comment_host + f"/app/comment.php?m=comment&ac=get_comment_list&v=1.0&last_id=0&pid=1&fid={game_id}&cursor=0&customize_tag_id=0&sort=default&kb_game_type={game_type}&limit=20&list_type=all"
                data = {
                    "device": self.devices,
                    "last_id": "0",
                    "pid": "1",
                    "_url": url,
                    "fid": game_id,
                    "cursor": "0",
                    "app_name": "1.5.7.7_debug",
                    "list_type": "all",
                    "device_system_version": "7.1.2",
                    "ts": str(int(time.time())),
                    "app_version": "351",
                    "permission_storage": "1",
                    "device_name": "auto",
                    "sort": "default",
                    "customize_tag_id": "0",
                    "kb_game_type": "cloud",
                    "isNightMode": "0",
                    "limit": "20",
                    "level": "4"
                }
                data = self.get_comment_token(data)
                score_data = self.get_app_game_detail_list(url, data, game_id, "云玩")

            else:
                # 小游戏 没有游戏详情页 取值 都为0
                score_data = {"all_star": 0, "3_star": 0, "7_star": 0, "game_type_des": "小游戏"}
        return score_data

    def get_app_game_detail_list(self, url, data, game_id, game_type_des):
        score_data = {}
        reuslt = requests.post(url=url, headers=self.header, data=data)
        if reuslt.status_code == 200:
            result_data = reuslt.json()
            if game_id == "128686":
                print(1)
            '''
                ['star']  当前评分、评分都取这个  7701 历史评分也取这个
                ['recent_user_star']
                ['recent_day_star']  近七天评分
            '''
            score_data['c_all_star'] = result_data['result']['star_info']['star']  # 当前评分、评分都取这个  (7701 历史评分也取这个)
            score_data['3_star'] = result_data['result']['star_info']['recent_user_star']
            score_data['7_star'] = result_data['result']['star_info']['recent_day_star']  # 9.4近七天评分
            score_data['game_type_des'] = game_type_des
            print(score_data)
        else:
            print(f"======== {game_id}====获取 评分失败===============")

        return score_data

    # 爬取后台 安卓游戏后台第二版本 获取 该游戏 上架了哪几种 （普 云 快 小）
    def get_web_game_detail(self, game_id):
        content = ""
        try:
            url = self.web_host + f"/games/game.android.v2.php?ac=list&id={game_id}&search_keyword=&packag=&status=0&audit_status=-1&update=0&pubdate=0&kb_down=0&source=-1&level=%E5%85%A8%E9%83%A8&down=%E5%85%A8%E9%83%A8&version_type=%E5%85%A8%E9%83%A8"
            print(f"=====获取 上架游戏类型： ============ {game_id} ============= ")
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                trs = soup.select("table.table-hover > tbody > tr")
                if len(trs) > 1:
                    content = trs[1].select("td")[7].text.replace(" ", "").replace("\n", "、")
                    print(content)
                else:
                    print(f"{game_id}___未搜索到——该游戏数据---")
        except Exception as e:
            print(f"=======获取 {game_id}异常：{str(e)} 上架哪几种类型游戏 ========================")

        return content

    def get_time(self, tr, des):
        time_list = [0, ""]
        if not tr.select_one("input") is None and "value" in tr.select_one("input").attrs and len(
                tr.select_one("input").attrs["value"]) > 5:
            print(f'{des} = {tr.select_one("input").attrs["value"]}')
            time_list[0] = self.dealwith_time(tr.select_one("input").attrs["value"])
            time_list[1] = tr.select_one("input").attrs["value"]
        return time_list

    def dealwith_time(self, date_str):
        # 日期字符串
        # date_str = '2018-06-29 15:45:25'
        # 将日期字符串转换为datetime对象  日期转换
        dt_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        # 转换为时间戳
        timestamp = int(time.mktime(dt_obj.timetuple()))  # 秒
        return timestamp

    # 获取 游戏上架 时间系数 琳琅
    def get_game_launch_time(self, game_id):
        item_data = {}
        try:
            url = self.web_host + f"/games/game.android.v2.php?ac=edit&id={game_id}"
            print(f"=====获取 游戏上架日期 ============ {game_id} ============= ")
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                trs = soup.select("tr")
                for tr in trs:
                    # if "上架时间" in tr.text.strip():
                    #     print(111)
                    if "上架时间" == tr.text.strip():
                        time_arrays = self.get_time(tr, "上架-时间")
                        item_data['Y'] = 0
                        item_data['listing_time'] = time_arrays[0]
                        item_data['listing_time_str'] = time_arrays[1]
                        if len(item_data['listing_time_str']) < 3:
                            item_data['Y'] = 1
                            print(f'上架时间：为空')
                        else:
                            # 定义日期格式  旧算法
                            date_format = "%Y-%m-%d %H:%M:%S"
                            # 将字符串转换为datetime对象
                            listing_time_dt = datetime.strptime(item_data['listing_time_str'], date_format)

                            current_time = datetime.now()
                            # 计算间隔天数X
                            days_difference = (current_time - listing_time_dt).days + 1
                            print(f'当前时间：{current_time.strftime(date_format)}')
                            print(f'上架时间：{listing_time_dt.strftime(date_format)}')
                            print(f'时间间隔天数：{days_difference}')
                            if 0 < days_difference <= 1:
                                item_data['Y'] = 2
                            elif 1 < days_difference <= 2:
                                item_data['Y'] = 1.8
                            elif 2 < days_difference <= 3:
                                item_data['Y'] = 1.5
                            elif 3 < days_difference <= 7:
                                item_data['Y'] = 1.2
                            elif days_difference > 7:
                                item_data['Y'] = 1
                        print(f'时间系数 X：{item_data["Y"]}')
                        '''
                        >> 上架时间间隔天数X=当前时间-上架时间+1；如：5月3日上架，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推
                 >> 0<X≤1对应的上架时间系数为2
                 >> 1<X≤2对应的上架时间系数为1.8
                 >> 2<X≤3对应的上架时间系数为1.5
                 >> 3<X≤7对应的上架时间系数为1.2
                 >> X>7对应的上架时间系数为1
                 >> 当字段为空时，上架时间系数取1                                                
                        '''
        except Exception as e:
            print(f"获取上架时间数据异常：{str(e)}")

        return item_data

    # todo：获取 游戏 订单量
    def get_game_order_data(self, game_id, game_name, _time):
        number = ""
        # game_id = "110689"
        url = f"http://t.admin.newsapp.5054399.com/ccq.test.php?type=7&gid={game_id}&time={_time}"
        result = requests.get(url=url)
        if result.status_code == 200:
            content = result.text.strip()

            if game_id in content:
                number = int((content[content.index('cnt] =>') + 7:content.index(")\n\n")]).strip())
            else:
                number = 0
            print(f"======= {game_id} __ {game_name} 近7天订单量： {number} =================")
            pass
        else:
            print(f"======= {game_id} __ {game_name} :获取订单量接口 失败 =================")

        return number

    # 获取 游戏上架 时间系数 热销榜
    def get_hot_sell_game_launch_time(self, game_id):
        item_data = {}
        try:
            url = self.web_host + f"/games/game.android.v2.php?ac=edit&id={game_id}"
            print(f"=====获取 游戏上架日期 ============ {game_id} ============= ")
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                trs = soup.select("tr")
                for tr in trs:

                    if "上架时间" == tr.text.strip():
                        time_arrays = self.get_time(tr, "上架-时间")
                        item_data['Y'] = 0
                        item_data['listing_time'] = time_arrays[0]
                        item_data['listing_time_str'] = time_arrays[1]
                        if len(item_data['listing_time_str']) < 3:
                            print("上架时间为 空,直接过滤")
                            item_data['Y'] = 0
                        else:
                            # 定义日期格式  旧算法
                            date_format = "%Y-%m-%d %H:%M:%S"
                            # 将字符串转换为datetime对象
                            listing_time_dt = datetime.strptime(item_data['listing_time_str'], date_format)

                            current_time = datetime.now()
                            # 计算间隔天数X
                            days_difference = (current_time - listing_time_dt).days + 1
                            print(f'当前时间：{current_time.strftime(date_format)}')
                            print(f'上架时间：{listing_time_dt.strftime(date_format)}')
                            print(f'时间间隔天数：{days_difference}')
                            item_data['时间间隔天数'] = days_difference
                            if 0 < days_difference <= 1:
                                item_data['Y'] = 10
                            elif 1 < days_difference <= 2:
                                item_data['Y'] = 8
                            elif 2 < days_difference <= 3:
                                item_data['Y'] = 6
                            elif 3 < days_difference <= 7:
                                item_data['Y'] = 3
                            elif days_difference > 7:
                                item_data['Y'] = 1
                            print(f'时间系数 Y：{item_data["Y"]}')
                            '''
                                >> 上架时间间隔天数X=当前时间-上架时间+1；如：5月3日上架，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推
                                >> 0<X≤1对应的上架时间系数为10
                                >> 1<X≤2对应的上架时间系数为8
                                >> 2<X≤3对应的上架时间系数为6
                                >> 3<X≤7对应的上架时间系数为3
                                >> X>7对应的上架时间系数为1
                                >> 当字段为空时，上架时间系数取1                                             
                            '''
        except Exception as e:
            print(f"获取上架时间数据异常：{str(e)}")

        return item_data

    # 爬取后台 安卓游戏后台第二版本 获取 该游戏 上架 状态
    def get_web_game_detail_status(self, game_id):
        content = ""
        try:
            url = self.web_host + f"/games/game.android.v2.php?ac=list&id={game_id}&search_keyword=&packag=&status=0&audit_status=-1&update=0&pubdate=0&kb_down=0&source=-1&level=%E5%85%A8%E9%83%A8&down=%E5%85%A8%E9%83%A8&version_type=%E5%85%A8%E9%83%A8"
            print(f"=====获取 游戏状态情况： ============ {game_id} ============= ")
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                trs = soup.select("table.table-hover > tbody > tr")
                if len(trs) > 1:
                    content = trs[1].select("td")[7].text.replace(" ", "").replace("\n", "、")
                    print(content)
                else:
                    print(f"{game_id}___未搜索到——该游戏数据---")
        except Exception as e:
            print(f"=======获取 游戏状态情况 {game_id}异常：{str(e)}  ========================")

        return content

    # 独家 获取独家有 上架 时间、 版本更新时间    游戏时间最新日期
    # 获取 游戏上架 时间系数 琳琅
    def get_dujia_game_launch_time(self, game_id):
        item_data = {}
        try:
            url = self.web_host + f"/games/game.android.v2.php?ac=edit&id={game_id}"
            print(f"=====获取 游戏上架日期、版本更新时间、游戏时间最新日期 ============ {game_id} ============= ")
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                trs = soup.select("tr")
                for tr in trs:
                    if "游戏事件最新日期" in tr.text:
                        if len(tr.select("td")[1].text.strip()) < 3:
                            item_data['game_event_new_time'] = 0
                            item_data['game_event_new_time_str'] = ""
                        else:
                            item_data['game_event_new_time'] = self.dealwith_time(
                                tr.select("td")[1].text.strip() + " 00:00:00")
                            item_data['game_event_new_time_str'] = tr.select("td")[1].text.strip() + " 00:00:00"
                            print(f"游戏事件最新日期:{item_data['game_event_new_time']}")

                    if "版本更新时间" == tr.text.strip():
                        time_arrays2 = self.get_time(tr, "版本-更新时间")
                        item_data['version_update_time'] = time_arrays2[0]
                        item_data['version_update_str'] = time_arrays2[1]

                    if "上架时间" == tr.text.strip():
                        time_arrays = self.get_time(tr, "上架-时间")
                        item_data['listing_time'] = time_arrays[0]
                        item_data['listing_time_str'] = time_arrays[1]

        except Exception as e:
            print(f"获取 游戏上架日期、版本更新时间、游戏时间最新日期 异常：{str(e)}")

        return item_data

    # 获取 小游戏统计页面 数据
    def get_web_mini_game_list(self, time_list):
        result_list = []
        page = 1  # 一页 20条数据   150条
        try:
            while page <= 8:
                url = self.web_host + f"/tongji/tongji.tencent.mini.php?ac=list&gid=&appname=&date_range={time_list[-1]}+%7E+{time_list[0]}&page={page}"
                page += 1
                result = requests.get(url=url, cookies=self.web_cookie)
                if result.status_code == 200:
                    soup = BeautifulSoup(result.content, "html5lib")
                    tbody = soup.select_one("table.table-hover > tbody")
                    #trs = tbody.select("tr")

                    if tbody is not None:
                        trs = tbody.select("tr")
                    else:
                        trs = []

                    trs = trs[1:-1]
                    for tr in trs:
                        tds = tr.select("td")
                        if "上架" in tds[5].text.strip():
                            result_list.append({"rank": tds[0].text.strip(),
                                                "game_id": tds[1].text.strip(),
                                                "game_name": tds[3].text.strip(),
                                                "game_status": tds[5].text.strip(),  # 上架
                                                "values": int(tds[6].text.strip())})  # 启动次数
                else:
                    print(f"=== page: {page} 获取小游戏统计页 失败")
        except Exception as e:
            print(f"获取小游戏统计页  page: {page} 异常： {str(e)}")
        return result_list

    # 获取 快玩统计页 启动次数
    def get_web_fast_game_list(self, time_list):
        result_list = []
        page = 1  # 一页 50条数据  150条
        try:
            while page <= 4:
                url = self.web_host + f"/tongji/tongji.fast.game.php?ac=list&gid=&title=&date_range={time_list[-1]}+%7E+{time_list[0]}&order=1&pagenum=&page={page}"
                page += 1
                result = requests.get(url=url, cookies=self.web_cookie)
                if result.status_code == 200:
                    soup = BeautifulSoup(result.content, "html5lib")
                    tbody = soup.select_one("table.table-hover > tbody")
                    #trs = tbody.select("tr")

                    if tbody is not None:
                        trs = tbody.select("tr")
                    else:
                        trs = []

                    trs = trs[1:]
                    for tr in trs:
                        tds = tr.select("td")
                        # if "上架" in tds[5].text.strip():
                        result_list.append({"game_id": tds[0].text.strip(),
                                            "game_name": tds[1].text.strip(),

                                            "values": int(tds[5].text.strip())})  # 启动次数
                else:
                    print(f"=== page: {page} 获取-快玩统计页 失败")
        except Exception as e:
            print(f"获取-快玩游戏统计页  page: {page} 异常： {str(e)}")
        return result_list

    # 获取 云玩 启动次数 云玩统计页面
    def get_web_cloud_game_list(self, time_list):
        result_list = []
        page = 1  # 一页 20条数据  150条
        try:

            while page <= 8:
                url = self.web_host + f"/ucenter/ucenter.cloudgame.data.php?ac=l2&platform=0&gid=&gamename=&container=&search_date_range={time_list[-1]}+%7E+{time_list[0]}&order=0&per_page=20&page={page}"
                page += 1
                result = requests.get(url=url, cookies=self.web_cookie)
                if result.status_code == 200:
                    soup = BeautifulSoup(result.content, "html5lib")
                    tbody = soup.select_one("table.table-hover > tbody")
                    #trs = tbody.select("tr")

                    if tbody is not None:
                        trs = tbody.select("tr")
                    else:
                        trs = []

                    trs = trs[1:]
                    for tr in trs:
                        tds = tr.select("td")
                        if "上架" in tds[4].text.strip():
                            result_list.append({"rank": tds[0].text.strip(),
                                                "game_id": tds[1].text.strip(),
                                                "game_name": tds[2].text.strip(),
                                                "game_status": tds[4].text.strip(),  # 上架
                                                "values": int(tds[7].text.strip())})  # 启动次数
                else:
                    print(f"=== page: {page} 获取-云玩统计页 失败")
        except Exception as e:
            print(f"获取-云玩游戏统计页  page: {page} 异常： {str(e)}")
        return result_list

    # 获取app app近期热门榜
    def get_app_rank_list(self, des):
        single_rank_lists = []
        rank_url = self.news_app_host + f"/cdn/android/ranktop-home-1577-type-hot2-page-1-{self.level}.htm"
        print(f"=============  获取 {des} tab 数据   ==================")
        result = requests.get(url=rank_url, headers=self.header)
        if result.json()['code'] == 100:
            rank_datas = result.json()['result']['data']
            for single_item in rank_datas:
                score = 0.0
                if len(single_item['score']) > 0:
                    score = float(single_item['score'])
                '''
                > 评分系数：
                >> 当“0<=评分<5”时，评分系数为 0.5（“评分=0”指列表数据无评分展示）
                >> 其余情况，评分系数为1
                '''
                scoring_coefficient = 1
                if 0 <= score < 5:
                    scoring_coefficient = 0.5

                item = {'game_id': single_item['id'],
                        'game_name': single_item['title'],
                        'score': score,
                        'scoring_coefficient': scoring_coefficient
                        }
                print(item)
                single_rank_lists.append(item)
                # if single_item['downinfo']['status'] == "1":
                #     single_rank_lists.append(item)
                # else:
                #     print(f"=============  非下载状态数据 {item}   ==================")
        else:
            print(f"=============  获取 {des} tab 数据  失败   ==================")

        return single_rank_lists

    # 获取上周日 日期
    def get_last_sunday_str(self):
        # 获取当前时间
        now = datetime.now()

        # 计算今天是周几（0=星期一，1=星期二，..., 6=星期天）
        current_weekday = now.weekday()
        # days = 0
        # if current_weekday == 0:
        #     days = current_weekday + 1
        # elif current_weekday == 1:
        #     days = current_weekday + 1
        # elif current_weekday == 2:
        #     days = current_weekday + 1
        # elif current_weekday == 3:
        #     days = current_weekday + 1
        # elif current_weekday == 4:
        #     days = current_weekday + 1
        # elif current_weekday == 5:
        #     days = current_weekday + 1
        # elif current_weekday == 6:
        #     days = current_weekday + 1

        # 计算上周日的日期
        last_sunday = now - timedelta(days=current_weekday + 1)

        date_format = "%Y-%m-%d"  # %H:%M:%S
        last_sunday = last_sunday.strftime(date_format)

        # 获取上周日的时间戳
        # timestamp = int(last_sunday.timestamp())

        return last_sunday

    # 获取本周的日期 timestamp
    def get_weekday_str(self):
        # 获取当前时间
        now = datetime.now()

        # 计算今天是周几（0=星期一，1=星期二，..., 6=星期天）
        current_weekday = now.weekday()
        # 计算本周 日期
        date_format = "%Y-%m-%d"
        monday = now - timedelta(days=current_weekday)
        monday = monday.strftime(date_format)

        today = now.strftime(date_format)

        return [today, monday]

    # 获取上周的日期 timestamp
    def get_last_week_str(self, number):
        # 获取当前时间
        now = datetime.now()

        # 计算今天是周几（0=星期一，1=星期二，..., 6=星期天）
        current_weekday = now.weekday()
        # 计算本周 日期
        date_format = "%Y-%m-%d"
        last_sunday = now - timedelta(days=current_weekday + 1 + 7 * number)
        end_last_sunday = last_sunday.strftime(date_format)  # 上周日

        last_monday = now - timedelta(days=current_weekday + 7 + 7 * number)
        start_last_monday = last_monday.strftime(date_format)  # 上周一

        return [end_last_sunday, start_last_monday]

    # 获取 近期榜单游戏 时间系数  游戏更新时间、 上架时间
    def get_recent_hot_game_launch_time(self, game_id):
        item_data = {}
        try:
            url = self.web_host + f"/games/game.android.v2.php?ac=edit&id={game_id}"
            print(f"=====获取 游戏上架日期、版本更新时间 ============ {game_id} ============= ")
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                trs = soup.select("tr")
                for tr in trs:
                    if "版本更新时间" == tr.text.strip():
                        time_arrays2 = self.get_time(tr, "版本-更新时间")
                        item_data['version_update_time'] = time_arrays2[0]
                        item_data['version_update_str'] = time_arrays2[1]

                    if "上架时间" == tr.text.strip():
                        time_arrays = self.get_time(tr, "上架-时间")
                        item_data['listing_time'] = time_arrays[0]
                        item_data['listing_time_str'] = time_arrays[1]

        except Exception as e:
            print(f"获取 {game_id}  游戏上架日期、版本更新时间、 异常：{str(e)}")
        print(item_data)
        return item_data

    # 手动 刷新 排行榜
    def get_refresh_rank(self, rank_type):
        if self.dev:
            url = self.web_host + f"/other/other.top.v2.php?ac=pm&typeid={rank_type}"
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                #contents = soup.select_one("script").contents
                # unicode_string = "\\u624b\\u52a8\\u6392\\u540d\\u5b8c\\u6210"
                # 解码为中文字符
                #decoded_string = contents[0].text.encode('utf-8').decode('unicode-escape')
                #print(decoded_string)
                script_element = soup.select_one("script")
                if script_element is not None:
                    contents = script_element.contents
                    decoded_string = contents[0].text.encode('utf-8').decode('unicode-escape')
                    print(decoded_string)
                else:
                    print("Script element not found")

    # 获取小时普通明细  普通游戏下载量 小时明细
    def get_web_download_detail_datas(self, time_list, game_id, game_name):
        all_download = 0
        hour_data = ""
        try:
            now = datetime.now()
            # 提取当前时间的小时
            current_hour = now.hour - 1  # 14:40 ->14  ->>>14-1 =13 获取14点之前的数据 所以要-1
            url = self.web_host + f'/tongji/tongji.downstat.php?ac=detail&gid={game_id}&btime={time_list[0]}&etime={time_list[0]}&type=num'
            download_info_result = requests.get(url=url, cookies=self.web_cookie)
            if download_info_result.json()['code'] == 100:
                if len(download_info_result.json()['list']) > 0:
                    hour_data = download_info_result.json()['list'][time_list[0].replace("-", "")]['hour_data']
                    print(current_hour)
                    for index, item in enumerate(hour_data):
                        if index <= current_hour:
                            all_download += item['num']

                print(f" 普通游戏 今日小时下载数据 ： 总的：{all_download},详情：{hour_data}")
            else:
                print(f" 普通游戏 今日各时段 小时下载明细 获取失败 :game :{game_id}")

        except Exception as e:
            print(f" 普通游戏 今日各时段 小时下载明细 获取异常 {str(e)} :game :{game_id}")
        return [all_download, hour_data]

    # 获取小时普通明细  普通游戏下载量 小时明细
    def get_web_update_detail_datas(self, time_list, game_id, game_name):
        all_update = 0
        hour_data = ""
        try:
            now = datetime.now()
            # 提取当前时间的小时
            current_hour = now.hour - 1  # 14:40 ->14  ->>>14-1 =13 获取14点之前的数据 所以要-1
            url = self.web_host + f'/tongji/tongji.downstat.php?ac=detail&gid={game_id}&btime={time_list[0]}&etime={time_list[0]}&type=update_num'
            download_info_result = requests.get(url=url, cookies=self.web_cookie)
            if download_info_result.json()['code'] == 100:
                hour_data = download_info_result.json()['list'][time_list[0].replace("-", "")]['hour_data']
                for index, item in enumerate(hour_data):
                    if index <= current_hour:
                        all_update += item['num']
                print(f" 普通游戏 今日小时更新数据 ：总的：{all_update},详情：{hour_data}")
            else:
                print(f" 普通游戏 今日各时段 小时更新明细 获取失败 :game :{game_id}")

        except Exception as e:
            print(f" 普通游戏 今日各时段 小时更新明细 获取异常 {str(e)} :game :{game_id}")
        return [all_update, hour_data]

    # 获取app app 新品榜
    def get_app_new_rank_list(self, des):
        single_rank_lists = []
        rank_url = self.news_app_host + f"/cdn/android/ranktop-home-1577-type-hot3-page-1-{self.level}.htm"
        print(f"=============  获取 {des} tab 数据   ==================")
        result = requests.get(url=rank_url, headers=self.header)
        if result.json()['code'] == 100:
            rank_datas = result.json()['result']['data']
            for single_item in rank_datas:
                score = 0.0
                if len(single_item['score']) > 0:
                    score = float(single_item['score'])
                '''
                > 评分系数：
                >> 当“0<=评分<5”时，评分系数为 0.5（“评分=0”指列表数据无评分展示）
                >> 其余情况，评分系数为1
                '''
                scoring_coefficient = 1
                if 0 <= score < 5:
                    scoring_coefficient = 0.5

                item = {'game_id': single_item['id'],
                        'game_name': single_item['title'],
                        'score': score,
                        'scoring_coefficient': scoring_coefficient
                        }
                print(item)
                # if single_item['downinfo']['status'] == "1":
                #     single_rank_lists.append(item)
                # else:
                #     print(f"=============  非下载状态数据 {item}   ==================")
                single_rank_lists.append(item)
        else:
            print(f"=============  获取 {des} tab 数据  失败   ==================")

        return single_rank_lists

    # 获取app app 热门榜下的 子Tab榜单
    def get_app_all_rank_list(self, des, rank_type):
        single_rank_lists = []
        rank_url = self.news_app_host + f"/cdn/android/ranktop-home-1577-type-tag{rank_type}-page-1-{self.level}.htm"
        print(f"=============  获取 {des} tab 数据   ==================")
        result = requests.get(url=rank_url, headers=self.header)
        if result.json()['code'] == 100:
            rank_datas = result.json()['result']['data']  # todo:20000
            for single_item in rank_datas:
                score = 0.0
                if len(single_item['score']) > 0:
                    score = float(single_item['score'])
                '''
                > 评分系数：
                >> 当“0<=评分<5”时，评分系数为 0.5（“评分=0”指列表数据无评分展示）
                >> 其余情况，评分系数为1
                '''
                scoring_coefficient = 1
                if 0 <= score < 5:
                    scoring_coefficient = 0.5
                title = single_item['title']
                if "(测试服)" in title:
                    title = title.replace('(测试服)', "")

                item = {'game_id': single_item['id'],
                        'game_name': title,
                        'score': score,
                        'scoring_coefficient': scoring_coefficient
                        }
                print(item)
                single_rank_lists.append(item)
                # if single_item['downinfo']['status'] == "1":
                #     single_rank_lists.append(item)
                # else:
                #     print(f"=============  非下载状态数据 {item}   ==================")
        else:
            print(f"=============  获取 {des} tab 数据  失败   ==================")

        return single_rank_lists

    # http://t.newsapp.5054399.com/
    # 获取app app 往期 热门\新品榜 下的子Tab榜单  共4个  rank_type =1，2，3，4
    def get_app_all_hot_past_list(self, des, rank_type):
        single_rank_lists = []
        rank_url = self.news_app_host + f"/cdn/android/ranktop-home-1577-type-{rank_type}-page-1-{self.level}.htm"
        print(f"=============  获取 {des} tab 数据   ==================")
        result = requests.get(url=rank_url, headers=self.header)
        if result.json()['code'] == 100:
            rank_datas = result.json()['result']['data']
            for single_item in rank_datas:
                score = 0.0
                if len(single_item['score']) > 0:
                    score = float(single_item['score'])
                '''
                > 评分系数：
                >> 当“0<=评分<5”时，评分系数为 0.5（“评分=0”指列表数据无评分展示）
                >> 其余情况，评分系数为1 
                '''
                scoring_coefficient = 1
                if 0 <= score < 5:
                    scoring_coefficient = 0.5

                item = {'game_id': single_item['id'],
                        'game_name': single_item['title'],
                        'score': score,
                        'scoring_coefficient': scoring_coefficient
                        }
                print(item)
                single_rank_lists.append(item)
                # if single_item['downinfo']['status'] == "1":
                #     single_rank_lists.append(item)
                # else:
                #     print(f"=============  非下载状态数据 {item}   ==================")
        else:
            print(f"=============  获取 {des} tab 数据  失败   ==================")

        return single_rank_lists

    # todo:  未修改  获取 近期榜单游戏 时间系数  游戏更新时间、 上架时间
    def get_hot_past_game_time_info(self, game_id):
        item_data = {}
        try:
            url = self.web_host + f"/games/game.android.v2.php?ac=edit&id={game_id}"
            print(f"=====获取 游戏上架日期、版本更新时间 ============ {game_id} ============= ")
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                trs = soup.select("tr")
                for tr in trs:
                    if "版本更新时间" == tr.text.strip():
                        time_arrays2 = self.get_time(tr, "版本-更新时间")
                        item_data['version_update_time'] = time_arrays2[0]
                        item_data['version_update_str'] = time_arrays2[1]

                    if "上架时间" == tr.text.strip():
                        time_arrays = self.get_time(tr, "上架-时间")
                        item_data['listing_time'] = time_arrays[0]
                        item_data['listing_time_str'] = time_arrays[1]

        except Exception as e:
            print(f"获取 {game_id}  游戏上架日期、版本更新时间、 异常：{str(e)}")
        print(item_data)
        return item_data

    # 获取热销榜 原始值
    def get_web_single_rank(self, game_id, game_name, rank_name, type_id):
        order = 0
        web_rank_url = self.web_host + f'/other/other.top.v2.php?ac=l&typeid={type_id}'
        try:
            result = requests.get(url=web_rank_url, cookies=self.web_cookie)
            if result.status_code == 200:
                detail_soup = BeautifulSoup(result.content, 'html5lib')
                detail_trs = detail_soup.select("table.table-hover > tbody > tr")
                for tr in detail_trs:
                    tds = tr.select("td")
                    if len(tds) > 0:
                        if str(game_id) in tds[1].text:
                            order = int(tds[4].text.strip())
            else:
                print(f"获取 {rank_name} {rank_name} 原始值 失败：{str(result.status_code)}")
        except Exception as e:
            print(f"获取 {rank_name} {rank_name} 原始值 异常：{str(e)}")

        return order

    # 获取热销榜   分类榜单 数值 及其他榜单
    def get_web_category_single_rank(self, rank_name, type_id):
        rank_list = []
        web_rank_url = self.web_host + f'/other/other.top.v2.php?ac=l&typeid={type_id}'
        try:
            result = requests.get(url=web_rank_url, cookies=self.web_cookie)
            if result.status_code == 200:
                detail_soup = BeautifulSoup(result.content, 'html5lib')
                detail_trs = detail_soup.select("table.table-hover > tbody > tr")
                for tr in detail_trs:
                    tds = tr.select("td")
                    if len(tds) > 0:
                        rank_list.append({"rank": tr.select("td")[0].text, "game_id": tr.select("td")[1].text,
                                          "game_name": tr.select("td")[2].text.strip(),
                                          "values": tr.select("td")[3].text})
            else:
                print(f"获取 {rank_name} {rank_name} 数值 失败：{str(result.status_code)}")
        except Exception as e:
            print(f"获取 {rank_name} {rank_name} 数值 异常：{str(e)}")

        return rank_list

    # 获取 琳琅榜V2   数值 、原始值  new_version 157701 新算法 直接应用到线上
    def get_web_linlang_v2_rank(self, rank_name, type_id):
        rank_list = []
        web_rank_url = self.web_host + f'/other/other.top.v2.php?ac=l&typeid={type_id}'
        try:
            result = requests.get(url=web_rank_url, cookies=self.web_cookie)
            if result.status_code == 200:
                detail_soup = BeautifulSoup(result.content, 'html5lib')
                detail_trs = detail_soup.select("table.table-hover > tbody > tr")
                for tr in detail_trs:
                    tds = tr.select("td")
                    if len(tds) > 0:
                        rank_list.append({"rank": tr.select("td")[0].text, "game_id": tr.select("td")[1].text,
                                          "game_name": tr.select("td")[2].text.strip(),
                                          "values": tr.select("td")[3].text, "init_values": tr.select("td")[4].text})
            else:
                print(f"获取 {rank_name} {rank_name} 数值 失败：{str(result.status_code)}")
        except Exception as e:
            print(f"获取 {rank_name} {rank_name} 数值 异常：{str(e)}")

        return rank_list

    # 获取 游戏上架 时间系数 琳琅V2
    def get_game_launch_time_linlang_v2(self, game_id):
        item_data = {}
        try:
            url = self.web_host + f"/games/game.android.v2.php?ac=edit&id={game_id}"
            print(f"\n=====获取 游戏上架日期 ============ {game_id} ============= ")
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                trs = soup.select("tr")
                #   >> 上架时间与版本更新时间两个字段同时为空时，时间系数取1；
                #   仅上架时间字段不为空，执行「上架时间系数」逻辑；仅版本更新时间字段不为空，执行「更新时间系数」逻辑；

                time_type = 0
                time_type_content = ""  # 执行了 什么形式的时间系数：  1-> 执行 上架时间系数、  2->执行_更新时间系数
                time_x = 9999
                item_data['listing_time'] = 0
                item_data['version_update_time'] = 0
                for tr in trs:
                    if "上架时间" == tr.text.strip():
                        time_arrays = self.get_time(tr, "上架-时间")
                        item_data['listing_time'] = time_arrays[0]
                        item_data['listing_time_str'] = time_arrays[1]
                    if "版本更新时间" == tr.text.strip():
                        time_arrays2 = self.get_time(tr, "版本-更新时间")
                        item_data['version_update_time'] = time_arrays2[0]
                        item_data['version_update_str'] = time_arrays2[1]

                if item_data['listing_time'] == 0 and item_data['version_update_time'] == 0:
                    time_x = 1
                elif item_data['listing_time'] > 0 and item_data['version_update_time'] == 0:
                    time_type = 1  # 执行 上架时间系数
                elif item_data['listing_time'] == 0 and item_data['version_update_time'] > 0:
                    time_type = 2  # 执行 更新时间系数
                elif item_data['version_update_time'] <= item_data['listing_time']:
                    '''
                        >>> 当「版本最新时间<=上架时间」时，该款游戏视为「新上架游戏」，执行「上架时间系数」逻辑
                         >>> 当「版本最新时间>上架时间」时，该款游戏视为「新更新游戏」，执行「更新时间系数」逻辑
                    '''
                    time_type = 1  # 执行 上架时间系数
                elif item_data['version_update_time'] > item_data['listing_time']:
                    time_type = 2  # 执行 更新时间系数

                if time_type == 1:
                    time_type_content = "1 执行 上架时间系数"
                    # 执行 上架时间系数
                    '''
                     >>> 上架时间间隔天数X=当前时间-上架时间（时间精确到秒）；如：5月3日上架，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推
                         >>> 0<X≤1对应的上架时间系数为5
                         >>> 1<X≤2对应的上架时间系数为4
                         >>> 2<X≤3对应的上架时间系数为3
                         >>> 3<X≤7对应的上架时间系数为2
                         >>> X>7对应的上架时间系数为1
                    '''
                    # 定义日期格式  旧算法
                    date_format = "%Y-%m-%d %H:%M:%S"
                    # 将字符串转换为datetime对象
                    listing_time_dt = datetime.strptime(item_data['listing_time_str'], date_format)

                    current_time = datetime.now()
                    # 计算间隔天数X
                    days_difference = (current_time - listing_time_dt).days + 1
                    print(f'当前时间：{current_time.strftime(date_format)}')
                    print(f'上架时间：{listing_time_dt.strftime(date_format)}')
                    print(f'时间间隔天数：{days_difference}')
                    if 0 < days_difference <= 1:
                        time_x = 5
                    elif 1 < days_difference <= 2:
                        time_x = 4
                    elif 2 < days_difference <= 3:
                        time_x = 3
                    elif 3 < days_difference <= 7:
                        time_x = 2
                    elif days_difference > 7:
                        time_x = 1
                    print(f'上架时间系数 time_x：{time_x}')
                elif time_type == 2:
                    time_type_content = "2 执行 更新时间系数"
                    '''
                     >>> 更新时间间隔天数X=当前时间-版本最新时间（时间精确到秒）；如：5月3日为更新时间，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推
                         >>> 0<X≤1对应的更新时间系数为3
                         >>> 1<X≤2对应的更新时间系数为2.5
                         >>> 2<X≤3对应的更新时间系数为2
                         >>> 3<X≤7对应的更新时间系数为1.5
                         >>> X>7对应的上架时间系数为1
                    '''
                    # 执行 更新时间系数
                    # 定义日期格式  旧算法
                    date_format = "%Y-%m-%d %H:%M:%S"
                    # 将字符串转换为datetime对象
                    listing_time_dt = datetime.strptime(item_data['version_update_str'], date_format)
                    current_time = datetime.now()
                    # 计算间隔天数X
                    days_difference = (current_time - listing_time_dt).days + 1
                    print(f'当前时间：{current_time.strftime(date_format)}')
                    print(f'版本更新时间：{listing_time_dt.strftime(date_format)}')
                    print(f'时间间隔天数：{days_difference}')
                    if 0 < days_difference <= 1:
                        time_x = 3
                    elif 1 < days_difference <= 2:
                        time_x = 2.5
                    elif 2 < days_difference <= 3:
                        time_x = 2
                    elif 3 < days_difference <= 7:
                        time_x = 1.5
                    elif days_difference > 7:
                        time_x = 1
                    print(f'更新时间系数 time_x：{time_x}')

                item_data['time_type_content'] = time_type_content
                item_data['time_x'] = time_x

        except Exception as e:
            print(f"获取上架时间数据异常：{str(e)}")

        return item_data
