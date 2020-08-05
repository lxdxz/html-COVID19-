from flask import Flask, render_template
from flask_mail import Mail, Message
import time
import requests
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.figure
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pyecharts.charts import Map
from pyecharts import options as opts
from lxml import etree
import json

url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)  #以毫秒为单位，当前的时间戳
info = requests.get(url).text  #获取到json文件数据
info = eval(info)
china = info['data']



info = str(info)

info = info.replace("\'","\"")
new_str = ""
nn = ""

qqq = ""
val = len(info)

for i in range(0, len(info)):
	if i != 19:
		new_str = new_str + info[i]
val = len(new_str)

for q in range(0, len(new_str)):
	if q != val-2:
		qqq = qqq + new_str[q]

"""
for q in range(0, len(new_str)):
	if q != val-3:
		qqq = qqq + nn[q]
	else:
		qqq = qq+nn[q]
"""

info = qqq.replace("true","1")
info = info.replace("false","0")


info = eval(info)
comfirm = info["data"]["chinaTotal"]["confirm"]
heal = info["data"]["chinaTotal"]["heal"]
dead = info["data"]["chinaTotal"]["dead"]
nowConfirm = info["data"]["chinaTotal"]["nowConfirm"]
suspect = info["data"]["chinaTotal"]["suspect"]
nowSevere = info["data"]["chinaTotal"]["nowSevere"]
importedCase = info["data"]["chinaTotal"]["importedCase"]
com = comfirm
comfirm = str(comfirm)
heal = str(heal)
dead = str(dead)
nowConfirm = str(nowConfirm)
suspect = str(suspect)
nowSevere = str(nowSevere)
importedCase = str(importedCase)


tree = info["data"]["areaTree"][0]["children"]
def p(u):
	name = u["name"]
	strnowConfirm = u["total"]["nowConfirm"]
	strsuspect = u["total"]["suspect"]
	strdead = u["total"]["dead"]
	strdeadRate = u["total"]["deadRate"]
	strheal = u["total"]["heal"]
	strhealRate = u["total"]["healRate"]
	return [name,strnowConfirm,strsuspect,strdead,strdeadRate,strheal,strhealRate]

province_distribution={}
for o in tree:
	state = p(o)
	province_distribution[state[0]] = state[1]


conty = []


for o in range(len(tree)):
	state = p(tree[o])
	conty.append(state)
	conty.append("end")
	for y in tree[o]["children"]:
		city = p(y)
		conty.append(city)
		conty.append("cend")

total = """"""

def into(inf,cou):
	global total
	if cou<10:
		cou = "0"+str(cou)
	else:
		cou = str(cou)
	rowin = "row_"+cou
	chi_row = "child_row_"+cou
	muban = """
	<tr class="parent" id='"""+rowin+"""'>   
	        <td colspan="7"><h3>"""+inf[0]+"""</h3></td>
	      </tr>
	"""
	total+=muban

def into_c(inf,cou):
	global total
	if cou<10:
		cou = "0"+str(cou)
	else:
		cou = str(cou)
	chi_row = "row_"+cou
	muban = """
	<tr class='child_"""+chi_row+"""' style="display:none;">     
	        <td>"""+str(inf[0])+"""</td>
	        <td>"""+str(inf[1])+"""</td>
	        <td>"""+str(inf[2])+"""</td>
	        <td>"""+str(inf[3])+"""</td>
	        <td>"""+str(inf[4])+"""</td>
	        <td>"""+str(inf[5])+"""</td>
	        <td>"""+str(inf[6])+"""</td>
	      </tr>
	"""
	total+=muban

count = 0
for u in conty:
	if conty[conty.index(u)+1] == "end":
		count += 1
		into(u,count)
		into_c(u,count)
	elif conty[conty.index(u) + 1] == "cend":
		into_c(u, count)
	else:
		continue



map = Map()
map.set_global_opts(
    title_opts=opts.TitleOpts(title="China 19-nCov MAP"),
    visualmap_opts=opts.VisualMapOpts(max_=3600, is_piecewise=True,
                                      pieces=[
                                        {"max": 5000, "min": 1001, "label": ">1000", "color": "#8A0808"},
                                        {"max": 1000, "min": 500, "label": "500-1000", "color": "#B40404"},
                                        {"max": 499, "min": 100, "label": "100-499", "color": "#DF0101"},
                                        {"max": 99, "min": 10, "label": "10-99", "color": "#F78181"},
                                        {"max": 9, "min": 1, "label": "1-9", "color": "#F5A9A9"},
                                        {"max": 0, "min": 0, "label": "0", "color": "#FFFFFF"},
                                        ], )
    )
map.add("graphic", data_pair=province_distribution.items(), maptype="china", is_roam=True)
map.render('templates/graphic.html')



map = Map()
map.set_global_opts(
    title_opts=opts.TitleOpts(title="China 19-nCov MAP"),
    visualmap_opts=opts.VisualMapOpts(max_=3600, is_piecewise=True,
                                      pieces=[
                                        {"max": 5000, "min": 1001, "label": ">1000", "color": "#8A0808"},
                                        {"max": 1000, "min": 500, "label": "500-1000", "color": "#B40404"},
                                        {"max": 499, "min": 100, "label": "100-499", "color": "#DF0101"},
                                        {"max": 99, "min": 10, "label": "10-99", "color": "#F78181"},
                                        {"max": 9, "min": 1, "label": "1-9", "color": "#F5A9A9"},
                                        {"max": 0, "min": 0, "label": "0", "color": "#FFFFFF"},
                                        ], )
    )
