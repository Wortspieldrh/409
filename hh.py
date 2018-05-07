import sys
import sklearn
import requests
import json
import csv
import datetime
import time

def getdata():
    pass
    # start
    podUrl = "http://10.60.38.181:10001/api/v1/model/namespaces/default/pods"
    podNames = requests.get(podUrl).json()
    #print(podNames)
    for podName in podNames:
        baseUrl = "http://10.60.38.181:10001/api/v1/model/namespaces/default/pods/" + podName + "/metrics/"
        metricNames = [
            "cpu/limit",
            "network/tx_rate",
            "cpu/usage_rate",
            "network/tx_errors_rate",
            "network/rx_rate",
            "cpu/usage",
            "network/tx_errors",
            "memory/usage",
            "network/rx_errors_rate",
            "uptime",
            "memory/working_set",
            "memory/limit",
            "restart_count",
            "cpu/request",
            "memory/major_page_faults",
            "memory/page_faults_rate",
            "network/rx_errors",
            "network/rx",
            "memory/major_page_faults_rate",
            "memory/cache",
            "memory/request",
            "memory/rss",
            "memory/page_faults",
            "network/tx"
        ]
        csv_dataset = dict()
        for metricName in metricNames:
            curUrl = baseUrl + metricName
            localtime = datetime.datetime.now()
            endTime = localtime.strftime('%Y-%m-%d') + 'T' + hourConvertor(localtime.hour) + ':' + minuteConvertor(
                localtime.minute) + ':' + secondConvertor(localtime.second) + 'Z'
            startTime = localtime.strftime('%Y-%m-%d') + 'T' + hourConvertor(localtime.hour) + ':' + minuteConvertor(
                localtime.minute - 2) + ':' + secondConvertor(localtime.second) + 'Z'
            time = {'start': startTime, 'end': endTime}
            curReq = requests.get(curUrl, params=time)  # 取回的是reponse对象
            json_req = curReq.json()  # 通过req.json()将reponse对象转换为dict(并非json)
            size = len(json_req['metrics'])
            for i in range(size):
                curTimestamp = json_req['metrics'][i]['timestamp']
                curValue = json_req['metrics'][i]['value']
                if curTimestamp in csv_dataset.keys():
                    csv_dataset[curTimestamp][metricName] = curValue
                else:
                    metricNameValueDic = dict()
                    metricNameValueDic[metricName] = curValue
                    csv_dataset[curTimestamp] = metricNameValueDic

        startTime = sorted(csv_dataset.keys(), reverse=False)[0].replace(":", "-")
        endTime = sorted(csv_dataset.keys(), reverse=True)[0].replace(":", "-")
        filename = "data/" + podName + "_" + startTime + "_" + endTime + ".csv"
        csvfile = open("data/" + podName, 'a', newline='')  # 打开文件
        writer = csv.writer(csvfile)  # 启用writer
        writer.writerow(["timestamp"] + metricNames)
        for timestamp in sorted(csv_dataset.keys(), reverse=False):
            row = []
            for name in metricNames:
                if name in csv_dataset[timestamp].keys():
                    row.append(csv_dataset[timestamp][name])
                else:
                    row.append("")
            writer.writerow([timestamp] + row)
        csvfile.close()

def hourConvertor(hour):
    newHour = hour - 8
    if newHour<0:
        newHour += 24
        return str(newHour)
    elif newHour<10:
        return "0"+str(newHour)
    else:
        return str(newHour)

def minuteConvertor(minute):
    if minute<10:
        return '0' + str(minute)
    else:
        return str(minute)

def secondConvertor(second):
    if second<10:
        return  '0' + str(second)
    else:
        return  str(second)

def main():
    while True:
        getdata()
        time.sleep(60)


if __name__ == "__main__":
    main()












