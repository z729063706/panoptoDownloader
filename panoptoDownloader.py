import json
import math
import requests
cookies = {
    #此处自行更换为自己的cookie
}

headers = {
    'authority': 'auckland.au.panopto.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'referer': 'https://auckland.au.panopto.com/Panopto/Pages/Viewer.aspx?id=19d4e9e9-c978-4865-9b24-aed5015b46d8',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'x-csrf-token': '此处也更换',
    'x-requested-with': 'XMLHttpRequest',
}

ccdata = {
    'deliveryId': '',
    'getCaptions': 'true',
    'language': '1',
    'responseType': 'json',
}
infodata = {
    'deliveryId': '',
    'invocationId': '',
    'isLiveNotes': 'false',
    'refreshAuthCookie': 'true',
    'isActiveBroadcast': 'false',
    'isEditing': 'false',
    'isKollectiveAgentInstalled': 'false',
    'isEmbed': 'false',
    'responseType': 'json',
}


vid = input("欢迎使用panopto视频下载器！\n首次使用请更换cookie！\n请输入视频网址id，如19d4e9e9-c978-4865-9b24-aed5015b46d8:")
ccdata['deliveryId'] = vid
infodata['deliveryId'] = vid
inforesponse = requests.post('https://auckland.au.panopto.com/Panopto/Pages/Viewer/DeliveryInfo.aspx', cookies=cookies, headers=headers, data=infodata)
ccresponse = requests.post('https://auckland.au.panopto.com/Panopto/Pages/Viewer/DeliveryInfo.aspx', cookies=cookies, headers=headers, data=ccdata)

info = json.loads(inforesponse.text)
jsoncc = json.loads(ccresponse.text)
videourl = info['DownloadUrl']
srtcc = ''
videoname = info['Delivery']['SessionName']
line = 1
print('视频名称：' + videoname)
for cc in jsoncc:
    start = cc['Time'] 
    stop = start + cc['CaptionDuration']  
    stop = round(stop, 3)  
    content = cc['Caption']  
    srtcc += '{}\n'.format(line) 
    hour = math.floor(start) // 3600
    minute = (math.floor(start) - hour * 3600) // 60
    sec = math.floor(start) - hour * 3600 - minute * 60
    minisec = int(math.modf(start)[0] * 100)  
    srtcc += str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(sec).zfill(2) + ',' + str(minisec).zfill(2)
    srtcc += ' --> '
    hour = math.floor(stop) // 3600
    minute = (math.floor(stop) - hour * 3600) // 60
    sec = math.floor(stop) - hour * 3600 - minute * 60
    minisec = abs(int(math.modf(stop)[0] * 100 - 1))
    srtcc += str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(sec).zfill(2) + ',' + str(minisec).zfill(2)
    srtcc += '\n' + content + '\n\n'  
    line += 1
with open('./{}.srt'.format(videoname), 'w', encoding='utf-8') as f:
    f.write(srtcc)  
    f.close()
print('字幕保存成功！')
print('正在下载视频，如长时间卡住（没网速）请关闭重试！')
videofile = requests.get(videourl, cookies=cookies, headers=headers)
with open('./{}.mp4'.format(videoname), 'wb') as f:
    f.write(videofile.content)
    f.close()
print('下载完成！')