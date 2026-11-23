import csv
W14="https://zh.wikipedia.org/zh-tw/2014年中華民國直轄市長及縣市長選舉"
W22="https://zh.wikipedia.org/zh-tw/2022年臺北市市長選舉"
WR="https://zh.wikipedia.org/zh-tw/中華民國歷任直轄市長得票率"
W24="https://en.wikipedia.org/wiki/Opinion_polling_for_the_2024_Taiwanese_presidential_election"
W24R="https://en.wikipedia.org/wiki/2024_Taiwanese_presidential_election"
# (election,pollster,date,n,blue_cand,blue,green_cand,green,und,url,third)
rows=[]
def A(e,p,d,n,b,g,u,url,bc,gc,third=None): rows.append(dict(election=e,pollster=p,date=d,n=n,blue_cand=bc,blue_pct=b,green_cand=gc,green_pct=g,undecided=u,source_url=url,third=third))
# 2014 連 vs 柯
for p,d,ko,li,u in [("聯合報系","2014-11-16",42,28,29),("TVBS","2014-11-18",51,29,18),("蘋果日報","2014-11-08",55.68,33.15,7.07),("旺旺中時","2014-11-08",46.9,30.2,16.2),("趨勢","2014-11-15",43.0,30.0,26.2),("壹電視","2014-11-13",44.9,26.7,28.4),("自由時報","2014-11-15",44.27,25.66,30.07),("世新大學","2014-11-16",40.1,28.6,25.7)]:
  A("2014TPE",p,d,"",li,ko,u,W14,"連勝文","柯文哲")
A("2014TPE","RESULT","2014-11-29",1493918 if False else "",40.82,57.16,"",WR,"連勝文","柯文哲")
# 2018 丁 vs 姚 (green), third=柯
for p,d,n,ko,ti,ya,u,url in [("TVBS","2018-11-11~12",1130,39,36,12,12,"https://www.chinatimes.com/realtimenews/20181113002652-260407"),("美麗島電子報","2018-11-05~07",1075,38.6,27.1,8.3,18.0,"https://www.storm.mg/article/617488"),("聯合報","2018-11-01",'',38,35,8,'',"https://www.rti.org.tw/news/view/id/2000878"),("台灣競爭力論壇","2018-10-27~29",1069,36.6,34.3,12.7,15.7,"https://www.tcf.tw/%E8%AC%9D%E6%98%8E%E8%BC%9D%EF%BC%9A%E5%8F%B0%E5%8C%97%E5%B8%82%E9%95%B7%E7%88%AD%E9%9C%B8%E6%88%B0%E6%B0%91%E8%AA%BF%E7%99%BC%E4%BD%88%E6%9C%83-%E5%B8%82%E6%94%BF%E8%83%BD%E5%8A%9B%E6%AF%94%E4%B8%80/"),("旺旺中時","2018-11-12",'',33.6,32.8,None,'',"https://www.storm.mg/article/617272")]:
  A("2018TPE",p,d,n,ti,ya,u,url,"丁守中","姚文智",ko)
A("2018TPE","RESULT","2018-11-24","",40.82,17.28,"",WR,"丁守中","姚文智",41.07)
# 2022 蔣 vs 陳, third=黃
for p,d,c,ch,h,u in [("美麗島電子報","2022-11-02",34.3,27.7,22.4,15),("菱傳媒","2022-11-05",36.48,33.47,27.97,1.44),("台灣民意基金會","2022-11-07",29.8,21.8,26.6,21),("中華亞太菁英交流協會","2022-11-08",27.8,29.1,28.8,14.3),("震傳媒","2022-11-10",34.7,26.2,21.7,12.9),("匯流","2022-11-10",30.6,26.8,27.0,14.6),("自由時報","2022-11-11",28.71,34.80,23.45,12.01),("三立","2022-11-12",29.5,32.0,17.6,20.8),("蓋洛普","2022-11-13",34.25,22.79,15.60,22.90),("聯合報","2022-11-13",36,20,27,17),("ETtoday","2022-11-14",37.9,29.4,22.5,10.2),("TVBS","2022-11-14",36,25,24,'')]:
  A("2022TPE",p,d,"",c,ch,u,W22,"蔣萬安","陳時中",h)
