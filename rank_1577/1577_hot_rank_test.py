"""
    1577版本热门榜近期榜和新品榜的往期回顾榜单自动化测试
todo:热门榜各子榜单新增往期回顾功能        往期热门榜、 往期新品榜
http://task.kuaibao.com/index.php?m=story&f=view&storyID=10013
"""
import time
from datetime import datetime
from base import BaseRank


# adb bugreport
class HotRankTest(BaseRank):

    def __init__(self) -> None:
        super().__init__()

    def start_test(self):
        # self.date_str = "12_16"
        self.date_str = "12_23"

        if True:
            print("============== 往期热门 算法测试 ==================")
            '''
                 > 排序规则：排序值=下载更新量*时间系数*评分系数，依据排序值进行「往期热门各tab」的自然排序，取前150名    
                 > 时间系数：分为上架时间系数和更新时间系数，「新上架游戏」对应“上架时间系数”，「新更新游戏」对应“更新时间系数”    
                    >> 系数类型 判断规则：    
                              >>> 当「更新时间<=上架时间」时，该款游戏视为「新上架游戏」，执行「上架时间系数」逻辑    
                              >>> 当「更新时间>上架时间」时，该款游戏视为「新更新游戏」，执行「更新时间系数」逻辑  
                                
                    >> 「上架时间系数」逻辑：基于上架时间间隔天数，判断对应的上架时间系数    
                              >>> 上架时间间隔天数X=上周日-上架时间+1（时间精确到天）；如：今天9月26日，上周日9月22日新上架，则「上周tab」的X为1    
                              >>> 0<X≤1对应的上架时间系数为3    
                              >>> 1<X≤2对应的上架时间系数为2.8    
                              >>> 2<X≤3对应的上架时间系数为2.5    
                              >>> 3<X≤7对应的上架时间系数为2    
                              >>> X>7对应的上架时间系数为1    
                    >> 「更新时间系数」逻辑：基于更新时间间隔天数，判断对应的更新时间系数    
                              >>> 更新时间间隔天数X=上周日-版本最新时间+1（时间精确到天）；    
                              >>> 0<X≤1对应的更新时间系数为3    
                              >>> 1<X≤2对应的更新时间系数为2.8    
                              >>> 2<X≤3对应的更新时间系数为2.5    
                              >>> 3<X≤7对应的更新时间系数为2
                              >>> X>7对应的上架时间系数为1    
                    >> 上架时间与版本更新时间两个字段同时为空时，时间系数取1；仅上架时间字段不为空，执行「上架时间系数」逻辑；仅版本更新时间字段不为空，执行「更新时间系数」逻辑；
                    
                    > 评分系数：           
                        >> 当“0<=评分<5”时，评分系数为 0.5（“评分=0”指列表数据无评分展示）    
                        >> 其余情况，评分系数为1    
                        
                    > 下载更新量：基于「上周」内新增的[下载量+更新量+快玩量]进行计算    
                        >> 下载更新量=「上周」上架后新增的[下载量+更新量+快玩量]           
            '''
            rank_info = [
                            {"rank_name": "上周", "rank_type": "1", "web_type": "58"},
                            {"rank_name": "两周前", "rank_type": "2", "web_type": "59"},
                            {"rank_name": "三周前", "rank_type": "3", "web_type": "60"},
                            {"rank_name": "四周前", "rank_type": "4", "web_type": "61"},
                        ][:2]

            all_web_lists = []
            for rank_item in rank_info:
                self.get_refresh_rank(rank_item['web_type'])
                web_rank_list = self.get_web_category_single_rank(f"热门_往期榜单({rank_item['rank_name']})",
                                                                  type_id=rank_item['web_type'])
                all_web_lists.append(web_rank_list)

            all_rank_lists = []

            for rank_item in rank_info:
                print(
                    f"\n\n\n ============== 往期热门     {rank_item['rank_name']}   获取列表 及 评分      ===============\n")
                single_rank_list = self.get_app_all_hot_past_list(rank_item['rank_name'],
                                                                  f"hottime{rank_item['rank_type']}")
                all_rank_lists.append(single_rank_list)

            # 合并 整合 后台榜单和 app显示榜单 列表 数据 整成一个列表
            for index, single_rank_list in enumerate(all_rank_lists):
                web_list = all_web_lists[index]
                for item in single_rank_list:
                    for inner_item in web_list:
                        if item['game_id'] == inner_item['game_id']:
                            item['rank'] = inner_item['rank']
                            item['values'] = inner_item['values']

            for j, single_rank_list in enumerate(all_rank_lists):
                print(f"\n\n\n ==============     {rank_info[j]['rank_name']}   获取时间系数      ===============\n")
                # 获取 上架时间、版本更新时间
                '''
                   >>> 当「版本更新时间 <=上架时间」时，该款游戏视为「新上架游戏」，执行「上架时间系数」逻辑
                   >>> 当「版本更新时间 > 上架时间」时，该款游戏视为「新更新游戏」，执行「更新时间系数」逻辑
                '''
                for game_item in single_rank_list:
                    _time = 1000
                    game_item['_time'] = _time
                    time_info = self.get_hot_past_game_time_info(game_item['game_id'])
                    game_item['version_update_str'] = time_info['version_update_str']
                    game_item['listing_time_str'] = time_info['listing_time_str']
                    # game_item['version_update_time'] = time_info['version_update_time']
                    # game_item['listing_time'] = time_info['listing_time']

                    _time_des = ""
                    time_type = 0
                    if "163151" in game_item['game_id']:
                        print(11)
                    if len(time_info['version_update_str']) == 0 and len(time_info['listing_time_str']) == 0:
                        # 上架时间与版本更新时间两个字段同时为空时，时间系数取1；
                        _time = 1
                        game_item['_time'] = _time
                        _time_des = "上架&版本更新 为空"
                    # 上架时间与版本更新时间两个字段同时为空时，时间系数取1；仅上架时间字段不为空，执行「上架时间系数」逻辑；仅版本更新时间字段不为空，执行「更新时间系数」逻辑；
                    elif len(time_info['listing_time_str']) > 0 and len(time_info['version_update_str']) == 0:
                        time_type = 1
                        _time_des = "仅架时间字段 不为空，执行「上架时间系数」逻辑"

                    elif len(time_info['version_update_str']) > 0 and len(time_info['listing_time_str']) == 0:
                        time_type = 2
                        _time_des = "版本更新时间字段 不为空，执行「更新时间系数」逻辑"

                    # >> > 当「更新时间 <= 上架时间」时，该款游戏视为「新上架游戏」，执行「上架时间系数」逻辑
                    # >> > 当「更新时间 > 上架时间」时，该款游戏视为「新更新游戏」，执行「更新时间系数」逻辑

                    elif time_info['version_update_time'] <= time_info['listing_time']:
                        time_type = 1
                        _time_des = "版本最新时间 <= 上架时间，执行「上架时间系数」逻辑"

                    else:
                        time_type = 2
                        _time_des = "版本最新时间 > 上架时间，执行「更新时间系数」逻辑"
                    game_item['_time_des'] = _time_des
                    last_sunday_str = self.get_last_sunday_str()  # 获取上周日

                    if time_type == 1:
                        # 执行「上架时间系数」逻辑
                        # now_date_str = datetime.now().strftime("%Y-%m-%d")
                        # now_info = datetime.strptime(now_date_str, "%Y-%m-%d")
                        last_sunday = datetime.strptime(last_sunday_str, "%Y-%m-%d")
                        last_sunday_timestamp = int(time.mktime(last_sunday.timetuple()))

                        listing_date_str = time_info['listing_time_str'].split(" ")[0]
                        listing_info = datetime.strptime(listing_date_str, '%Y-%m-%d')
                        listing_timestamp = int(time.mktime(listing_info.timetuple()))
                        # '2024-11-10 13:56:41', 'listing_time_str': '2024-12-05 10:49:48',
                        X = 1 + (last_sunday_timestamp - listing_timestamp) / (24 * 60 * 60)
                        # if X <= 0:
                        #     _time = 1
                        if 0 < X <= 1:
                            _time = 3
                        elif 1 < X <= 2:
                            _time = 2.8
                        elif 2 < X <= 3:
                            _time = 2.5
                        elif 3 < X <= 7:
                            _time = 2
                        elif X > 7:
                            _time = 1
                        game_item['_time'] = _time
                        game_item['_X'] = X
                        '''
                              >>> 上架时间间隔天数X=上周日-上架时间+1（时间精确到天）；如：今天9月26日，上周日9月22日新上架，则「上周tab」的X为1    
                              >>> 0<X≤1对应的上架时间系数为3    
                              >>> 1<X≤2对应的上架时间系数为2.8    
                              >>> 2<X≤3对应的上架时间系数为2.5    
                              >>> 3<X≤7对应的上架时间系数为2    
                              >>> X>7对应的上架时间系数为1    
                        '''
                    elif time_type == 2:
                        # 更新时间系数 ['version_update_time']
                        # now_date_str = datetime.now().strftime("%Y-%m-%d")
                        # now_info = datetime.strptime(now_date_str, "%Y-%m-%d")
                        last_sunday = datetime.strptime(last_sunday_str, "%Y-%m-%d")
                        last_sunday_timestamp = int(time.mktime(last_sunday.timetuple()))

                        listing_date_str = time_info['version_update_str'].split(" ")[0]
                        listing_info = datetime.strptime(listing_date_str, '%Y-%m-%d')
                        listing_timestamp = int(time.mktime(listing_info.timetuple()))

                        X = 1 + (last_sunday_timestamp - listing_timestamp) / (24 * 60 * 60)
                        # if X <= 0:
                        #     _time = 1
                        if 0 < X <= 1:
                            _time = 3
                        elif 1 < X <= 2:
                            _time = 2.8
                        elif 2 < X <= 3:
                            _time = 2.5
                        elif 3 < X <= 7:
                            _time = 2
                        elif X > 7:
                            _time = 1
                        game_item['_time'] = _time
                        game_item['_X'] = X
                        '''
                              >>> 更新时间间隔天数X=上周日-版本最新时间+1（时间精确到天）；    
                              >>> 0<X≤1对应的更新时间系数为3    
                              >>> 1<X≤2对应的更新时间系数为2.8    
                              >>> 2<X≤3对应的更新时间系数为2.5    
                              >>> 3<X≤7对应的更新时间系数为2
                              >>> X>7对应的上架时间系数为1    
                        '''
            # 获取上周
            # > 下载更新量：基于「上周」内新增的[下载量 + 更新量 + 快玩量]
            #   进行计算
            #   >> 下载更新量 =「上周」上架后新增的[下载量 + 更新量 + 快玩量]

            for j, single_rank_list in enumerate(all_rank_lists):
                last_week_time_list = self.get_last_week_str(j)

                print(f"\n\n\n ==============     {rank_info[j]['rank_name']}   获取下载量      ===============\n")
                for index, game_item in enumerate(single_rank_list):
                    game_item['all_download_update_data'] = 0

                    download_info = {}
                    # 获取 上周 普通游戏   下载量 + 更新量
                    game_download_data = self.get_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                     last_week_time_list, None)
                    download_info['download_number'] = game_download_data['download_number']
                    download_info['update_number'] = game_download_data['update_number']

                    # # 获取 上周 快玩游戏   下载量   + 更新量
                    fast_game_download_data = self.get_fast_game_download_data(game_item['game_id'],
                                                                               game_item['game_name'],
                                                                               last_week_time_list)
                    download_info['fast_download_number'] = fast_game_download_data['fast_download_number']
                    download_info['fast_update_number'] = fast_game_download_data['fast_update_number']

                    # 下载更新量= 上周 新增的[下载量+更新量+快玩量]
                    game_item['all_download_update_data'] = (
                            download_info['download_number'] + download_info['update_number'] + download_info[
                        'fast_download_number'] + download_info['fast_update_number'])

                    print(
                        f"\n\n=== {index + 1} ====> {game_item['game_id']}_{game_item['game_name']} 下载更新量:{game_item['all_download_update_data']} \n"
                        f"上周 普通游戏下载量 & 更新量 ：{download_info['download_number']} & {download_info['update_number']}\n"
                        f"上周 快玩游戏下载量 & 更新量 ：{download_info['fast_download_number']} & {download_info['fast_update_number']}\n")

            # todo： 排序值=下载更新量*时间系数*评分系数
            for j, single_rank_list in enumerate(all_rank_lists):
                # todo：开始计算 排序值=下载更新量*时间系数*评分系数
                print(f"\n\n\n ==============     {rank_info[j]['rank_name']}   检测结果      ===============\n")
                self.write_data(f"分类榜单/{self.date_str}/往期_热门_{self.date_str}_.txt",
                                f"\n\n\n往期热门     {rank_info[j]['rank_name']}   检测结果")

                for index, game_item in enumerate(single_rank_list):
                    auto_score = game_item['all_download_update_data'] * game_item['_time'] * game_item[
                        'scoring_coefficient']
                    auto_score = round(auto_score, 2)
                    content = ""
                    if "values" not in game_item:
                        content = f"后台排行榜中未查看该项,auto_score : {auto_score}; {game_item}"
                        self.write_data(f"分类榜单/{self.date_str}/往期_热门_{self.date_str}_.txt", content)
                        print(f"后台排行榜中未查看该项,auto_score : {auto_score}; {game_item}")
                    else:
                        if float(game_item['values']) == auto_score:
                            content = f"True {game_item['game_id']}_{game_item['game_name']} score: web->{game_item['values']},auto->{auto_score}_下载量：{game_item['all_download_update_data']}"
                            self.write_data(f"分类榜单/{self.date_str}/往期_热门_{self.date_str}_.txt", content)

                            print(f"{index} True 数值 score: {auto_score} === {game_item}")
                        else:
                            content = f"False {game_item['game_id']}_{game_item['game_name']} score: web->{game_item['values']},auto->{auto_score}_下载量：{game_item['all_download_update_data']}"
                            self.write_data(f"分类榜单/{self.date_str}/往期_热门_{self.date_str}_.txt", content)
                            print(
                                f"{index} False({round(float(game_item['values']) - auto_score, 2)})  数值：{float(game_item['values'])} 、 auto——>{auto_score}   ===>评分系数{game_item['scoring_coefficient']}*时间系数{game_item['_time']} === {game_item}")

        if True:
            print("\n\n\n\n\n\n============== 往期新品 算法测试 ==============")
            '''
                > 游戏范围：「上周日往前推21天内」的「新上架」的游戏；如：今天9.23周一，则「上周日往前推21天内」为9.2-9.22
                 > 数据更新：每周一的00:30:00，通过脚本自动生成「上周tab」的「日期、排序值」，并记录以延用至「两周前/三周前/四周前tab」；延用时，需过滤掉按钮状态变为“查看”的游戏
                 > 时间系数：为上架时间系数；基于上架时间间隔天数，判断对应的上架时间系数
                        >> 上架时间间隔天数X=上周日-上架时间+1（时间精确到天）；如：今天9月26日，上周日9月22日新上架，则「上周tab」的X为1；
                        >> 0<X≤1对应的上架时间系数为3
                        >> 1<X≤2对应的上架时间系数为2.8
                        >> 2<X≤3对应的上架时间系数为2.5
                        >> 3<X≤7对应的上架时间系数为2
                        >> X>7对应的上架时间系数为1
                        >> 当字段为空时，上架时间系数取1
                 > 评分系数：同 近期热门-往期回顾
                 > 下载更新量：同 近期热门-往期回顾
                 > 排序规则：排序值=下载更新量*时间系数*评分系数，依据排序值进行「往期新品4个tab」的自然排序，取前150名            
            '''
            rank_info = [
                            {"rank_name": "上周", "rank_type": "1", "web_type": "62"},
                            {"rank_name": "两周前", "rank_type": "2", "web_type": "63"},
                            {"rank_name": "三周前", "rank_type": "3", "web_type": "64"},
                            {"rank_name": "四周前", "rank_type": "4", "web_type": "65"}
                        ][:2]

            all_web_lists = []
            for rank_item in rank_info:
                self.get_refresh_rank(rank_item['web_type'])
                web_rank_list = self.get_web_category_single_rank(f"新品_往期榜单({rank_item['rank_name']})",
                                                                  type_id=rank_item['web_type'])
                all_web_lists.append(web_rank_list)

            all_rank_lists = []
            for rank_item in rank_info:
                print(f"\n\n\n ==============     {rank_item['rank_name']}   获取列表 及 评分      ===============\n")
                # 包含获取了 评分系数
                single_rank_list = self.get_app_all_hot_past_list(rank_item['rank_name'],
                                                                  f"new{rank_item['rank_type']}")
                all_rank_lists.append(single_rank_list)

            # 合并 整合 后台榜单和 app显示榜单 列表 数据 整成一个列表
            for index, single_rank_list in enumerate(all_rank_lists):
                web_list = all_web_lists[index]
                for item in single_rank_list:
                    for inner_item in web_list:
                        if item['game_id'] == inner_item['game_id']:
                            item['rank'] = inner_item['rank']
                            item['values'] = inner_item['values']

            for j, single_rank_list in enumerate(all_rank_lists):
                print(f"\n\n\n ==============     {rank_info[j]['rank_name']}   获取时间系数      ===============\n")
                # 获取 上架时间
                for game_item in single_rank_list:
                    _time = 1000
                    game_item['_time'] = _time
                    time_info = self.get_hot_past_game_time_info(game_item['game_id'])
                    game_item['listing_time_str'] = time_info['listing_time_str']
                    # game_item['listing_time'] = time_info['listing_time']
                    '''
                        > 时间系数：为上架时间系数；基于上架时间间隔天数，判断对应的上架时间系数
                            >> 当字段为空时，上架时间系数取1            
                    '''
                    _time_des = ""
                    last_sunday_str = self.get_last_sunday_str()  # 获取上周日

                    if len(time_info['listing_time_str']) == 0:
                        _time = 1
                        _time_des = "上架字段为空，上架时间系数取1"
                    else:
                        # 执行「上架时间系数」逻辑
                        _time_des = "执行上架时间逻辑"
                        # now_date_str = datetime.now().strftime("%Y-%m-%d")
                        # now_info = datetime.strptime(now_date_str, "%Y-%m-%d")
                        last_sunday = datetime.strptime(last_sunday_str, "%Y-%m-%d")
                        last_sunday_timestamp = int(time.mktime(last_sunday.timetuple()))

                        listing_date_str = time_info['listing_time_str'].split(" ")[0]
                        listing_info = datetime.strptime(listing_date_str, '%Y-%m-%d')
                        listing_timestamp = int(time.mktime(listing_info.timetuple()))
                        # '2024-11-10 13:56:41', 'listing_time_str': '2024-12-05 10:49:48',
                        X = 1 + (last_sunday_timestamp - listing_timestamp) / (24 * 60 * 60)
                        # if X <= 0:
                        #     _time = 1
                        if 0 < X <= 1:
                            _time = 3
                        elif 1 < X <= 2:
                            _time = 2.8
                        elif 2 < X <= 3:
                            _time = 2.5
                        elif 3 < X <= 7:
                            _time = 2
                        elif X > 7:
                            _time = 1
                        game_item['_time'] = _time
                        game_item['_X'] = X
                        '''
                            >> 上架时间间隔天数X=上周日-上架时间+1（时间精确到天）；如：今天9月26日，上周日9月22日新上架，则「上周tab」的X为1；
                            >> 0<X≤1对应的上架时间系数为3
                            >> 1<X≤2对应的上架时间系数为2.8
                            >> 2<X≤3对应的上架时间系数为2.5
                            >> 3<X≤7对应的上架时间系数为2
                            >> X>7对应的上架时间系数为1
                        '''
                    game_item['_time_des'] = _time_des

            # 获取上周
            # > 下载更新量：基于「上周」内新增的[下载量 + 更新量 + 快玩量]
            #   进行计算
            #   >> 下载更新量 =「上周」上架后新增的[下载量 + 更新量 + 快玩量]
            for j, single_rank_list in enumerate(all_rank_lists):
                last_week_time_list = self.get_last_week_str(j)
                print(f"\n\n\n ==============     {rank_info[j]['rank_name']}   获取下载量      ===============\n")
                for index, game_item in enumerate(single_rank_list):
                    game_item['all_download_update_data'] = 0

                    download_info = {}
                    # 获取 上周 普通游戏   下载量 + 更新量
                    game_download_data = self.get_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                     last_week_time_list, None)
                    download_info['download_number'] = game_download_data['download_number']
                    download_info['update_number'] = game_download_data['update_number']

                    # # 获取 上周 快玩游戏   下载量   + 更新量
                    fast_game_download_data = self.get_fast_game_download_data(game_item['game_id'],
                                                                               game_item['game_name'],
                                                                               last_week_time_list)
                    download_info['fast_download_number'] = fast_game_download_data['fast_download_number']
                    download_info['fast_update_number'] = fast_game_download_data['fast_update_number']

                    # 下载更新量= 上周 新增的[下载量+更新量+快玩量]
                    game_item['all_download_update_data'] = (
                            download_info['download_number'] + download_info['update_number'] + download_info[
                        'fast_download_number'] + download_info['fast_update_number'])

                    print(
                        f"\n\n=== {index + 1} ====> {game_item['game_id']}_{game_item['game_name']} 下载更新量:{game_item['all_download_update_data']} \n"
                        f"上周 普通游戏下载量 & 更新量 ：{download_info['download_number']} & {download_info['update_number']}\n"
                        f"上周 快玩游戏下载量 & 更新量 ：{download_info['fast_download_number']} & {download_info['fast_update_number']}\n")

            # todo： 排序值=下载更新量*时间系数*评分系数
            for j, single_rank_list in enumerate(all_rank_lists):
                # todo：开始计算 排序值=下载更新量*时间系数*评分系数
                print(
                    f"\n\n\n ============== 往期新品     {rank_info[j]['rank_name']}   检测结果      ===============\n")
                self.write_data(f"分类榜单/{self.date_str}/往期_新品_{self.date_str}_.txt",
                                f"\n\n\n往期新品     {rank_info[j]['rank_name']}   检测结果")

                for index, game_item in enumerate(single_rank_list):
                    auto_score = game_item['all_download_update_data'] * game_item['_time'] * game_item[
                        'scoring_coefficient']
                    auto_score = round(auto_score, 2)
                    content = ""

                    if "values" not in game_item:
                        content = f"后台排行榜中未查看该项,auto_score : {auto_score}; {game_item}"
                        print(content)
                        self.write_data(f"分类榜单/{self.date_str}/往期_新品_{self.date_str}_.txt", content)
                    else:
                        if float(game_item['values']) == auto_score:
                            content = f"True {game_item['game_id']}_{game_item['game_name']} score: web->{game_item['values']},auto->{auto_score}_下载量：{game_item['all_download_update_data']}"
                            self.write_data(f"分类榜单/{self.date_str}/往期_新品_{self.date_str}_.txt", content)
                            print(f"True score: {auto_score} === {game_item}")
                        else:
                            content = f"False {game_item['game_id']}_{game_item['game_name']} score: web->{game_item['values']},auto->{auto_score}_下载量：{game_item['all_download_update_data']}"
                            self.write_data(f"分类榜单/{self.date_str}/往期_新品_{self.date_str}_.txt", content)
                            print(
                                f"False {game_item['game_id']}_{game_item['game_name']} score: web->{float(game_item['values'])},auto->{auto_score}  === {game_item}")

    def write_data(self, file_path, content):
        with open(file_path, mode='a+') as f:
            f.write(content + '\n')
            f.flush()


if __name__ == '__main__':
    test = HotRankTest()
    test.start_test()
