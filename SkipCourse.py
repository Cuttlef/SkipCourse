import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
from io import BytesIO

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
# 禁用音频
options.add_argument("--mute-audio")
# 禁止最小化窗口时暂停视频播放
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
# options.addArguments("--headless")
options.add_argument("--disable-browser-side-navigation")
service = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

# 创建Chrome浏览器的实例
driver.maximize_window()
def clickLogin(path,url):
    # 设置ChromeDriver的路径 ../chromedriver_win32/chromedriver.exe
    chromedriver_path = f'{path}'
    # 打开课程网页
    driver.get(f'{url}')
    # 登录课程平台（如果需要登录）
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/button').click()
def login(loginUser, loginPassword,code):
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/form/div[1]/div/div/input').send_keys(f'{loginUser}')
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/form/div[2]/div/div/input').send_keys(
        f'{loginPassword}')
    # 验证码
    # element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/form/div[3]/div/div/img')
    # imgCodeUrl = element.get_attribute("src")
    # print(imgCodeUrl)
    # # 读取验证码图片并进行文本识别
    # response = requests.get(imgCodeUrl)
    # image = Image.open(BytesIO(response.content))
    # text = pytesseract.image_to_string(image)
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/form/div[3]/div/div/div/input').send_keys(code)
    time.sleep(10)
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/form/button').click()
    # 等待页面加载完成
    time.sleep(3)
    driver.refresh()

# def inCoursePage(courseId):
#     # 进入课程页面
#     driver.get(f'https://kkzxsx.yit.edu.cn/course/study/ware/{courseId}')
#     # 等待页面加载完成
#     time.sleep(3)


def index(url, data, sectionIdList):
    indexResponse = requests.post(url=url, json=data)
    responseJson = indexResponse.json()
    chapters = responseJson['data']['chapters']
    # print(chapters)

    for i in range(len(chapters)):
        sections = chapters[i]['sections']
        # 目录
        sectionsName = chapters[i]['name']
        for j in range(len(sections)):
            sectionIdMap = {}
            sectionId = sections[j]['id']
            # 课程名称
            sectionName = sections[j]['name']
            # 每节课的时长
            videoDuration = sections[j]['videoDuration']
            sectionIdMap['sectionId'] = sectionId
            sectionIdMap['sectionName'] = sectionName
            sectionIdMap['videoDuration'] = videoDuration
            sectionIdList.append(sectionIdMap)


def courseVideoPage(sectionId, sectionName,courseId):
    video_element_now_s = ''
    # 等待页面加载完成
    driver.implicitly_wait(5)
    driver.refresh()
    # 输出日志
    print('当前正在观看: ' + sectionName)
    # 请求课程的视频界面
    driver.get(f'https://kkzxsx.yit.edu.cn/course/play/{courseId}/{sectionId}')
    time.sleep(5)
    # 查找视频元素并点击播放
    print('开始点击播放按键')
    try:
        driver.find_element(By.XPATH, '//*[@id="vjs_video_3"]/button').click()
        video_element_now = driver.find_element(By.XPATH, '//*[@id="vjs_video_3"]/div[4]/div[4]/span[2]')
        video_element_now_s = video_element_now.text
        print('当前视频时长为: ', video_element_now_s)
    except:
        print('这段代码报异常了')
    duration = video_element_now_s.split(':')
    # print(duration)
    minute = int(duration[0]) * 60
    totalSeconds = int(minute + int(duration[1])) + 5  # 观看时长（单位：秒）
    # print(totalSeconds)
    time.sleep(totalSeconds)
    print('当前视频观看完毕,正在切换下一个视频')


if __name__ == '__main__':
    print('仅供学习交流,请勿贩卖,该程序免费,如有BUG请反馈-----By zzJ  https://lzai.fun')
    print('重要提示: 请不要手动点击最小化窗口,可以正常使用电脑,做其他事情')
    print('重要提示: 请不要手动点击最小化窗口,可以正常使用电脑,做其他事情')
    print('重要提示: 请不要手动点击最小化窗口,可以正常使用电脑,做其他事情')
    InputPath = input('请输入chromedriver的路径: ')
    path = InputPath + '\\chromedriver.exe'
    mainUrl = input('请输入登录地址(学校): ')
    clickLogin(path,mainUrl)
    loginUser = input('请输入账号: ')
    loginPassword = input('请输入密码: ')
    loginCode = input('请输入验证码: ')
    login(loginUser,loginPassword,loginCode)
    courseId = input('请输入课程id(你可以点击要学习的课程,浏览器的url地址最后的数字就是id): ')
    pageNums = input('请输入章节(0-?,默认0)因为平台限制时长可能会中断学习,再次运行请输入控制台的章节id,不输入默认从头开始: ')
    if pageNums == '':
        pageNums = 0
    else:
        pageNums = int(pageNums)
    # 解析页面 json
    url = 'https://kkzxsx.yit.edu.cn/api/v1/home/course_detail'
    data = {
        'id': f'{courseId}'
    }
    sectionIdList = []
    index(url, data, sectionIdList)
    for i in range(pageNums, len(sectionIdList)):
        print('您正在学习章节id为: ', i)
        courseVideoPage(sectionIdList[i]['sectionId'], sectionIdList[i]['sectionName'],courseId)
    print('观看完毕')
    # 关闭浏览器
    driver.quit()

