import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class GetInfo:
    def __init__(self) -> None:
        super().__init__()

        self.level = "level-4"
        self.dev = True
        #self.dev = False  # False OT

        self.dev_web_host = "https://dev.admin.newsapp.5054399.com"
        self.dev_web_cookie = {"PHPSESSID": "9l4rr9un2eet2u15vn7ji03k32"}
        self.ot_web_host = "http://ot.admin.newsapp.5054399.com"
        self.ot_web_cookie = {"PHPSESSID": "ol0l5edok1kgn8vdhshn11acs3"}
        # 5566  设备
        self.header = {
            "User-Agent": "Androidkb/1.5.7.507(android;auto;7.1.2;1080x1920;WiFi);at"
        }
        if self.dev:
            self.web_host = self.dev_web_host
            self.web_cookie = self.dev_web_cookie
        else:
            self.web_host = self.ot_web_host
            self.web_cookie = self.ot_web_cookie


    def get_web_game_detail(self, game_id):
        content = ""
        try:
            url = self.web_host + f"/games/game.android.v2.php?ac=edit&id={game_id}"
            game_info_result = requests.get(url=url, cookies=self.web_cookie)
            if game_info_result.status_code == 200:
                soup = BeautifulSoup(game_info_result.content, 'html5lib')
                # 查找游戏名称
                app_name = soup.select('input[name="appname"]')
                if app_name:
                    value = app_name[0].get('value', '')
                    print(f"游戏名称: {value}")

                print(f"=============开始查询普通游戏信息：============= ")
                # 查找普通游戏相关信息
                selectors = {
                    'level': ('input[name="level"][checked="true"]', 'value', '等级'),
                    'status': ('select[name="status"] option[selected]', 'text', '状态'),
                }
                
                for key, (selector, attr_type, label) in selectors.items():
                    elements = soup.select(selector)
                    if elements:
                        value = elements[0].text.strip() if attr_type == 'text' else elements[0].get('value', '')
                        if key == 'priority':
                            value = "是" if value == "1" else "否"
                        print(f"普通游戏--{label}: {value}")
                print(f"================================================")

                print(f"===============开始查询快玩信息：=============== ")
                # 查找快玩相关信息
                selectors = {
                    'type': ('input[name="fast_game_type"][checked]', 'value', '位数'),
                    'level': ('input[name="fast_level"][checked="true"]', 'value', '等级'),
                   'status': ('select[name="fast_status"] option[selected="selected"]', 'text', '状态'),
                    'priority': ('input[name="fast_priority_show"][checked]', 'value', '是否优先')
                }
                for key, (selector, attr_type, label) in selectors.items():
                    elements = soup.select(selector)
                    if elements:
                        value = elements[0].text.strip() if attr_type == 'text' else elements[0].get('value', '')
                        if key == 'priority':
                            value = "是" if value == "1" else "否"
                        elif key == 'type':
                            type_map = {
                                "1": "32位",
                                "2": "32位/64位",
                                "3": "64位"
                            }
                            value = type_map.get(str(value), str(value))
                        print(f"快玩--{label}: {value}")
                print(f"================================================")
                    
                print(f"==============开始查询小游戏信息：==============")
                # 查找小游戏相关信息
                selectors = {
                    'type': ('input[name="mini_game_type"][checked="checked"]', 'value', '类型'),
                    'level': ('input[name="mini_level"][checked="true"]', 'value', '等级'),
                    'status': ('select[name="mini_status"] option[selected="selected"]', 'text', '状态'),
                    'priority': ('input[name="mini_priority_show"][checked]', 'value', '是否优先')
                }
                for key, (selector, attr_type, label) in selectors.items():
                    elements = soup.select(selector)
                    if elements:
                        value = elements[0].text.strip() if attr_type == 'text' else elements[0].get('value', '')
                        if key == 'priority':
                            value = "是" if value == "1" else "否"
                        print(f"小游戏--{label}: {value}")
                print(f"================================================")

                print(f"===============开始查询云玩信息：=============== ")
                # 查找云游戏相关信息
                selectors = {
                    'level': ('input[name="cloud_level"][checked="true"]', 'value', '等级'),
                    'status': ('select[name="cloud_status"] option[selected="selected"]', 'text', '状态'),
                    'priority': ('input[name="mini_priority_show"][checked]', 'value', '是否优先')
                }
                
                for key, (selector, attr_type, label) in selectors.items():
                    elements = soup.select(selector)
                    if elements:
                        value = elements[0].text.strip() if attr_type == 'text' else elements[0].get('value', '')
                        if key == 'priority':
                            value = "是" if value == "1" else "否"
                        print(f"云玩--{label}: {value}")
                
                # 查找云玩各个线路容器、LEVEL、线路名称、线路类型、线路状态
                containers = soup.select('input[name="ext_cloud_line[container][]"]')
                names = soup.select('input[name="ext_cloud_line[name][]"]')
                levels = soup.select('select[name="ext_cloud_line[level][]"]')
                types = soup.select('select[name="ext_cloud_line[type][]"]')

                # 获取所有线路数量
                line_count = max(len(containers), len(names), len(levels), len(types))
                
                # 按线路组织输出
                for i in range(line_count):
                    print(f"\n线路{i+1}:")
                    line_info = []
                    
                    # 获取容器信息
                    if i < len(containers) and containers[i].get('value'):
                        line_info.append(f"容器{i+1}：{containers[i].get('value')}")
                    
                    # 获取名称信息
                    if i < len(names) and names[i].get('value'):
                        line_info.append(f"名称{i+1}：{names[i].get('value')}")
                    
                    # 获取level信息
                    if i < len(levels):
                        selected = levels[i].select_one('option[selected]')
                        if selected and selected.text:
                            line_info.append(f"LEVEL{i+1}：{selected.text.strip()}")
                    
                    # 获取类型信息
                    if i < len(types):
                        selected = types[i].select_one('option[selected]')
                        if selected and selected.text:
                            line_info.append(f"类型{i+1}：{selected.text.strip()}")
                    
                    if line_info:
                        print(' | '.join(line_info))
                        
                print(f"================================================")

        except Exception as e:
            print(f"=======获取 {game_id}异常：{str(e)} 上架哪几种类型游戏 ========================")
        return content


if __name__ == '__main__':
    info = GetInfo()  # 创建实例
    test = info.get_web_game_detail(118904)  # 调用方法
    print(test)