map.add("China 19-nCov MAP", data_pair=province_distribution.items(), maptype="china", is_roam=True)

ht = """"""
with open("templates/graphic.html","r") as ii:
	wq = ii.read()
	ht+=wq

context = {
	"data": total,
	"confirm": comfirm,
	"heal": heal,
	"dead": dead,
	"nowConfirm": nowConfirm,
	"suspect": suspect,
	"nowSevere": nowSevere,
	"importedCase": importedCase,
	"html": ht
}

data2 = {"args":{"req":{"tab":"shishitongbao","readIds":[],"reqType":2,"limit":2,"areaName":"国内"}},"service":"THPneumoniaOuterService","func":"getAreaContents","context":{"userId":"f288b5283ef44b09b413506dcad34b6f"}}
data = {"args":{"req":{"tab":"shishitongbao","readIds":[],"reqType":2,"limit":5,"areaName":"国外"}},"service":"THPneumoniaOuterService","func":"getAreaContents","context":{"userId":"f288b5283ef44b09b413506dcad34b6f"}}
headers={
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36 SLBrowser/6.0.1.3091",
	"Content-Type": "application/json;charset=UTF-8"
}
url = "https://mitest.wecity.qq.com/ncovh5api/THPneumoniaService/getAreaContents"

resp = requests.post(url=url,data=json.dumps(data),headers=headers).text
resp2 = requests.post(url=url,data=json.dumps(data2),headers=headers).text
resp = eval(resp)
resp2 = eval(resp2)

foriegnurl = "https://mitest.wecity.qq.com/ncovh5api/THPneumoniaOuterDataService/getInfoBatch"
fordata = {"args":{"req":{"batchReq":{"getChinaTotal":"{\"none\":\"none\"}","getAreaInfo":"{\"none\":\"none\"}","getForeignTotal":"{\"none\":\"none\"}","getForeignInfo":"{\"none\":\"none\"}","getForeignHistory":"{\"none\":\"none\"}","getHubeiInfo":"{\"none\":\"none\"}","getRate":"{\"none\":\"none\"}","getCityInfoByCode":"{\"cityCode\":\"420100\"}"}}},"service":"THPneumoniaOuterDataService","func":"getInfoBatch","context":{"userId":"f288b5283ef44b09b413506dcad34b6f"}}
froresp = requests.post(url=foriegnurl,data=json.dumps(fordata),headers=headers).text
froresp = eval(froresp)


dataw = """"""
wro = froresp["args"]["rsp"]['batchRsp']["getForeignInfo"]
wro = eval(wro)
wro = wro["foreignTotal"]
print(len(wro))
for kk in wro:
	mu = """<tr class="child_row_01" style="display:none;">     
	        <td><h3>"""+str(kk["country"])+"""</h3></td>
	        <td><h3>"""+str(kk["confirm"])+"""</h3></td>
	        <td><h3>"""+str(kk["suspect"])+"""</h3></td>
	        <td><h3>"""+str(kk["dead"])+"""</h3></td>
	        <td><h3>"""+str(kk["heal"])+"""</h3></td>
	        <td><h3>"""+str(kk["modifyConfirm"])+"""</h3></td>
	        <td><h3>"""+str(kk["modifyDead"])+"""</h3></td>
	        <td><h3>"""+str(kk["modifyHeal"])+"""</h3></td>
	      </tr>
	"""
	dataw+=mu
context["dataw"] = dataw

ft = eval(froresp["args"]["rsp"]["batchRsp"]["getForeignTotal"])
ft = ft["data"]

date = ft["foreignTotalUpdateTime"]
ft = ft["foreignTotal"]
wtconfirm = ft["confirm"]
wtdeaad = ft["dead"]
wtheal = ft["heal"]
wtnowconfirm = ft["nowConfirm"]

ft = eval(froresp["args"]["rsp"]["batchRsp"]["getForeignTotal"])
ft = ft["data"]['foreignDayModify']
wttconfirm = ft["confirm"] + com
wttheal = ft["heal"]
wttdead = ft["dead"]
wttnowconfirm = ft["nowConfirm"]

context["date"] = date
context["wconfirm"] = str(wtconfirm)
context["wdead"] = str(wtdeaad)
context["wheal"] = str(wtheal)
context["wnowConfirm"] = str(wtnowconfirm)
context["wtconfirm"] = "+"+str(wttconfirm)
context["wtdead"] = "+"+str(wttdead)
context["wtheal"] = "+"+str(wttheal)
context["wtnowConfirm"] = "+"+str(wttnowconfirm)



art=""""""


"""
	if pc==4:
		break
	else:
"""


pc = 0
for uuu in resp["args"]["rsp"]["contents"]:
	pc+=1
	title = uuu["title"]
	pag = uuu["desc"]
	href = uuu["jumpLink"]["url"]
	artmu = """
	<article class="footer_column">
	      <h3><a style="text-decoration: none" href="""+href+""">""" + title + """</a></h3>
	      <p>""" + pag + """</p></article>
	"""
	art+=artmu

for uuup in resp2["args"]["rsp"]["contents"]:
	pc+=1
	title = uuup["title"]
	pag = uuu["desc"]
	href = uuu["jumpLink"]["url"]
	artmu = """
	<article class="footer_column">
	      <h3><a style="text-decoration: none" href="""+href+""">""" + title + """</a></h3>
	      <p>""" + pag + """</p></article>
	"""
	art+=artmu

context["article"] = art


myapp = Flask(__name__)
@myapp.route('/')
def index():
	return render_template('index.html',**context)

myapp.run()


