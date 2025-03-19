'''

todo: 1577版本排行榜各榜单算法调整自动化测试

热门榜细分子分类（单机、二次元、独立游戏等），飙升榜作为新品榜tab并入  TODO:包含 近期热门榜单_56  长期热门_55  新品_57 及 单机、二次元、独立游戏等
http://task.kuaibao.com/index.php?m=story&f=view&storyID=10012   56

预约榜默认tab算法以及各子tab样式优化  (综合Tab)
http://task.kuaibao.com/index.php?m=story&f=view&storyID=10014   54         True

新增琳琅榜
http://task.kuaibao.com/index.php?m=story&f=view&storyID=10015   52         True

热销榜算法优化及样式优化
http://task.kuaibao.com/index.php?m=story&f=view&storyID=10016   53         True

todo：独家榜、
http://task.kuaibao.com/index.php?m=story&f=view&storyID=10017  独家 = 19     True

todo：在线玩 ->小游戏V2 type = 18、--云游戏V2 type = 17、 --快玩V2 type = 16
http://task.kuaibao.com/index.php?m=story&f=view&storyID=10017              True


热门榜各tab、琳琅榜均是用【普通下载 + 普通更新 + 快玩下载 + 快玩更新】
非纯快玩的，评分，上架时间，版本时间等，都取普通的
纯快玩的，那就取快玩的
'''
import requests
import time
from base import BaseRank
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


