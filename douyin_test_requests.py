# 请求模块
import json
import os
import re
import requests
import sys

# 格式化输出模块
# from pprint import pprint
# 爬取抖音无水印
# 原始链接
'''url = input("请输入抖音分享链接：")
if 'douyin' in url:
    # 处理抖音链接
    print("解析抖音链接中")
else:
    # 提示用户输入抖音链接
    print("请输入抖音分享链接")
    # 停止程序的运行
    sys.exit()'''
while True:
    while True:
        url = input("抖音分享链接 ( 退出请输入：quit )：")
        if url == 'quit':
            # 用户输入 quit，停止循环
            sys.exit()
        elif 'douyin' in url:
            # 处理抖音链接
            print("解析抖音链接中")
            # 处理完成后退出循环
            break
        elif 'kuaishou' in url:
            # 处理快手链接
            print("不支持快手链接")
        else:
            # 提示用户输入抖音链接
            print("请输入正确的抖音分享链接")
    # 使用re.findall()函数查找所有匹配项
    pattern = r'(https?://\S+)'
    # 输出所有匹配的URL
    urls = re.findall(pattern, url)[0]
    # 打印
    print('处理重定向')
    # 开始处理重定向链接
    html = requests.get(urls, allow_redirects=False)
    # 获取跳转地址
    url2 = html.headers['Location']
    print('获取链接')
    # 提取里面的链接用于替换
    title = re.findall('https://(.*?)?region=', url2)[0]
    print('替换中')
    # 替换成抖音的最终链接
    title = title.replace('?', '')
    title = title.replace('iesdouyin', 'douyin')
    title = title.replace('share/', '')
    url = ('https://' + title)
    print('解析链接：'+url)
    '''
    # 发送get请求
    response = requests.get(url)
    # 检查最终的URL
    redirect_url = response.url
    print(redirect_url)'''
    # 变量
    headers = {
        # 添加一个亲球头信息
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/110.0.0.0'
                      'Safari/537.36 Edg/110.0.1587.57'
        ,
        'cookie': '__ac_nonce=064022a0900f3ffd992d5; __ac_signature=_02B4Z6wo00f01E.nd2QAAIDBupid-GpYXOBPx3PAAHgD57; '
                  '__ac_referer=__ac_blank'
    }
    # 提取标题
    resp = requests.get(url=url, headers=headers)
    # print(resp.text)
    # 这行代码使用了Python中的正则表达式模块re。它的作用是从resp.text中匹配出第一个符合''这个正则表达式的字符串，并将其存储在title变量中。
    # 具体而言，这个正则表达式表示匹配以''结尾的字符串，并在这两个标签之间匹配任何字符（.?表示非贪婪匹配，即尽可能少地匹配字符）。其中，data-react-helmet="true"是HTML标签上的一个属性，它用于控制网页的头部信息，包括标题。
    # 因此，这行代码的作用是从resp.text中提取出网页的标题，并将其存储在title变量中供后续使用
    # print(resp.text)
    title = re.findall('<title data-react-helmet="true">(.*?)</title>', resp.text, re.S)[0]
    title = re.sub('\s+', ' ', title)
    title = re.sub(r'#\w+', '', title)
    title = re.sub(r'.。', '', title)
    print(title)
    title = re.sub(r'\s+', ' ', title)
    print(title)

    # 这行代码使用了 Python 字符串的 replace() 方法，将 title 变量中的 # 字符替换为空字符串，从而去除了字符串中的 #。最终的结果将存储在 title 变量中，供后续使用。

    # 提取视频信息
    title = title.replace('#', '')
    # 解析数据
    info = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script>', resp.text)[0]
    # print(info)
    html_data = requests.utils.unquote(info)
    # print(html_data)
    json_data = json.loads(html_data)
    # pprint(json_data['44']['aweme']['detail']['video']['bitRateList'])
    # loss = json_data['44']['aweme']['detail']['video']['bitRateList'][0]['playAddr'][0]
    # pprint(loss)
    video_url = 'https:' + json_data['44']['aweme']['detail']['video']['bitRateList'][0]['playAddr'][0]['src']

    video_data = requests.get(url=video_url, headers=headers).content
    # .content 返回二进制数据
    # with open('woniu\\' + title + '.mp4', mode='wb') as f:
    #     f.write(video_data)
    #     print('下载完成')


    # # 获取当前目录
    # current_dir = os.getcwd()
    # print(current_dir)
    # # 创建 Download 文件夹
    # download_dir = os.path.join(current_dir, 'Download_tiktok')
    # if not os.path.exists(download_dir):
    #     os.makedirs(download_dir)
    # # 检查文件是否已经存在

    # 获取当前脚本文件的绝对路径
    script_path = os.path.abspath(__file__)
    print(script_path)
    # 获取当前脚本所在目录的绝对路径
    script_dir = os.path.dirname(script_path)
    print(script_dir)
    # 将当前脚本所在目录和字符串 "Download_tiktok" 拼接起来，生成下载目录的路径
    download_dir = os.path.join(script_dir, "Download_tiktok")
    print(download_dir)
    # 创建下载目录（如果不存在）
    os.makedirs(download_dir, exist_ok=True)

    file_path = os.path.join(download_dir, title + '.mp4')
    if os.path.exists(file_path):
        while True:
            overwrite = input('文件已存在，是否覆盖？(y/n):')
            if overwrite.lower() == 'y':
                # 覆盖文件
                with open(file_path, mode='wb') as f:
                    f.write(video_data)
                    print('下载完成')
                break
            elif overwrite.lower() == 'n':
                print('取消下载')
                break
            else:
                print('输入有误，请重新输入')

    else:
        # 下载文件并保存到 Download 文件夹中
        with open(file_path, mode='wb') as f:
            f.write(video_data)
            print('下载完成')