A("2022TPE","RESULT","2022-11-26","",42.29,31.93,"",WR,"蔣萬安","陳時中",25.14)
# 2024 national 侯 vs 賴, third=柯 (4th col = others+undecided mixed)
for p,d,n,l,h,k,u in [("Formosa daily","2023-12-27~29",1253,39.6,28.5,18.9,13.0),("QuickseeK","(未標日期,表中最後列)",1285,33.7,23.7,27.7,14.8),("TVBS","2023-12-30",1407,33,30,24,13),("ETtoday","2023-12-31~2024-01-01",1557,38.9,35.8,22.4,2.8),("TPOF","2023-12-22~24",1076,32.4,28.2,24.6,14.8),("CMMedia","2023-12-23~25",1066,29.5,22.7,27.8,20.1),("Mirror Media","2023-12-30~31",1099,35.6,24.1,24.2,16.2),("SETN","2023-12-26~27",1095,30.9,27.9,23.8,17.5),("RW News","2023-12-25~29",12409,36.89,32.83,28.64,1.63),("FTNN","2023-12-26~29",1200,35.8,27.3,22.1,14.8),("udn","2023-12-26~30",1215,32,27,21,20)]:
  A("2024PRES_NATL",p,d,n,h,l,u,W24,"侯友宜","賴清德",k)
A("2024PRES_NATL","RESULT","2024-01-13","",33.49,40.05,"",W24R,"侯友宜","賴清德",26.46)
A("2024PRES_TPE","RESULT","2024-01-13","",38.08,38.13,"",W24R,"侯友宜","賴清德",23.79)
with open("/tmp/tpe2026/poll_bias.csv","w",newline="") as f:
  w=csv.writer(f); w.writerow("election,pollster,date,n,blue_cand,blue_pct,green_cand,green_pct,undecided,source_url".split(","))
  for r in rows: w.writerow([r[k] for k in "election,pollster,date,n,blue_cand,blue_pct,green_cand,green_pct,undecided,source_url".split(",")])
def stat(e,mode="bg",excl=()):
  ps=[r for r in rows if r["election"]==e and r["pollster"]!="RESULT" and r["pollster"] not in excl]
  res=[r for r in rows if r["election"]==e and r["pollster"]=="RESULT"][0]
  def ratio(r):
    b=r["blue_pct"]; o=r["green_pct"] if mode=="bg" else r["third"]
    return None if o is None else 100*b/(b+o)
  v=[ratio(r) for r in ps if ratio(r) is not None]
  avg=sum(v)/len(v); act=ratio(res)
  print(f"{e} {mode} excl={excl} n={len(v)} poll={avg:.2f} [{min(v):.1f}-{max(v):.1f}] act={act:.2f} bias={act-avg:+.2f}")
  return act-avg
b14=stat("2014TPE")
b18=stat("2018TPE"); b18k=stat("2018TPE","bthird")
b22=stat("2022TPE"); stat("2022TPE",excl=("菱傳媒",)); stat("2022TPE","bthird")
b24=stat("2024PRES_NATL"); stat("2024PRES_NATL","bthird")
# raw averages
for e in ["2014TPE","2018TPE","2022TPE","2024PRES_NATL"]:
  ps=[r for r in rows if r["election"]==e and r["pollster"]!="RESULT"]
  print(e,"raw blue avg %.2f green avg %.2f"%(sum(r["blue_pct"] for r in ps)/len(ps), sum(r["green_pct"] for r in ps if r["green_pct"] is not None)/len([r for r in ps if r["green_pct"] is not None])), "third avg", (sum(r["third"] for r in ps if r["third"])/len([r for r in ps if r["third"]]) if any(r["third"] for r in ps) else "-"))
for name,bs in [("blue/(blue+green) 4 elections",[b14,b18,b22,b24]),("main-rival 2018=Ko",[b14,b18k,b22,b24])]:
  print(name,"mean %+.2f range %+.2f~%+.2f"%(sum(bs)/len(bs),min(bs),max(bs)))