class RankTest(BaseRank):

    def __init__(self) -> None:
        super().__init__()

    def start_test(self):
        if False:
            print("==================   TEST 其他各分类榜Tab(20个榜) 检测  ==================")
            '''
            二次元/多人联机/单机等分类榜                                  
                 • 算法策略：        
                     > 游戏范围：处于「上架状态」的某一分类游戏            
                     > 时间系数：同 新品            
                     > 评分系数：同 近期热门            
                     > 下载更新量：同 新品   
                     > 排序规则：排序值=下载更新量*时间系数*评分系数，依据排序值进行「分类游戏榜」的自然排序，取前50名
            '''
            tag_datas = self.get_app_hot_rank_nav_tab_list()[:3]

            content = "榜单："
            for item in tag_datas:
                content += item['title'] + "、"
            print(content)
            all_rank_list = self.get_app_rank_tab_list(tag_datas)  # 包含了获取 评分系数

            all_web_rank_list = []
            for index, tag_item in enumerate(tag_datas):
                web_rank_list = self.get_web_category_single_rank(f"{tag_item['title']}_榜单", type_id=tag_item['id'])[
                                :20]

                # web_rank_list = self.get_kb_web_rank_data(f"{tag_item['title']}_榜单", rank_type=tag_item['id'])  # 前20名
                all_web_rank_list.append(web_rank_list)
                # single_rank_list = all_rank_list[index]
                # 合并每个榜单 整合 后台榜单和 app显示榜单 列表 数据 整成一个列表
                for rank_item in all_rank_list[index]:
                    for inner_item in web_rank_list:
                        if rank_item['game_id'] == inner_item['game_id']:
                            rank_item['rank'] = inner_item['rank']
                            rank_item['values'] = inner_item['values']

            time_list = self.get_days_time_list(_days=2)
            print(time_list)
            # 获得下载量：
            for j, single_rank_list in enumerate(all_rank_list):
                print(f"\n\n============ 获得下载量  {tag_datas[j]['title']}_榜单 ==================")
                # > 下载更新量：基于 今日昨日两天的 [下载量+更新量+快玩量]进行计算（下载更新量 等于后台的“原始值”字段）
                #   >> 下载更新量 = 昨日整日的[下载量+更新量+快玩量]*1% + 今日实时新增的[下载量+更新量+快玩量]
                for index, game_item in enumerate(single_rank_list):
                    game_item['all_download_update_data'] = 0
                    game_item['all_download_info'] = ""

                    download_info = {}
                    # 获取 今日 普通游戏   下载量 + 更新量
                    game_download_data = self.get_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                     time_list[0:1], None)
                    download_info['today_download_number'] = game_download_data['download_number']
                    download_info['today_update_number'] = game_download_data['update_number']

                    # 获取 今日 快玩游戏   下载量 + 更新量
                    fast_game_download_data = self.get_fast_game_download_data(game_item['game_id'],
                                                                               game_item['game_name'],
                                                                               time_list[0:1])
                    download_info['today_fast_download_number'] = fast_game_download_data['fast_download_number']
                    download_info['today_fast_update_number'] = fast_game_download_data['fast_update_number']

                    # 获取 昨日 普通游戏   下载量 + 更新量
                    yesterday_game_download_data = self.get_game_download_data(game_item['game_id'],
                                                                               game_item['game_name'],
                                                                               [time_list[1]], None)
                    download_info['yesterday_download_number'] = yesterday_game_download_data['download_number']
                    download_info['yesterday_update_number'] = yesterday_game_download_data['update_number']

                    # # 获取 上周日 快玩游戏   下载量   + 更新量
                    yesterday_fast_game_download_data = self.get_fast_game_download_data(game_item['game_id'],
                                                                                         game_item['game_name'],
                                                                                         [time_list[1]])
                    download_info['yesterday_fast_download_number'] = yesterday_fast_game_download_data[
                        'fast_download_number']
                    download_info['yesterday_fast_update_number'] = yesterday_fast_game_download_data[
                        'fast_update_number']

                    # 下载更新量=昨日整日的[下载量+更新量+快玩量]*1% + 今日实时新增的[下载量+更新量+快玩量]
                    game_item['all_download_update_data'] = 0.01 * (download_info['yesterday_download_number'] +
                                                                    download_info['yesterday_update_number'] +
                                                                    download_info['yesterday_fast_download_number'] +
                                                                    download_info['yesterday_fast_update_number']) + (
                                                                    download_info['today_download_number'] +
                                                                    download_info['today_update_number'] +
                                                                    download_info['today_fast_download_number'] +
                                                                    download_info['today_fast_update_number'])

                    game_item[
                        'all_download_info'] = f"昨日_普+快_下载量 & 更新量 ：{download_info['yesterday_download_number']}+{download_info['yesterday_fast_download_number']} & {download_info['yesterday_update_number']}+{download_info['yesterday_fast_update_number']} ;" \
                                               f"今日_普+快_下载量 & 更新量 ：{download_info['today_download_number']}+{download_info['today_fast_download_number']} & {download_info['today_update_number']}+{download_info['today_fast_update_number']}"
                    print(
                        f"\n\n=== {index + 1} ====> {game_item['game_id']}_{game_item['game_name']} 下载更新量:{game_item['all_download_update_data']} \n"
                        f"昨日   普通游戏下载量 & 更新量 ：{download_info['yesterday_download_number']} & {download_info['yesterday_update_number']}\n"
                        f"昨日   快玩游戏下载量 & 更新量 ：{download_info['yesterday_fast_download_number']} & {download_info['yesterday_fast_update_number']}\n"
                        f"今日   普通游戏下载量 & 更新量 ：{download_info['today_download_number']} & {download_info['today_update_number']}\n"
                        f"今日   快玩游戏下载量 & 更新量 ：{download_info['today_fast_download_number']} & {download_info['today_fast_update_number']}\n")

            # 获取时间系数
            for j, single_rank_list in enumerate(all_rank_list):
                print(f"\n\n============ 获取时间系数  {tag_datas[j]['title']}_榜单 ==================")
                for index, game_item in enumerate(single_rank_list):
                    '''
                            > 时间系数：为上架时间系数        
                            >> 上架时间间隔天数X=当前时间-上架时间+1（时间精确到天）；如：5月3日上架，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推        
                            >> 0<X≤1对应的上架时间系数为2        
                            >> 1<X≤2对应的上架时间系数为1.8        
                            >> 2<X≤3对应的上架时间系数为1.5        
                            >> 3<X≤7对应的上架时间系数为1.2        
                            >> X>7对应的上架时间系数为1 
                            >> 当字段为空时，上架时间系数取1    
                    '''
                    time_info = self.get_recent_hot_game_launch_time(game_item['game_id'])
                    _time = 6666
                    game_item['listing_time_str'] = time_info['listing_time_str']
                    if len(time_info['listing_time_str']) == 0:
                        # 上架时间为空时，时间系数取1；
                        _time = 1
                        game_item['_time'] = _time
                        _time_des = "上架时间为空：系数取 1 ；"

                    else:
                        # todo: 上架时间间隔天数X=当前时间-上架时间+1（时间精确到天）；如：5月3日上架，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推
                        now_date_str = datetime.now().strftime("%Y-%m-%d")
                        now_info = datetime.strptime(now_date_str, "%Y-%m-%d")
                        now_timestamp = int(time.mktime(now_info.timetuple()))

                        listing_date_str = time_info['listing_time_str'].split(" ")[0]
                        listing_info = datetime.strptime(listing_date_str, '%Y-%m-%d')
                        listing_timestamp = int(time.mktime(listing_info.timetuple()))

                        X = 1 + (now_timestamp - listing_timestamp) / (24 * 60 * 60)
                        if 0 < X <= 1:
                            _time = 2
                        elif 1 < X <= 2:
                            _time = 1.8
                        elif 2 < X <= 3:
                            _time = 1.5
                        elif 3 < X <= 7:
                            _time = 1.2
                        elif X > 7:
                            _time = 1
                        game_item['_time'] = _time

            # todo：开始计算 排序值 = 下载更新量 * 时间系数 * 评分系数

            for j, single_rank_list in enumerate(all_rank_list):
                print(f"\n\n============ 开始计算  {tag_datas[j]['title']}_榜单 ==================")
                for index, game_item in enumerate(single_rank_list):
                    auto_score = game_item['all_download_update_data'] * game_item['scoring_coefficient'] * game_item[
                        '_time']
                    auto_score = round(auto_score, 2)
                    if "values" not in game_item:
                        print(f"{index} 后台排行榜中未查看该项,auto_score : {auto_score}; {game_item}")
                    else:
                        if float(game_item['values']) == auto_score:
                            print(f"{index} True 数值 score: {auto_score} === {game_item}")
                        else:
                            print(
                                f"{index} False({round(float(game_item['values']) - auto_score, 2)})  数值：{float(game_item['values'])} 、 auto——>{auto_score}   ===>评分系数{game_item['scoring_coefficient']}*时间系数{game_item['_time']} === {game_item}")

        if False:
            print("==================   TEST 新品榜Tab 检测    ==================")
            self.get_refresh_rank("57")
            web_rank_list = self.get_web_category_single_rank("新品榜Tab", type_id="57")  # 前20名
            '''
            算法策略：     
                 > 排序规则：排序值=下载更新量*时间系数*评分系数，依据排序值进行「新品」的自然排序        
                 >> 游戏数量小于150个，按仅有的数量进行排序；游戏数量大于等于150个，只取前150名   
               
                 > 游戏范围：近1月「新上架」的游戏        
                 > 时间系数：为上架时间系数        
                        >> 上架时间间隔天数X=当前时间-上架时间+1（时间精确到天）；如：5月3日上架，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推        
                        >> 0<X≤1对应的上架时间系数为2        
                        >> 1<X≤2对应的上架时间系数为1.8        
                        >> 2<X≤3对应的上架时间系数为1.5        
                        >> 3<X≤7对应的上架时间系数为1.2        
                        >> X>7对应的上架时间系数为1        
                        >> 当字段为空时，上架时间系数取1        
                 > 评分系数：同 近期热门               
                    >> 当“0<=评分<5”时，评分系数为 0.5（“评分=0”指列表数据无评分展示）
                    >> 其余情况，评分系数为1
                 > 下载更新量：基于 今日昨日两天的 [下载量+更新量+快玩量]进行计算（下载更新量 等于后台的“原始值”字段）        
                        >> 下载更新量= 昨日整日的[下载量+更新量+快玩量]*1% + 今日实时新增的[下载量+更新量+快玩量]        
            '''
            app_rank_list = self.get_app_new_rank_list("新品榜")  # 获取评分系数

            # 合并 整合 后台榜单和 app显示榜单 列表 数据 整成一个列表
            for item in app_rank_list:
                for inner_item in web_rank_list:
                    if item['game_id'] == inner_item['game_id']:
                        item['rank'] = inner_item['rank']
                        item['values'] = inner_item['values']

            time_list = self.get_days_time_list(_days=2)
            print(time_list)
            # > 下载更新量：基于 今日昨日两天的 [下载量+更新量+快玩量]进行计算（下载更新量 等于后台的“原始值”字段）
            #   >> 下载更新量 = 昨日整日的[下载量+更新量+快玩量]*1% + 今日实时新增的[下载量+更新量+快玩量]
            for index, game_item in enumerate(app_rank_list):
                game_item['all_download_update_data'] = 0

                download_info = {}
                # 获取 今日 普通游戏   下载量 + 更新量
                game_download_data = self.get_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                 time_list[0:1], None)
                download_info['today_download_number'] = game_download_data['download_number']
                download_info['today_update_number'] = game_download_data['update_number']

                # 获取 今日 快玩游戏   下载量 + 更新量
                fast_game_download_data = self.get_fast_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                           time_list[0:1])
                download_info['today_fast_download_number'] = fast_game_download_data['fast_download_number']
                download_info['today_fast_update_number'] = fast_game_download_data['fast_update_number']

                # 获取 昨日 普通游戏   下载量 + 更新量
                yesterday_game_download_data = self.get_game_download_data(game_item['game_id'],
                                                                           game_item['game_name'],
                                                                           [time_list[1]], None)
                download_info['yesterday_download_number'] = yesterday_game_download_data['download_number']
                download_info['yesterday_update_number'] = yesterday_game_download_data['update_number']

                # # 获取 上周日 快玩游戏   下载量   + 更新量
                yesterday_fast_game_download_data = self.get_fast_game_download_data(game_item['game_id'],
                                                                                     game_item['game_name'],
                                                                                     [time_list[1]])
                download_info['yesterday_fast_download_number'] = yesterday_fast_game_download_data[
                    'fast_download_number']
                download_info['yesterday_fast_update_number'] = yesterday_fast_game_download_data[
                    'fast_update_number']
                # 昨日整日的[下载量 + 更新量 + 快玩量] * 1 % + 今日实时新增的[下载量 + 更新量 + 快玩量]
                game_item[
                    'all_download_info'] = f"昨日_普+快_下载量 & 更新量 ：{download_info['yesterday_download_number']}+{download_info['yesterday_fast_download_number']} & {download_info['yesterday_update_number']}+{download_info['yesterday_fast_update_number']} ;" \
                                           f"今日_普+快_下载量 & 更新量 ：{download_info['today_download_number']}+{download_info['today_fast_download_number']} & {download_info['today_update_number']}+{download_info['today_fast_update_number']}"

                # 下载更新量=昨日整日的[下载量+更新量+快玩量]*1% + 今日实时新增的[下载量+更新量+快玩量]
                game_item['all_download_update_data'] = 0.01 * (download_info['yesterday_download_number'] +
                                                                download_info['yesterday_update_number'] +
                                                                download_info['yesterday_fast_download_number'] +
                                                                download_info['yesterday_fast_update_number']) + (
                                                                download_info['today_download_number'] +
                                                                download_info['today_update_number'] +
                                                                download_info['today_fast_download_number'] +
                                                                download_info['today_fast_update_number'])
                print(
                    f"\n\n=== {index + 1} ====> {game_item['game_id']}_{game_item['game_name']} 下载更新量:{game_item['all_download_update_data']} \n"
                    f"昨日 普通游戏下载量 & 更新量 ：{download_info['yesterday_download_number']} & {download_info['yesterday_update_number']}\n"
                    f"昨日 快玩游戏下载量 & 更新量 ：{download_info['yesterday_fast_download_number']} & {download_info['yesterday_fast_update_number']}\n"
                    f"今日   普通游戏下载量 & 更新量 ：{download_info['today_download_number']} & {download_info['today_update_number']}\n"
                    f"今日   快玩游戏下载量 & 更新量 ：{download_info['today_fast_download_number']} & {download_info['today_fast_update_number']}\n")

            # 获取时间系数
            for index, game_item in enumerate(app_rank_list):
                '''
                        > 时间系数：为上架时间系数        
                        >> 上架时间间隔天数X=当前时间-上架时间+1（时间精确到天）；如：5月3日上架，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推        
                        >> 0<X≤1对应的上架时间系数为2        
                        >> 1<X≤2对应的上架时间系数为1.8        
                        >> 2<X≤3对应的上架时间系数为1.5        
                        >> 3<X≤7对应的上架时间系数为1.2        
                        >> X>7对应的上架时间系数为1 
                        >> 当字段为空时，上架时间系数取1    
                '''
                time_info = self.get_recent_hot_game_launch_time(game_item['game_id'])
                _time = 6666
                if len(time_info['listing_time_str']) == 0:
                    # 上架时间为空时，时间系数取1；
                    _time = 1
                    game_item['_time'] = _time
                    _time_des = "上架时间为空：系数取 1 ；"

                else:
                    # todo: 上架时间间隔天数X=当前时间-上架时间+1（时间精确到天）；如：5月3日上架，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推
                    now_date_str = datetime.now().strftime("%Y-%m-%d")
                    now_info = datetime.strptime(now_date_str, "%Y-%m-%d")
                    now_timestamp = int(time.mktime(now_info.timetuple()))

                    listing_date_str = time_info['listing_time_str'].split(" ")[0]
                    listing_info = datetime.strptime(listing_date_str, '%Y-%m-%d')
                    listing_timestamp = int(time.mktime(listing_info.timetuple()))

                    X = 1 + (now_timestamp - listing_timestamp) / (24 * 60 * 60)
                    if 0 < X <= 1:
                        _time = 2
                    elif 1 < X <= 2:
                        _time = 1.8
                    elif 2 < X <= 3:
                        _time = 1.5
                    elif 3 < X <= 7:
                        _time = 1.2
                    elif X > 7:
                        _time = 1
                    game_item['_time'] = _time

            # todo：开始计算 排序值=下载更新量*时间系数*评分系数
            for index, game_item in enumerate(app_rank_list):
                auto_score = game_item['all_download_update_data'] * game_item['_time'] * game_item[
                    'scoring_coefficient']
                auto_score = round(auto_score, 2)
                if "values" not in game_item:
                    print(f"{index} 后台排行榜中未查看该项,auto_score : {auto_score}; {game_item}")
                else:
                    if float(game_item['values']) == auto_score:
                        print(f"{index} True 数值 score: {auto_score} === {game_item}")
                    else:
                        print(
                            f"{index} False({round(float(game_item['values']) - auto_score, 2)})  数值：{float(game_item['values'])} 、 auto——>{auto_score}   ===>评分系数{game_item['scoring_coefficient']}*时间系数{game_item['_time']} === {game_item}")

        if False:
            print("==================   TEST 长期热门榜Tab 检测    ====== result True ==================")
            '''
               算法策略：        
                 > 游戏范围：所有处于「上架状态」的游戏        
                 > 数据更新：详见需求 数据自动/手动更新规则统一化        
                 > 排序规则：依据「近3个月新增的下载量+更新量+快玩量」进行自然排序，取前150名
            '''
            web_rank_list = self.get_kb_web_rank_data("长期热门榜Tab", rank_type="55")  # 前20名
            self.get_refresh_rank("55")
            time_list = self.get_days_time_list(_days=3 * 30)

            # 获取近 3个月内的 普通游戏（下载量+更新量）及 快玩游戏（下载量+更新量）
            for index, game_item in enumerate(web_rank_list):
                game_item['rank'] = index + 1
                game_item['all_download_update_data'] = 0

                download_info = {}
                # 获取 本周 普通游戏   下载量 + 更新量
                game_download_data = self.get_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                 time_list, None)
                download_info['download_number'] = game_download_data['download_number']
                download_info['update_number'] = game_download_data['update_number']

                # # 获取 本周 快玩游戏   下载量   + 更新量
                fast_game_download_data = self.get_fast_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                           time_list)
                download_info['fast_download_number'] = fast_game_download_data['fast_download_number']
                download_info['fast_update_number'] = fast_game_download_data['fast_update_number']

                # 下载更新量=普通游戏（下载量+更新量）+ 快玩游戏（下载量+更新量）
                game_item['all_download_update_data'] = (download_info['download_number'] +
                                                         download_info['update_number'] +
                                                         download_info['fast_download_number'] +
                                                         download_info['fast_update_number'])

                print(
                    f"\n\n=== {index + 1} ====> {game_item['game_id']}_{game_item['game_name']} 下载更新量:{game_item['all_download_update_data']} \n"
                    f"近3个月（90天） 普通游戏下载量 & 更新量 ：{download_info['download_number']} & {download_info['update_number']}\n"
                    f"近3个月（90天） 快玩游戏下载量 & 更新量 ：{download_info['fast_download_number']} & {download_info['fast_update_number']}\n")

            # 开始校验：
            new_rank = web_rank_list
            # 使用 sorted 函数结合 lambda 函数排序  从大到小排序
            new_rank = sorted(new_rank, key=lambda x: x['all_download_update_data'], reverse=True)

            for index, item in enumerate(web_rank_list):
                if len(item['game_name']) > 5:
                    item['game_name'] = item['game_name'][0:5]
                print(f"\n 排行榜  ==>  {item['game_id']},{item['game_name']}, 数值: {item['values']} ,",
                      end="")

                web_item = new_rank[index]
                if len(web_item['game_name']) > 5:
                    web_item['game_name'] = web_item['game_name'][0:5]
                game_id_des = ""
                values_des = ""
                if item['game_id'] in web_item['game_id']:
                    game_id_des = "游戏ID：True"
                    if "values" in item and "all_download_update_data" in web_item:
                        if float(item['values']) == web_item['all_download_update_data']:
                            values_des = "数值：True"
                        else:
                            values_des = "数值：False"

                print(
                    f"     AUTO ==>  {web_item['game_id']},{web_item['game_name']}, 数值: {web_item['values']} ,{game_id_des},{values_des}")

        if False:
            print("==================   TEST 近期热门榜Tab 检测    ===============================")
            # tag_datas = self.get_app_hot_rank_nav_tab_list()
            # self.get_app_rank_tab_list(tag_datas)
            '''
            > 游戏范围：所有处于「上架状态」的游戏
            > 排序规则：排序值=下载更新量*时间系数*评分系数，依据排序值进行「近期热门」的自然排序，取前150名（排序值 等于 后台的“数值”字段）
            > 下载更新量：基于本周新增的[下载量+更新量+快玩量]进行计算（下载更新量 等于后台的“原始值”字段）
                   >> 下载更新量=上周日新增的[下载量+更新量+快玩量]*1%+本周新增的[下载量+更新量+快玩量]
            > 时间系数：分为上架时间系数和更新时间系数，「新上架游戏」对应“上架时间系数”，「新更新游戏」对应“更新时间系数”
                    >> 系数类型 判断规则：
                             >>> 当「版本最新时间<=上架时间」时，该款游戏视为「新上架游戏」，执行「上架时间系数」逻辑
                             >>> 当「版本最新时间>上架时间」时，该款游戏视为「新更新游戏」，执行「更新时间系数」逻辑
                    >> 上架时间系数：基于上架时间间隔天数，判断对应的上架时间系数
                             >>> 上架时间间隔天数X=当前时间-上架时间+1（时间精确到天）；如：5月3日上架，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推
                             >>> 0<X≤1对应的上架时间系数为2
                             >>> 1<X≤2对应的上架时间系数为1.8
                             >>> 2<X≤3对应的上架时间系数为1.5
                             >>> 3<X≤7对应的上架时间系数为1.2
                             >>> X>7对应的上架时间系数为1
                    >> 更新时间系数：基于更新时间间隔天数，判断对应的更新时间系数
                             >>> 更新时间间隔天数X=当前时间-版本最新时间+1（时间精确到天）；如：5月3日为更新时间，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推
                             >>> 0<X≤1对应的更新时间系数为2
                             >>> 1<X≤2对应的更新时间系数为1.8
                             >>> 2<X≤3对应的更新时间系数为1.5
                             >>> 3<X≤7对应的更新时间系数为1.2
                             >>> X>7对应的上架时间系数为1
                    >> 上架时间与版本更新时间两个字段同时为空时，时间系数取1；仅上架时间字段不为空，执行「上架时间系数」逻辑；仅版本更新时间字段不为空，执行「更新时间系数」逻辑；
            > 评分系数：
                    >> 当“0<=评分<5”时，评分系数为 0.5（“评分=0”指列表数据无评分展示）
                    >> 其余情况，评分系数为1
             '''

            self.get_refresh_rank("56")
            web_rank_list = self.get_web_category_single_rank("近期热门榜", type_id="56")  # 前20名
            app_rank_list = self.get_app_rank_list("app近期热门榜")

            # 合并 整合 后台榜单和 app显示榜单 列表 数据 整成一个列表
            for item in app_rank_list:
                for inner_item in web_rank_list:
                    if item['game_id'] == inner_item['game_id']:
                        item['rank'] = inner_item['rank']
                        item['values'] = inner_item['values']

            # 调用函数并打印结果
            # 获取上周日 日期
            last_sunday_str = self.get_last_sunday_str()

            time_list = self.get_weekday_str()
            # 获取 本周 至  今天日期
            print(time_list)
            # > 下载更新量：基于本周新增的[下载量+更新量+快玩量]进行计算（下载更新量 等于后台的“原始值”字段）
            #   >> 下载更新量=上周日新增的[下载量+更新量+快玩量]*1%+本周新增的[下载量+更新量+快玩量]
            for index, game_item in enumerate(app_rank_list):
                game_item['all_download_update_data'] = 0

                download_info = {}
                # 获取 本周 普通游戏   下载量 + 更新量
                game_download_data = self.get_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                 time_list, None)
                download_info['download_number'] = game_download_data['download_number']
                download_info['update_number'] = game_download_data['update_number']

                # # 获取 本周 快玩游戏   下载量   + 更新量
                fast_game_download_data = self.get_fast_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                           time_list)
                download_info['fast_download_number'] = fast_game_download_data['fast_download_number']
                download_info['fast_update_number'] = fast_game_download_data['fast_update_number']

                print()
                # 获取 上周日 普通游戏   下载量 + 更新量
                last_sunday_game_download_data = self.get_game_download_data(game_item['game_id'],
                                                                             game_item['game_name'],
                                                                             [last_sunday_str], None)
                download_info['last_sunday_download_number'] = last_sunday_game_download_data['download_number']
                download_info['last_sunday_update_number'] = last_sunday_game_download_data['update_number']

                # # 获取 上周日 快玩游戏   下载量   + 更新量
                last_sunday_fast_game_download_data = self.get_fast_game_download_data(game_item['game_id'],
                                                                                       game_item['game_name'],
                                                                                       [last_sunday_str])
                download_info['last_sunday_fast_download_number'] = last_sunday_fast_game_download_data[
                    'fast_download_number']
                download_info['last_sunday_fast_update_number'] = last_sunday_fast_game_download_data[
                    'fast_update_number']

                # 下载更新量=上周日新增的[下载量+更新量+快玩量]*1%+本周新增的[下载量+更新量+快玩量]
                game_item['all_download_update_data'] = 0.01 * (download_info['last_sunday_download_number'] +
                                                                download_info['last_sunday_update_number'] +
                                                                download_info['last_sunday_fast_download_number'] +
                                                                download_info['last_sunday_fast_update_number']) + (
                                                                download_info['download_number'] +
                                                                download_info['update_number'] +
                                                                download_info['fast_download_number'] +
                                                                download_info['fast_update_number'])

                print(
                    f"\n\n=== {index + 1} ====> {game_item['game_id']}_{game_item['game_name']} 下载更新量:{game_item['all_download_update_data']} \n"
                    f"上周日 普通游戏下载量 & 更新量 ：{download_info['last_sunday_download_number']} & {download_info['last_sunday_update_number']}\n"
                    f"上周日 快玩游戏下载量 & 更新量 ：{download_info['last_sunday_fast_download_number']} & {download_info['last_sunday_fast_update_number']}\n"
                    f"本周   普通游戏下载量 & 更新量 ：{download_info['download_number']} & {download_info['update_number']}\n"
                    f"本周   快玩游戏下载量 & 更新量 ：{download_info['fast_download_number']} & {download_info['fast_update_number']}\n")

            # 获取时间系数
            for index, game_item in enumerate(app_rank_list):
                #     ['version_update_time']   ['version_update_str']
                #     ['listing_time']          ['listing_time_str']
                time_info = self.get_recent_hot_game_launch_time(game_item['game_id'])
                _time = 6666
                _time_des = ""
                time_type = 0
                if len(time_info['version_update_str']) == 0 and len(time_info['listing_time_str']) == 0:
                    # 上架时间与版本更新时间两个字段同时为空时，时间系数取1；
                    _time = 1
                    game_item['_time'] = _time
                    _time_des = "上架&版本更新 为空"

                elif len(time_info['listing_time_str']) > 0 and len(time_info['version_update_str']) == 0:
                    time_type = 1
                    _time_des = "仅架时间字段 不为空，执行「上架时间系数」逻辑"

                elif len(time_info['version_update_str']) > 0 and len(time_info['listing_time_str']) == 0:
                    time_type = 2
                    _time_des = "版本更新时间字段 不为空，执行「更新时间系数」逻辑"

                # >> > 当「版本最新时间 <= 上架时间」时，该款游戏视为「新上架游戏」，执行「上架时间系数」逻辑
                # >> > 当「版本最新时间 > 上架时间」时，该款游戏视为「新更新游戏」，执行「更新时间系数」逻辑
                elif time_info['version_update_time'] <= time_info['listing_time']:
                    time_type = 1
                    _time_des = "版本最新时间 <= 上架时间，执行「上架时间系数」逻辑"

                else:
                    time_type = 2
                    _time_des = "版本最新时间 > 上架时间，执行「更新时间系数」逻辑"

                if time_type == 1:
                    # 执行「上架时间系数」逻辑
                    # todo: 上架时间间隔天数X=当前时间-上架时间+1（时间精确到天）；如：5月3日上架，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推
                    now_date_str = datetime.now().strftime("%Y-%m-%d")
                    now_info = datetime.strptime(now_date_str, "%Y-%m-%d")
                    now_timestamp = int(time.mktime(now_info.timetuple()))

                    listing_date_str = time_info['listing_time_str'].split(" ")[0]
                    listing_info = datetime.strptime(listing_date_str, '%Y-%m-%d')
                    listing_timestamp = int(time.mktime(listing_info.timetuple()))

                    X = 1 + (now_timestamp - listing_timestamp) / (24 * 60 * 60)
                    if 0 < X <= 1:
                        _time = 2
                    elif 1 < X <= 2:
                        _time = 1.8
                    elif 2 < X <= 3:
                        _time = 1.5
                    elif 3 < X <= 7:
                        _time = 1.2
                    elif X > 7:
                        _time = 1
                    game_item['_time'] = _time
                    '''
                    >> 上架时间系数：基于上架时间间隔天数，判断对应的上架时间系数
                             >>>                              
                             >>> 0<X≤1对应的上架时间系数为2
                             >>> 1<X≤2对应的上架时间系数为1.8
                             >>> 2<X≤3对应的上架时间系数为1.5
                             >>> 3<X≤7对应的上架时间系数为1.2
                             >>> X>7对应的上架时间系数为1
                    '''

                elif time_type == 2:
                    # 更新时间系数 ['version_update_time']
                    now_date_str = datetime.now().strftime("%Y-%m-%d")
                    now_info = datetime.strptime(now_date_str, "%Y-%m-%d")
                    now_timestamp = int(time.mktime(now_info.timetuple()))

                    listing_date_str = time_info['version_update_str'].split(" ")[0]
                    listing_info = datetime.strptime(listing_date_str, '%Y-%m-%d')
                    listing_timestamp = int(time.mktime(listing_info.timetuple()))

                    X = 1 + (now_timestamp - listing_timestamp) / (24 * 60 * 60)
                    if 0 < X <= 1:
                        _time = 2
                    elif 1 < X <= 2:
                        _time = 1.8
                    elif 2 < X <= 3:
                        _time = 1.5
                    elif 3 < X <= 7:
                        _time = 1.2
                    elif X > 7:
                        _time = 1
                    game_item['_time'] = _time
                    '''
                      >> 更新时间系数：基于更新时间间隔天数，判断对应的更新时间系数
                             >>> 更新时间间隔天数X=当前时间-版本最新时间+1（时间精确到天）；如：5月3日为更新时间，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推
                             >>> 0<X≤1对应的更新时间系数为2
                             >>> 1<X≤2对应的更新时间系数为1.8
                             >>> 2<X≤3对应的更新时间系数为1.5
                             >>> 3<X≤7对应的更新时间系数为1.2
                             >>> X>7对应的上架时间系数为1
                    '''

            # todo：开始计算 排序值=下载更新量*时间系数*评分系数
            for index, game_item in enumerate(app_rank_list):
                auto_score = game_item['all_download_update_data'] * game_item['_time'] * game_item[
                    'scoring_coefficient']
                auto_score = round(auto_score, 2)
                if "values" not in game_item:
                    print(f"后台排行榜中未查看该项,auto_score : {auto_score}; {game_item}")
                else:
                    # if float(game_item['values']) == auto_score:
                    #     print(f"True score: {auto_score} === {game_item}")
                    # else:
                    #     print(f"False  {float(game_item['values'])} 、 auto——>{auto_score}  === {game_item}")
                    if float(game_item['values']) == auto_score:
                        print(f"{index} True 数值 score: {auto_score} === {game_item}")
                    else:
                        print(
                            f"{index} False({round(float(game_item['values']) - auto_score, 2)})  数值：{float(game_item['values'])} 、 auto——>{auto_score}   ===>评分系数{game_item['scoring_coefficient']}*时间系数{game_item['_time']} === {game_item}")

        if False:
            # todo: 获取 后台 预约榜单  type = 54
            print("==================   获取后台 预约榜单 自然排序数据 检测 ===============================\n")
            web_rank_list = self.get_kb_web_rank_data("预约榜单", rank_type="54")[:50]  # 前50名
            time_list = self.get_days_time_list(_days=2)
            # todo:  排序规则： 排序值 = 预约量 * 事件时间系数 * 重要程度系数（ 排序值 等于 后台的“数值”字段）
            for index, rank_item in enumerate(web_rank_list):
                pre_appointment_number_list = self.get_pre_data(rank_item['game_name'], rank_item['game_id'], time_list)
                print(f"今日：{pre_appointment_number_list[0]}  ； 昨日:{pre_appointment_number_list[1]}")  # [今天，昨天....]
                # 预约量=昨日总预约量的1%+今日实时新增的预约量
                rank_item['pre_appointment_number'] = pre_appointment_number_list[1] * 0.01 + \
                                                      pre_appointment_number_list[0]
                # 获取  事件时间系数
                game_detail_data = self.get_game_event_time(rank_item['game_id'], 3)
                # ['事件时间系数', '重要程度系数', '采用那种算法', "最早游戏事件时间", "游戏事件最新时间"]
                rank_item['X'] = game_detail_data[0]
                rank_item['number'] = game_detail_data[1]
                rank_item['type'] = game_detail_data[2]
                rank_item['first_time'] = game_detail_data[3]
                rank_item['game_event_time'] = game_detail_data[4]

                auto_result_score = rank_item['pre_appointment_number'] * rank_item['X'] * rank_item['number']

                # 四舍五入并保留小数点后一位
                auto_result_score = round(auto_result_score, 2)

                rank_item['auto_result_score'] = auto_result_score

                if float(rank_item['values']) == auto_result_score:
                    print(
                        f"======{str(index + 1)} == True   {rank_item['game_name']}_{rank_item['game_id']} 检测正常 排序值数：  {rank_item['values']}     == {auto_result_score}  \n")
                else:
                    print(
                        f"======{str(index + 1)}== False  {rank_item['game_name']}_{rank_item['game_id']} 检测异常 排序值数： 后台-> {rank_item['values']}   auto——>{rank_item['auto_result_score']}   \n")
            print(web_rank_list)

        if False:
            # todo: 获取 后台 琳琅榜 type = 52
            print("==================   获取后台 琳琅榜榜单 自然排序数据 检测 ===============================\n")
            web_rank_list = self.get_kb_web_rank_data("琳琅榜榜单", rank_type="52")
            time_list = self.get_days_time_list(_days=7)
            '''
             游戏范围：所有处于「上架状态」且有「星探团标签」的游戏
                > 排序规则：排序值=评分*（近七天下载量+更新量+快玩量）*时间系数*评分飙升系数，依据排序值进行「琳琅榜」的自然排序，取前150名
                >> 近七天下载量+更新量+快玩量 等于后台的“原始值”字段，排序值 等于 后台的“数值”字段
                
            new_version  01/03
                排序规则：排序值=（近七天下载量+更新量+快玩下载量+快玩更新量）*平均评分系数*时间系数*评分飙升系数，依据排序值进行「琳琅榜」的自然排序，取前150名（有修改）
                    > 近七天下载量+更新量+快玩下载量+快玩更新量 等于后台的“原始值”字段，排序值 等于 后台的“数值”字段
                    > 平均评分系数：先计算出「平均评分」，基于「平均评分」执行“平均评分系数”逻辑（有修改）                             
            '''
            # 获取 app琳琅榜单
            app_linlang_rank_list = self.get_app_linlang_rank_tab_list()
            # 爬取后他 安卓游戏后台第二版本 获取 该游戏 上架了哪几种 （普 云 快 小）
            for item in app_linlang_rank_list:
                item['status'] = self.get_web_game_detail(item['game_id'])

            # todo： > 评分飙升系数：若游戏「近7天评分-当前评分≥1分」，则评分飙升系数为3；否则，评分飙升系数为1
            for item in app_linlang_rank_list:
                # todo: # 获取评分 需要从 APP游戏详情页中获取 评分、近七天评分、最近评分
                item['score_data'] = self.get_app_game_detail_data(item['game_type'], item['game_id'], item['status'])

                # 近7天评分-当前评分
                if float(item['score_data']['7_star']) - float(item['score_data']['c_all_star']) >= 1:
                    item['score_multiple'] = 3
                else:
                    item['score_multiple'] = 1
                print(f" 评分飙升系数 : {item['score_multiple']}")

                # 合并 整合 后台榜单和 app显示榜单 列表 数据 整成一个列表
            for item in app_linlang_rank_list:
                for inner_item in web_rank_list:
                    if item['game_id'] == inner_item['game_id']:
                        item['rank'] = inner_item['rank']
                        item['values'] = inner_item['values']

            # 获取时间系数：
            for item in app_linlang_rank_list:
                # item_data['listing_time'] = time_arrays[0]
                # item_data['listing_time_str'] = time_arrays[1]
                # item_data['Y'] = 0
                item['time'] = self.get_game_launch_time(item['game_id'])
                print(item['time'])

            for index, game_item in enumerate(app_linlang_rank_list):
                # 获取 普通游戏 近七天  下载量 + 更新量
                game_download_data = self.get_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                 time_list, game_item['game_type'])
                game_item['download_number'] = game_download_data['download_number']
                game_item['update_number'] = game_download_data['update_number']
                # game_item['fast_download_number'] = game_download_data['fast_download_number']   fast_download_number 值不准

                # # 获取 快玩游戏 近七天  下载量     ///+ 更新量
                fast_game_download_data = self.get_fast_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                           time_list)
                game_item['fast_download_number'] = fast_game_download_data['fast_download_number']
                game_item['fast_update_number'] = fast_game_download_data['fast_update_number']

                game_item['download_data'] = game_item['download_number'] + game_item['update_number'] + game_item[
                    'fast_download_number'] + game_item['fast_update_number']  # 1200 12000

                # todo:排序值 = 评分 *（近七天下载量 + 更新量 + 快玩量）*时间系数 * 评分飙升系数
                auto_result_score = game_item['score_multiple'] * float(game_item['score_data']['c_all_star']) * \
                                    game_item['download_data'] * game_item['time']['Y']

                # 四舍五入并保留小数点后一位
                auto_result_score = round(auto_result_score, 2)
                game_item['auto_result_score'] = auto_result_score

            print("\n\n=================  开始验证 琳琅榜单  ======================\n")
            for index, game_item in enumerate(app_linlang_rank_list):
                if 'values' in game_item:
                    aaaaa = game_item['values']
                    auto_result_score = game_item['auto_result_score']
                    print(aaaaa, auto_result_score, game_item)
                    if float(game_item['values']) == game_item['auto_result_score']:
                        print(
                            f"==== {str(index + 1)} ==== True   {game_item['game_name']}_{game_item['game_id']} 检测正常 排序值数：  {game_item['values']}  \n")
                    else:
                        print(
                            f"==== {str(index + 1)} ==== False  {game_item['game_name']}_{game_item['game_id']} 检测异常 排序值数： 后台-> {game_item['values']}   auto——>{game_item['auto_result_score']}   \n")
                else:
                    print(
                        f"==== {str(index + 1)} ========= False 可能是 锁定 {game_item['game_name']}_{game_item['game_id']}")

        if False:
            # todo: 获取 后台 热销榜 type = 53
            print("==================   获取后台 热销榜 自然排序数据 检测 ===============================\n")

            ''' > 排序规则：排序值=近7天订单成交量*时间系数*折扣系数，依据排序值进行「热销榜」的自然排序（排序值 等于 后台的“数值”字段，近7天订单成交量 等于后台的“原始值”字段）
                >> 例如：今日为10月7日，则需近7天为「10月1日-10月7日」
                
            > 时间系数：为上架时间系数
            > 折扣系数：当游戏出现「史低 或 新史低 或 普通折扣」的标签时，折扣系数为3；否则，折扣系数为1            
            
            '''
            # 获取app 接口  获取折扣系数 discount
            app_rank_list = self.get_app_hot_sell_rank_tab_list()
            # 后台
            web_rank_list = self.get_kb_web_rank_data("热销榜", rank_type="53")
            time_list = self.get_days_time_list(_days=7)

            # 合并 整合 后台榜单和 app显示榜单 列表 数据 整成一个列表
            for item in app_rank_list:
                for inner_item in web_rank_list:
                    if item['game_id'] == inner_item['game_id']:
                        item['rank'] = inner_item['rank']
                        item['values'] = inner_item['values']

            # 获取 近七天订单量
            for item in app_rank_list:
                if self.dev:
                    item['order'] = self.get_game_order_data(item['game_id'], item['game_name'], time_list[6])
                else:
                    item['order'] = self.get_web_single_rank(item['game_id'], item["game_name"], '热销榜', "53")

            # 时间系数：为上架时间系数
            for item in app_rank_list:
                item['time'] = self.get_hot_sell_game_launch_time(item["game_id"])

            # 排序值 = 近7天订单成交量 * 时间系数 * 折扣系数，
            print(app_rank_list)
            for index, game_item in enumerate(app_rank_list):
                auto_result_score = game_item['order'] * game_item['time']['Y'] * game_item['discount']
                # 四舍五入并保留小数点后一位
                auto_result_score = round(auto_result_score, 2)
                game_item['auto_result_score'] = auto_result_score

            print("\n\n=================  开始验证 热销榜单  ======================\n")
            for index, game_item in enumerate(app_rank_list):
                if 'values' in game_item:
                    aaaaa = game_item['values']
                    auto_result_score = game_item['auto_result_score']
                    print(aaaaa, auto_result_score, game_item)
                    if float(game_item['values']) == game_item['auto_result_score']:
                        print(
                            f"==== {str(index + 1)} ==== True   {game_item['game_name']}_{game_item['game_id']} 检测正常 排序值数：  {game_item['values']}  \n")
                    else:
                        print(
                            f"==== {str(index + 1)} ==== False  {game_item['game_name']}_{game_item['game_id']} 检测异常 排序值数： 后台-> {game_item['values']}   auto——>{game_item['auto_result_score']}   \n")
                else:
                    print(
                        f"==== {str(index + 1)} ========= False 可能是 锁定 {game_item['game_name']}_{game_item['game_id']}")

        if False:
            # todo: 获取 后台 在线玩 --小游戏V2 type = 18
            print("小游戏V2榜单\n")
            self.get_refresh_rank("18")

            # 后台
            web_rank_list = self.get_kb_web_rank_data("小游戏V2榜单", rank_type="18")
            # 获取 小游戏 统计页面 启动次数排行
            time_list = self.get_days_time_list(_days=4)
            # todo: 小游戏统计页面
            web_statistics_rank_list = self.get_web_mini_game_list(time_list)

            # 使用 sorted 函数结合 lambda 函数排序
            web_statistics_rank_list = sorted(web_statistics_rank_list, key=lambda x: x['values'], reverse=True)

            if len(web_rank_list) > len(web_statistics_rank_list):
                for index, item in enumerate(web_rank_list):
                    if len(item['game_name']) > 5:
                        item['game_name'] = item['game_name'][0:5]
                    print(f"\n 排行榜  ==>  {item['game_id']},{item['game_name']}, 启动次数: {item['values']} ,",
                          end="")
                    if index + 1 <= len(web_statistics_rank_list):
                        web_item = web_statistics_rank_list[index]
                        if len(web_item['game_name']) > 5:
                            web_item['game_name'] = web_item['game_name'][0:5]

                        game_id_des = ""
                        values_des = ""
                        if item['game_id'] in web_item['game_id']:
                            game_id_des = "游戏ID：True"
                            if "values" in item and "values" in web_item:
                                if float(item['values']) == web_item['values']:
                                    values_des = "启动次数：True"
                                else:
                                    values_des = "启动次数：False"
                        else:
                            game_id_des = "游戏ID：False"
                        print(
                            f"     统计 ==>  {web_item['game_id']},{web_item['game_name']}, 启动次数: {web_item['values']} ,{game_id_des},{values_des}")
            else:
                for index, item in enumerate(web_statistics_rank_list):
                    if len(item['game_name']) > 5:
                        item['game_name'] = item['game_name'][0:5]
                    print(f"\n 统计  ==>  {item['game_id']},{item['game_name']}, 启动次数: {item['values']},", end="")
                    if index + 1 <= len(web_rank_list):
                        web_item = web_rank_list[index]
                        if len(web_item['game_name']) > 5:
                            web_item['game_name'] = web_item['game_name'][0:5]

                        game_id_des = ""
                        values_des = ""
                        if item['game_id'] in web_item['game_id']:
                            game_id_des = "游戏ID：True"
                            if "values" in item and "values" in web_item:
                                if float(item['values']) == web_item['values']:
                                    values_des = "启动次数：True"
                                else:
                                    values_des = "启动次数：False"
                        else:
                            game_id_des = "游戏ID：False"
                        print(
                            f"     排行榜 ==>  {web_item['game_id']},{web_item['game_name']}, 启动次数: {web_item['values']},{game_id_des},{values_des}")

        if False:
            # todo: 获取 后台 在线玩 --快玩 V2 type = 16
            print("\n\n--快玩V2榜单\n")
            self.get_refresh_rank("16")
            # 后台
            web_rank_list = self.get_kb_web_rank_data("快玩V2榜单", rank_type="16")
            # 获取 快玩 统计页面 启动次数排行
            time_list = self.get_days_time_list(_days=4)
            # todo:
            # 进行对比：
            web_statistics_rank_list = self.get_web_fast_game_list(time_list)
            # 使用 sorted 函数结合 lambda 函数排序
            web_statistics_rank_list = sorted(web_statistics_rank_list, key=lambda x: x['values'], reverse=True)
            if len(web_rank_list) > len(web_statistics_rank_list):
                for index, item in enumerate(web_rank_list):
                    if len(item['game_name']) > 5:
                        item['game_name'] = item['game_name'][0:5]
                    print(f"\n 排行榜  ==>  {item['game_id']},{item['game_name']}, 启动次数: {item['values']},", end="")
                    if index + 1 <= len(web_statistics_rank_list):
                        web_item = web_statistics_rank_list[index]
                        if len(web_item['game_name']) > 5:
                            web_item['game_name'] = web_item['game_name'][0:5]
                        game_id_des = ""
                        values_des = ""
                        if item['game_id'] in web_item['game_id']:
                            game_id_des = "游戏ID：True"
                            if "values" in item and "values" in web_item:
                                if float(item['values']) == web_item['values']:
                                    values_des = "启动次数：True"
                                else:
                                    values_des = "启动次数：False"
                        else:
                            game_id_des = "游戏ID：False"
                        print(
                            f"     统计 ==>  {web_item['game_id']},{web_item['game_name']}, 启动次数: {web_item['values']},{game_id_des},{values_des}")
            else:
                for index, item in enumerate(web_statistics_rank_list):
                    if len(item['game_name']) > 5:
                        item['game_name'] = item['game_name'][0:5]
                    print(f"\n 统计  ==>  {item['game_id']},{item['game_name']}, 启动次数: {item['values']},", end="")
                    if index + 1 <= len(web_rank_list):
                        web_item = web_rank_list[index]
                        if len(web_item['game_name']) > 5:
                            web_item['game_name'] = web_item['game_name'][0:5]
                        game_id_des = ""
                        values_des = ""
                        if item['game_id'] in web_item['game_id']:
                            game_id_des = "游戏ID：True"
                            if "values" in item and "values" in web_item:
                                if float(item['values']) == web_item['values']:
                                    values_des = "启动次数：True"
                                else:
                                    values_des = "启动次数：False"
                        else:
                            game_id_des = "游戏ID：False"
                        print(
                            f"     排行榜 ==>  {web_item['game_id']},{web_item['game_name']}, 启动次数: {web_item['values']},{game_id_des},{values_des}")

        if False:
            # todo: 获取 后台 在线玩 --云游戏V2 type = 17
            print("\n\n-云游戏V2榜单=\n")
            self.get_refresh_rank("17")
            # 后台
            web_rank_list = self.get_kb_web_rank_data("云游戏V2榜单", rank_type="17")
            # 获取 云游戏 统计页面 启动次数排行
            time_list = self.get_days_time_list(_days=4)
            # todo:
            # 进行对比
            web_statistics_rank_list = self.get_web_cloud_game_list(time_list)
            # 使用 sorted 函数结合 lambda 函数排序
            web_statistics_rank_list = sorted(web_statistics_rank_list, key=lambda x: x['values'], reverse=True)
            if len(web_rank_list) > len(web_statistics_rank_list):
                for index, item in enumerate(web_rank_list):
                    if len(item['game_name']) > 5:
                        item['game_name'] = item['game_name'][0:5]
                    print(f"\n 排行榜  ==>  {item['game_id']},{item['game_name']}, 启动次数: {item['values']},", end="")
                    if index + 1 <= len(web_statistics_rank_list):
                        web_item = web_statistics_rank_list[index]
                        if len(web_item['game_name']) > 5:
                            web_item['game_name'] = web_item['game_name'][0:5]
                        game_id_des = ""
                        values_des = ""
                        if item['game_id'] in web_item['game_id']:
                            game_id_des = "游戏ID：True"
                            if "values" in item and "values" in web_item:
                                if float(item['values']) == web_item['values']:
                                    values_des = "启动次数：True"
                                else:
                                    values_des = "启动次数：False"
                        else:
                            game_id_des = "游戏ID：False"
                        print(
                            f"     统计 ==>  {web_item['game_id']},{web_item['game_name']}, 启动次数: {web_item['values']},{game_id_des},{values_des}")
            else:
                for index, item in enumerate(web_statistics_rank_list):
                    if len(item['game_name']) > 5:
                        item['game_name'] = item['game_name'][0:5]
                    print(f"\n 统计  ==>  {item['game_id']},{item['game_name']}, 启动次数: {item['values']},", end="")
                    if index + 1 <= len(web_rank_list):
                        web_item = web_rank_list[index]
                        if len(web_item['game_name']) > 5:
                            web_item['game_name'] = web_item['game_name'][0:5]
                        game_id_des = ""
                        values_des = ""
                        if item['game_id'] in web_item['game_id']:
                            game_id_des = "游戏ID：True"
                            if "values" in item and "values" in web_item:
                                if float(item['values']) == web_item['values']:
                                    values_des = "启动次数：True"
                                else:
                                    values_des = "启动次数：False"
                        else:
                            game_id_des = "游戏ID：False"
                        print(
                            f"     排行榜 ==>  {web_item['game_id']},{web_item['game_name']}, 启动次数: {web_item['values']},{game_id_des},{values_des}")

        if False:
            # todo: 获取 后台 独家榜 type = 19
            # todo:小游戏情况 不管  之前独家是没有 快、云、小
            print("==================   获取后台 独家榜 自然排序数据 检测 ===============================\n")
            '''
                
                独家关注分 = 状态权重系数 * 时间权重系数 * 基础分
                
                游戏状态      上架      预约      普通付费      限免/折扣
                状态权重系数   1.0      1.0       1.1         1.15
                
                >基础分 = 除昨天外前5日 下载预约量 + 2*昨天下载预约量 + 3*今日下载预约量
                    >下载预约量 包括下载量（含快玩下载）、更新量及预约量，取不到对应值时默认为0
                
                >时间权重系数: 分为 预热时间系数、上架时间系数和更新时间系数，判断当前时间与不同状态对应时间的差值，
                    依据差值X选取对应系数参与计算，X=当前时间-Y
                    >>概念说明：
                    
                    ①预热游戏：Y取游戏事件最新日期，该字段为空时取版本更新时间，两个字段均为空时系数取1.0
                            X       X＜0     0≤X≤1天      1天＜X＜7天     X≥七天
                        预热时间系数   1.0       1.3          1.15         1.0                        
                        
                    ②新上架游戏：上架时间 ≥版本更新时间-3day，Y取上架时间，两个字段任一为空时
                            X       X＜0     0≤X≤1天      1天＜X≤3天     3天＜X＜7天     X≥七天
                        上架时间系数   1.0       3.5          2.0           1.45         1.0
                        
                    ③新更新游戏：上架时间＜版本更新时间-3day，Y取版本更新时间
                            X       X＜0     0≤X≤1天      1天＜X＜7天     X≥七天
                        更新时间系数   1.0       1.3          1.15         1.0 
                    
                >>兜底策略：（20240815补充）
                    ①：游戏事件最新日期为空时，Y取版本更新时间，两个字段均为空时系数取1.0
                    ②&③：上架时间与版本更新时间两个字段任一为空时，系数取1.0
                
                >>字段来源：取快爆后台-该游戏编辑页
                    （1）基础信息-版本更新时间或上架时间
                    （2）游戏补充信息-游戏事件最新日期
            '''
            self.get_refresh_rank("19")
            # 获取APP 独家列表 + 游戏状态权重系数 + 过滤掉 云、快、小游戏
            dujia_rank_list = self.get_app_exclusive_rank_tab_list()[:30]

            # # 爬取后台 获取游戏状态
            # for item in dujia_rank_list:
            #     self.get_web_game_detail_status(item['game_id'])

            web_rank_list = self.get_kb_web_rank_data("独家榜", rank_type="19")

            # 合并 整合 后台榜单和 app显示榜单 列表 数据 整成一个列表
            for item in dujia_rank_list:
                for inner_item in web_rank_list:
                    if item['game_id'] == inner_item['game_id']:
                        item['rank'] = inner_item['rank']
                        item['values'] = inner_item['values']

            # 获取基础分  >基础分 = 除昨天外前5日 下载预约量 + 2*昨天下载预约量 + 3*今日下载预约量
            #               >下载预约量 包括下载量（含快玩下载）、更新量及预约量，取不到对应值时默认为0
            time_list = self.get_days_time_list(_days=7)

            # 获取 近7日内 预约量
            for index, item in enumerate(dujia_rank_list):
                if '状态：预约(预热)' in item['discount_status_des']:
                    pre_appointment_number_list = self.get_pre_data(item['game_name'], item['game_id'], time_list)
                    item['pre_appointment_number_list'] = pre_appointment_number_list
                    print(f"预约量--->今日：{pre_appointment_number_list[0]}  ； 昨日:{pre_appointment_number_list[1]} ;"
                          f"除昨天外前5日: {pre_appointment_number_list[2:]}")  # [今天，昨天....]
                else:
                    item['pre_appointment_number_list'] = [0, 0, 0, 0, 0, 0, 0]

            for index, game_item in enumerate(dujia_rank_list):
                print()
                # todo:获取 除昨天外前5日 下载量     （普通）
                game_download_data = self.get_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                 time_list[2:], game_item['game_type'])
                game_item['normal_5_download_number'] = game_download_data['download_number']
                game_item['normal_5_update_number'] = game_download_data['update_number']

                # 获取 除昨天外前5日 下载量  + 更新量  (快玩)
                fast_game_download_data = self.get_fast_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                           time_list[2:])
                # game_item['fast_5_download_number'] = fast_game_download_data['fast_download_number']
                # game_item['fast_5_update_number'] = fast_game_download_data['fast_update_number']

                # todo: 获取 昨天下载预约量  下载量  + 更新量    （普通）
                game_download_data_1 = self.get_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                   time_list[1:2], game_item['game_type'])
                # game_item['normal_1_download_number'] = game_download_data_1['download_number']
                # game_item['normal_1_update_number'] = game_download_data_1['update_number']

                # 获取 昨天下载预约量  下载量  + 更新量    （ 快）
                fast_game_download_data_1 = self.get_fast_game_download_data(game_item['game_id'],
                                                                             game_item['game_name'],
                                                                             time_list[1:2])
                # game_item['fast_1_download_number'] = fast_game_download_data_1['fast_download_number']
                # game_item['fast_1_update_number'] = fast_game_download_data_1['fast_update_number']

                # todo:获取 今日下载预约量  下载量  + 更新量    （普通）  注释
                # game_download_data_0 = self.get_game_download_data(game_item['game_id'], game_item['game_name'],
                #                                                    time_list[0:1], game_item['game_type'])
                # game_item['normal_0_download_number'] = game_download_data_0['download_number']
                # game_item['normal_0_update_number'] = game_download_data_0['update_number']

                today_normal_all_download_number = \
                    self.get_web_download_detail_datas(time_list[0:1], game_item['game_id'],
                                                       game_item['game_name'])[0]

                today_normal_all_update_number = self.get_web_update_detail_datas(time_list[0:1], game_item['game_id'],
                                                                                  game_item['game_name'])[0]

                # 获取 今日下载预约量  下载量  + 更新量    （ 快）
                fast_game_download_data_0 = self.get_fast_game_download_data(game_item['game_id'],
                                                                             game_item['game_name'],
                                                                             time_list[0:1])
                # game_item['fast_0_download_number'] = fast_game_download_data_0['fast_download_number']
                # game_item['fast_0_update_number'] = fast_game_download_data_0['fast_update_number']

                # 基础分 = 除昨天外前5日 下载预约量 + 2*昨天下载预约量 + 3*今日下载预约量 score
                if '预热' in game_item['discount_status_des']:
                    game_item['base_score'] = (game_item['pre_appointment_number_list'][2] +
                                               game_item['pre_appointment_number_list'][3] +
                                               game_item['pre_appointment_number_list'][4] +
                                               game_item['pre_appointment_number_list'][5] +
                                               game_item['pre_appointment_number_list'][6]) + 2 * \
                                              game_item['pre_appointment_number_list'][1] + 3 * \
                                              game_item['pre_appointment_number_list'][0]
                else:
                    game_item['base_score'] = (game_download_data['download_number'] + game_download_data[
                        'update_number'] +
                                               fast_game_download_data['fast_download_number'] +
                                               fast_game_download_data[
                                                   'fast_update_number'] + game_item['pre_appointment_number_list'][2]
                                               + game_item['pre_appointment_number_list'][3]
                                               + game_item['pre_appointment_number_list'][4]
                                               + game_item['pre_appointment_number_list'][5]
                                               + game_item['pre_appointment_number_list'][6]) + \
                                              2 * (game_download_data_1['download_number'] + game_download_data_1[
                        'update_number'] + fast_game_download_data_1['fast_download_number'] +
                                                   fast_game_download_data_1[
                                                       'fast_update_number'] + game_item['pre_appointment_number_list'][
                                                       1]) + \
                                              3 * (today_normal_all_download_number + today_normal_all_update_number +
                                                   fast_game_download_data_0['fast_download_number'] +
                                                   fast_game_download_data_0[
                                                       'fast_update_number'] + game_item['pre_appointment_number_list'][
                                                       0])

            # 时间权重系数: 分为 预热时间系数、上架时间系数和更新时间系数，判断当前时间与不同状态对应时间的差值，
            #                     依据差值X选取对应系数参与计算，X=当前时间-Y
            '''
             >时间权重系数: 分为 预热时间系数、上架时间系数 和 更新时间系数，判断当前时间与不同状态对应时间的差值，
                    依据差值X选取对应系数参与计算，X=当前时间-Y
                    >>概念说明：
                    
                    ①预热游戏：Y取 游戏事件最新日期，该字段为空时取 版本更新时间，两个字段均为空时系数取1.0
                            X       X＜0     0≤X≤1天      1天＜X＜7天     X≥七天
                        预热时间系数   1.0       1.3          1.15         1.0                        
                        
                    ②新上架游戏：上架时间 ≥版本更新时间-3day，Y取上架时间，两个字段任一为空时
                            X       X＜0     0≤X≤1天      1天＜X≤3天     3天＜X＜7天     X≥七天
                        上架时间系数   1.0       3.5          2.0           1.45         1.0
                        
                    ③新更新游戏：上架时间＜版本更新时间-3day，Y取版本更新时间
                            X       X＜0     0≤X≤1天      1天＜X＜7天     X≥七天
                        更新时间系数   1.0       1.3          1.15         1.0 
                    
                >>兜底策略：（20240815补充）
                    ①：游戏事件最新日期 为空时，Y取 版本更新时间，两个字段均为空时系数取1.0
                    ②&③：上架时间 与 版本更新时间 两个字段任一为空时，系数取1.0            
            '''
            for index, game_item in enumerate(dujia_rank_list):
                # 获取 游戏事件最新日期 、 版本更新时间
                print()
                time_info = self.get_dujia_game_launch_time(game_item['game_id'])
                game_item['time_info'] = time_info

            for index, game_item in enumerate(dujia_rank_list):
                # 获取 时间权重系数
                # todo:1
                # 预热游戏
                if "预热" in game_item['discount_status_des']:
                    '''  X=当前时间-Y
                    ①预热游戏：Y取 游戏事件最新日期，该字段为空时取 版本更新时间，两个字段均为空时系数取1.0
                        X       X＜0     0≤X≤1天      1天＜X＜7天     X≥七天
                    预热时间系数   1.0       1.3          1.15         1.0   
                    '''
                    if len(game_item['time_info']['game_event_new_time_str']) == 0 and len(
                            game_item['time_info']['version_update_str']) == 0:
                        game_item['_time'] = 1.0
                        game_item['_time_des'] = "预热时间系数"
                    else:
                        Y = game_item['time_info']['game_event_new_time']
                        _time = 88888
                        if len(game_item['time_info']['game_event_new_time_str']) == 0:
                            Y = game_item['time_info']['version_update_time']

                        if int(time.time()) - Y < 0:
                            _time = 1.0
                        elif 0 <= int(time.time()) - Y <= 1 * 24 * 60 * 60:
                            _time = 1.3
                        elif 1 * 24 * 60 * 60 < int(time.time()) - Y < 7 * 24 * 60 * 60:
                            _time = 1.15
                        elif 7 * 24 * 60 * 60 <= int(time.time()):
                            _time = 1.0
                        game_item['_time_des'] = "预热时间系数"
                        game_item['_time'] = _time

                else:
                    '''
                    ②新上架游戏：上架时间 ≥版本更新时间-3day，Y取上架时间，两个字段任一为空时
                        X       X＜0     0≤X≤1天      1天＜X≤3天     3天＜X＜7天     X≥七天
                    上架时间系数   1.0       3.5          2.0           1.45         1.0

                    ③新更新游戏：上架时间＜版本更新时间-3day，Y取版本更新时间
                        X       X＜0     0≤X≤1天      1天＜X＜7天     X≥七天
                    更新时间系数   1.0       1.3          1.15         1.0 
                    '''
                    # if game_item['game_id'] in "118107":
                    #     print(1)
                    if len(game_item['time_info']['listing_time_str']) == 0 or len(
                            game_item['time_info']['version_update_str']) == 0:
                        game_item['_time'] = 1.0
                        game_item['_time_des'] = "时间系数_null"
                    else:
                        Y = 0
                        _time = 77777
                        if game_item['time_info']['listing_time'] >= game_item['time_info'][
                            'version_update_time'] - 3 * 24 * 60 * 60:
                            # todo:新上架游戏
                            Y = game_item['time_info']['listing_time']
                            game_item['_time_des'] = "上架时间系数"

                            if int(time.time()) - Y < 0:
                                _time = 1.0
                            elif 0 <= int(time.time()) - Y <= 1 * 24 * 60 * 60:
                                _time = 3.5

                            elif 1 * 24 * 60 * 60 < int(time.time()) - Y <= 3 * 24 * 60 * 60:
                                _time = 2.0

                            elif 3 * 24 * 60 * 60 < int(time.time()) - Y < 7 * 24 * 60 * 60:
                                _time = 1.45

                            elif 7 * 24 * 60 * 60 <= int(time.time()):
                                _time = 1.0
                            game_item['_time'] = _time

                        else:
                            # todo:新更新游戏
                            Y = game_item['time_info']['version_update_time']
                            game_item['_time_des'] = "更新时间系数"

                            if int(time.time()) - Y < 0:
                                _time = 1.0
                            elif 0 <= int(time.time()) - Y <= 1 * 24 * 60 * 60:
                                _time = 1.3

                            elif 1 * 24 * 60 * 60 < int(time.time()) - Y < 7 * 24 * 60 * 60:
                                _time = 1.15

                            elif 7 * 24 * 60 * 60 <= int(time.time()):
                                _time = 1.0
                            game_item['_time'] = _time

            for index, game_item in enumerate(dujia_rank_list):
                print()
                # 计算 输出 得分  独家关注分 = 状态权重系数 * 时间权重系数 * 基础分
                auto_score = game_item['discount_status'] * game_item['_time'] * game_item['base_score']
                auto_score = round(auto_score, 2)
                if "values" not in game_item:
                    print(f"auto_score : {auto_score}; {game_item}")
                else:
                    if float(game_item['values']) == auto_score:
                        print(f"True score: {auto_score} === {game_item}")
                    else:
                        print(f"False  {float(game_item['values'])} 、 auto——>{auto_score}  === {game_item}")

        if True:
            # todo: 获取 后台  157701 琳琅榜V2 type = 3
            print("==================   获取后台 琳琅榜v2榜单 原值、数值 数据列表 ===============================\n")
            web_rank_list = self.get_web_linlang_v2_rank("琳琅榜v2榜单", type_id="3")
            time_list = self.get_days_time_list(_days=7)
            '''
1、琳琅榜单算法优化，游戏范围需「历史评分≥8分」才能上榜，新增平均评分系数，调整评分飙升系数、时间系数；后台新增琳琅榜v2，先不作用于前端，后续观察合适再进行作用
 • 策略说明：
         > 游戏范围：所有处于「上架状态」且有「星探团标签」且「历史评分≥8分」的游戏（有修改）
         > 排序规则：排序值=（近七天下载量+更新量+快玩下载量+快玩更新量）*平均评分系数*时间系数*评分飙升系数，依据排序值进行「琳琅榜」的自然排序，取前150名（有修改）
                >> 近七天下载量+更新量+快玩下载量+快玩更新量 等于后台的“原始值”字段，排序值 等于 后台的“数值”字段
                
         > 平均评分系数：先计算出「平均评分」，基于「平均评分」执行“平均评分系数”逻辑（有修改）

         > 评分飙升系数：（有修改）

         > 时间系数：分为上架时间系数和更新时间系数，「新上架游戏」对应“上架时间系数”，「新更新游戏」对应“更新时间系数”（有修改）
                >> 系数类型 判断规则：
                         >>> 当「版本最新时间<=上架时间」时，该款游戏视为「新上架游戏」，执行「上架时间系数」逻辑
                         >>> 当「版本最新时间>上架时间」时，该款游戏视为「新更新游戏」，执行「更新时间系数」逻辑

                >> 上架时间系数：基于上架时间间隔天数，判断对应的上架时间系数
                         >>> 上架时间间隔天数X=当前时间-上架时间（时间精确到秒）；如：5月3日上架，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推
                         >>> 0<X≤1对应的上架时间系数为5
                         >>> 1<X≤2对应的上架时间系数为4
                         >>> 2<X≤3对应的上架时间系数为3
                         >>> 3<X≤7对应的上架时间系数为2
                         >>> X>7对应的上架时间系数为1

                >> 更新时间系数：基于更新时间间隔天数，判断对应的更新时间系数
                         >>> 更新时间间隔天数X=当前时间-版本最新时间（时间精确到秒）；如：5月3日为更新时间，5月3日当天X为1，5月4日当天X为2，5月5日当天X为3，以此类推
                         >>> 0<X≤1对应的更新时间系数为3
                         >>> 1<X≤2对应的更新时间系数为2.5
                         >>> 2<X≤3对应的更新时间系数为2
                         >>> 3<X≤7对应的更新时间系数为1.5
                         >>> X>7对应的上架时间系数为1
                >> 上架时间与版本更新时间两个字段同时为空时，时间系数取1；仅上架时间字段不为空，执行「上架时间系数」逻辑；仅版本更新时间字段不为空，执行「更新时间系数」逻辑；                        
            '''
            # 获取 app琳琅榜单v2
            # app_linlang_rank_list = self.get_app_linlang_rank_tab_list()
            # 爬取后他 安卓游戏后台第二版本 获取 该游戏 上架了哪几种 （普 云 快 小）
            for item in web_rank_list:
                item['status'] = self.get_web_game_detail(item['game_id'])

            for item in web_rank_list:
                # todo: # 获取评分 需要从 APP游戏详情页中获取 评分、近七天评分、最近评分
                '''
            > 平均评分系数：先计算出「平均评分」，基于「平均评分」执行“平均评分系数”逻辑（有修改）
                 >> 平均评分 计算规则：
                         >>> 若“历史评分、近7天评分、近3天评分”3个字段均存在数值，则 平均评分=（历史评分+近7天评分+近3天评分）/3
                         >>> 若“历史评分、近7天评分、近3天评分”其中2个字段存在数值，则 平均评分=（历史评分+近7天评分+近3天评分）/2
                         >>> 若“历史评分、近7天评分、近3天评分”仅1个字段（历史评分）均存在数值，则 平均评分=历史评分
                 >> 平均评分系数：
                         >>> 若9.9<=平均评分<=10，则平均评分系数为20
                         >>> 若9.7<=平均评分<9.8，则平均评分系数为18
                         >>> 若9.4<=平均评分<9.7，则平均评分系数为15
                         >>> 若9.0<=平均评分<9.4，则平均评分系数为10
                         >>> 若8.7<=平均评分<9.0，则平均评分系数为8
                         >>> 若8.4<=平均评分<8.7，则平均评分系数为5
                         >>> 若8.0<=平均评分<8.4，则平均评分系数为2
                         >>> 若平均评分<8，则平均评分系数为1                
                '''
                average_values = 99999
                # 先算出 平均值：
                item['score_data'] = self.get_app_game_detail_data(None, item['game_id'], item['status'])

                if float(item['score_data']['c_all_star']) >= 8 and float(item['score_data']['3_star']) > 0 and float(
                        item['score_data']['7_star']) > 0:
                    average_values = (float(item['score_data']['c_all_star']) + float(
                        item['score_data']['3_star']) + float(item['score_data']['7_star'])) / 3
                elif float(item['score_data']['c_all_star']) >= 8 and (
                        (float(item['score_data']['3_star']) > 0 and float(item['score_data']['7_star']) <= 0) or (
                        float(item['score_data']['3_star']) <= 0 and float(item['score_data']['7_star']) > 0)):
                    average_values = (float(item['score_data']['c_all_star']) + float(
                        item['score_data']['3_star']) + float(item['score_data']['7_star'])) / 2
                elif float(item['score_data']['c_all_star']) >= 8 and float(
                        item['score_data']['3_star']) <= 0 and float(item['score_data']['7_star']) <= 0:
                    average_values = float(item['score_data']['c_all_star'])
                # 平均评分系数
                average_x = 9999
                if 9.9 <= average_values <= 10:
                    average_x = 20
                elif 9.7 <= average_values < 9.8:
                    average_x = 18
                elif 9.4 <= average_values < 9.7:
                    average_x = 15
                elif 9.0 <= average_values < 9.4:
                    average_x = 10
                elif 8.7 <= average_values < 9.0:
                    average_x = 8
                elif 8.4 <= average_values < 8.7:
                    average_x = 5
                elif 8.0 <= average_values < 8.4:
                    average_x = 2
                elif average_values < 8:
                    average_x = 1
                item['average_x'] = average_x
                '''
                评分飙升系数
                    >> 若游戏「近7天评分-当前评分>=1」，则评分飙升系数为3
                    >> 若游戏「0.5<=近7天评分-当前评分<1」，则评分飙升系数为2
                    >> 若游戏「0<近7天评分-当前评分<=0.5」，则评分飙升系数为1.2
                    >> 其它情况，评分飙升系数为1
                '''

                if float(item['score_data']['7_star']) - float(item['score_data']['c_all_star']) >= 1:
                    item['score_multiple'] = 3
                elif 0.5 <= float(item['score_data']['7_star']) - float(item['score_data']['c_all_star']) < 1:
                    item['score_multiple'] = 2
                elif 0 < float(item['score_data']['7_star']) - float(item['score_data']['c_all_star']) <= 0.5:
                    item['score_multiple'] = 1.2
                else:
                    item['score_multiple'] = 1
                print(
                    f" 平均值_系数 : {item['average_x']} 、 平均值： {average_values} 、评分飙升系数 : {item['score_multiple']}")

                # 合并 整合 后台榜单和 app显示榜单 列表 数据 整成一个列表
            # for item in app_linlang_rank_list:
            #     for inner_item in web_rank_list:
            #         if item['game_id'] == inner_item['game_id']:
            #             item['rank'] = inner_item['rank']
            #             item['values'] = inner_item['values']  # 数值
            #             item['init_values'] = inner_item['init_values']  # 原始值

            # 获取时间系数：
            for item in web_rank_list:
                # item_data['listing_time'] = time_arrays[0]
                # item_data['listing_time_str'] = time_arrays[1]
                # item_data['Y'] = 0
                item['time'] = self.get_game_launch_time_linlang_v2(item['game_id'])
                print(item['time'])

            for index, game_item in enumerate(web_rank_list):
                # todo : 近七天下载量+更新量+快玩下载量+快玩更新量    等于后台的“原始值”字段，排序值 等于 后台的“数值”字段

                # 获取 普通游戏 近七天  下载量 + 更新量
                game_download_data = self.get_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                 time_list, None)#game_item['game_type']
                game_item['download_number'] = game_download_data['download_number']
                game_item['update_number'] = game_download_data['update_number']
                # game_item['fast_download_number'] = game_download_data['fast_download_number']   fast_download_number 值不准

                # # 获取 快玩游戏 近七天  下载量     ///+ 更新量
                fast_game_download_data = self.get_fast_game_download_data(game_item['game_id'], game_item['game_name'],
                                                                           time_list)
                game_item['fast_download_number'] = fast_game_download_data['fast_download_number']
                game_item['fast_update_number'] = fast_game_download_data['fast_update_number']

                game_item['download_data'] = game_item['download_number'] + game_item['update_number'] + game_item[
                    'fast_download_number'] + game_item['fast_update_number']  # 1200 12000

                # todo 排序值 =（近七天下载量+更新量+快玩下载量+快玩更新量）*平均评分系数*时间系数*评分飙升系数
                auto_result_score = game_item['download_data'] * float(game_item['average_x']) * \
                                    game_item['time']['time_x'] * game_item['score_multiple']

                # 四舍五入并保留小数点后一位
                auto_result_score = round(auto_result_score, 2)
                game_item['auto_result_score'] = auto_result_score

            print("\n\n=================  开始验证 琳琅榜单v2  ======================\n")
            for index, game_item in enumerate(web_rank_list):
                if 'values' in game_item:
                    aaaaa = game_item['values']
                    auto_result_score = game_item['auto_result_score']
                    print(aaaaa, auto_result_score, game_item)
                    if float(game_item['values']) == game_item['auto_result_score']:
                        print(
                            f"True  ==== {str(index + 1)} ====  {game_item['game_name']}_{game_item['game_id']} 检测正常 排序值数：  {game_item['values']}  \n")
                    else:
                        print(
                            f"False ==== {str(index + 1)} ====  {game_item['game_name']}_{game_item['game_id']}\n    检测异常 排序值数： 后台-> {game_item['values']}、（近七天下载量+更新量+快玩下载量+快玩更新量）：{game_item['init_values']}  "
                            f" auto——>{game_item['auto_result_score']}、原始值：{game_item['download_data']}、平均评分系数： {float(game_item['average_x'])} 、时间系数:{game_item['time']['time_x']} 、评分飙升系数:{game_item['score_multiple']} \n")
                else:
                    print(
                        f"False ==== {str(index + 1)} =========  可能是 锁定 {game_item['game_name']}_{game_item['game_id']}")

    # todo:获取 热门榜 导航tab标签数据
    def get_app_hot_rank_nav_tab_list(self):
        print(f"==================     获取 热门榜导航tab标签数据    ===================")
        tag_datas = []
        url = self.news_app_host + f"/cdn/android/ranktop-home-1577-type-hot2-page-1-{self.level}.htm"
        result = requests.get(url=url, headers=self.header)
        if result.json()['code'] == 100:
            tag_datas = result.json()['result']['nav']
        else:
            print("========   获取 热门榜 导航tab标签 数据失败！！！  =====================")
        return tag_datas

    # 获取 热门榜 tab列表数据
    def get_app_rank_tab_list(self, tag_datas):
        all_rank_list = []
        for tag_item in tag_datas:
            single_rank_lists = self.get_app_all_rank_list(f"{tag_item['title']}_榜单",
                                                           rank_type=tag_item['id'])  # 获取评分系数
            # single_rank_lists = []
            # rank_url = self.news_app_host + f"/cdn/android/ranktop-home-1577-type-{tag_item['type']}-page-1-{self.level}.htm"
            # print(f"=============  获取 {tag_item['title']} tab 数据   ==================")
            # result = requests.get(url=rank_url, headers=self.header)
            # if result.json()['code'] == 100:
            #     rank_datas = result.json()['result']['data']
            #     for single_item in rank_datas:
            #         item = {'game_id': single_item['id'],
            #                 'game_name': single_item['title'],
            #                 'score': single_item['score']
            #                 }
            #         print(item)
            #         single_rank_lists.append(item)
            #     # todo: 获取 快爆排行榜网页后台 自然排序的 数据
            #     web_rank_list = self.get_kb_web_rank_data(tag_item['title'], tag_item["type"].replace("type", ""))
            #     print(web_rank_list)
            # else:
            #     print(f"=============  获取 {tag_item['title']} tab 数据  失败   ==================")
            all_rank_list.append(single_rank_lists)
        return all_rank_list

    # 获取 APP 琳琅榜单 的数据
    def get_app_linlang_rank_tab_list(self):
        single_rank_lists = []
        print(f"=============  获取 琳琅榜单 tab 数据    =================")
        result = requests.get(
            url=self.news_app_host + f"/cdn/android/ranktop-home-1577-type-beautiful-page-1-{self.level}.htm")
        if result.json()['code'] == 100:
            rank_datas = result.json()['result']['data']
            for single_item in rank_datas:
                item = {'game_id': single_item['id'], 'game_name': single_item['title'],
                        "game_type": single_item['downinfo']['kb_game_type']}
                single_rank_lists.append(item)
        else:
            print(f"=============  获取 琳琅榜单 tab 数据  失败   ==================")
        return single_rank_lists

    # 获取 APP 热销榜单 的数据
    def get_app_hot_sell_rank_tab_list(self):
        single_rank_lists = []
        print(f"=============  获取 热销榜单 tab 数据    ==================")
        result = requests.get(
            url=self.news_app_host + f"/cdn/android/ranktop-home-1577-type-sales-page-1-{self.level}.htm")
        if result.json()['code'] == 100:
            rank_datas = result.json()['result']['data']
            for single_item in rank_datas:
                if "price_info" in single_item['downinfo']:
                    discount = 0
                    if single_item['downinfo']['price_info']['discount_info'] is None:
                        discount = 1
                    else:
                        discount = 3
                    item = {'game_id': single_item['id'], 'game_name': single_item['title'],
                            'discount': discount}
                    # , "price_info": single_item['downinfo']['price_info']}
                    single_rank_lists.append(item)
        else:
            print(f"=============  获取 热销榜单 tab 数据  失败   ==================")
        return single_rank_lists

    # 获取 APP 独家榜单 的数据
    def get_app_exclusive_rank_tab_list(self):
        '''
            普通-下载   		status  = 1 &   price_info null
            预约   			status = 4  &  price_info null

            普通付费（金额）  	status =3 &  price_info { discount_info=(null)、notify=1、original_price=1,price=1 }

            普通付费（爆米花） status =3 &  bmh_price_info { discount_info=(null)、original_price=500、price=500 }

            限免（金额） 		status =3 &  price_info{ discount_info= { type=2,val="史低” }，original_price=1,price=0 }
            限免（爆米花）		status =3 &  bmh_price_info{ discount_info= { type=3,val="100” }，original_price=1000,price=0} }

            折扣（金额） 		status =3 &  price_info{ discount_info={type=3,val="99”}，original_price=20,price=0.01 }
            折扣（爆米花）		status =3 &  bmh_price_info{ discount_info={ type=3,val="98” }，original_price=500,price=9 }
        '''

        single_rank_lists = []
        print(f"=============  获取 独家榜单 tab 数据    ==================")
        result = requests.get(
            url=self.news_app_host + f"/cdn/android/ranktop-home-1559-type-sole-page-1-{self.level}.htm")
        # 'http://ot.newsapp.5054399.com/cdn/android/ranktop-home-1577-type-sole-page-1-level-3.htm'
        # 'http://ot.newsapp.5054399.com/cdn/android/ranktop-home-1559-type-sole-page-1.htm'
        if result.json()['code'] == 100:
            rank_datas = result.json()['result']['data']
            for single_item in rank_datas:
                '''
                普通   			status = 1  &  price_info null
                预约   			status = 4  &  price_info null
                
                普通付费（金额）  	status =3 &  price_info { discount_info=(null)、notify=1、original_price=1,price=1 }                 
                普通付费（爆米花） status =3 &  bmh_price_info { discount_info=(null)、original_price=500、price=500 }
                
                限免（金额） 		status =3 &  price_info{discount_info={type=2,val="史低”}，original_price=1,price=0 }
                限免（爆米花）		status =3 &  bmh_price_info{discount_info={type=3,val="100”}，original_price=1000,price=0 }
                
                折扣（金额） 		status =3 &  price_info{discount_info={type=3,val="99”}，original_price=20,price=0.01 }
                折扣（爆米花）		status =3 &  bmh_price_info{discount_info={type=3,val="98”}，original_price=500,price=9}               
                '''
                if single_item['downinfo']['kb_game_type'] is None:
                    # 普通 游戏类型
                    discount_status_des = "状态："
                    discount_status = 9999999
                    if single_item['downinfo']['status'] == "1":
                        discount_status_des += "普通-下载(上架)"
                        discount_status = 1
                    elif single_item['downinfo']['status'] == "4":
                        discount_status_des += "预约(预热)"
                        discount_status = 1
                    elif single_item['downinfo']['status'] == "3":
                        if "price_info" in single_item['downinfo'] and \
                                "discount_info" in single_item['downinfo']["price_info"] and \
                                single_item['downinfo']["price_info"]['discount_info'] is None:
                            discount_status_des += "普通付费（金额）"
                            discount_status = 1.1

                        elif "bmh_price_info" in single_item['downinfo'] and \
                                "discount_info" in single_item['downinfo']["bmh_price_info"] and \
                                single_item['downinfo']["bmh_price_info"]['discount_info'] is None:
                            discount_status_des += "普通付费（爆米花）"
                            discount_status = 1.1

                        elif "price_info" in single_item['downinfo'] and \
                                "discount_info" in single_item['downinfo']["price_info"] and \
                                "type" in single_item['downinfo']["price_info"]['discount_info'] and \
                                float(single_item['downinfo']["price_info"]['price']) == 0:
                            discount_status_des += "限免（金额）"
                            discount_status = 1.15

                        elif "bmh_price_info" in single_item['downinfo'] and \
                                "discount_info" in single_item['downinfo']["bmh_price_info"] and \
                                "type" in single_item['downinfo']["bmh_price_info"]['discount_info'] and \
                                float(single_item['downinfo']["bmh_price_info"]['price']) == 0:
                            discount_status_des += "限免（爆米花）"
                            discount_status = 1.15

                        elif "price_info" in single_item['downinfo'] and \
                                "discount_info" in single_item['downinfo']["price_info"] and \
                                "type" in single_item['downinfo']["price_info"]['discount_info'] and \
                                float(single_item['downinfo']["price_info"]['price']) > 0:
                            discount_status_des += "折扣（金额）"
                            discount_status = 1.15

                        elif "bmh_price_info" in single_item['downinfo'] and \
                                "discount_info" in single_item['downinfo']["bmh_price_info"] and \
                                "type" in single_item['downinfo']["bmh_price_info"]['discount_info'] and \
                                float(single_item['downinfo']["bmh_price_info"]['price']) > 0:
                            discount_status_des += "折扣（爆米花）"
                            discount_status = 1.15

                    item = {'game_id': single_item['id'], 'game_name': single_item['title'],
                            "game_type": single_item['downinfo']['kb_game_type'], "discount_status": discount_status,
                            "discount_status_des": discount_status_des}
                    single_rank_lists.append(item)
        else:
            print(f"=============  获取 独家榜单 tab 数据  失败   =================")
        return single_rank_lists


if __name__ == '__main__':
    AAA = time.strftime("%Y/%m/%d %H:%M:%S")
    print(time.strftime("%Y/%m/%d %H:%M:%S"))
    test = RankTest()
    test.start_test()
    print("")
    # 云玩榜、小游戏榜、快玩榜、热销榜、独家榜、琳琅榜、预约榜
    print(AAA, "===>", time.strftime("%Y/%m/%d %H:%M:%S"))
