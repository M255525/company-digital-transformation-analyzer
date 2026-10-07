# 企業數位轉型分析（公司版）：範例資料（全虛構）＋獨立 Python 模型核對
import json, io, sys

def T(id, name, cat, people, freq, minutes, level, potential, difficulty, tool, toolCost, setupCost, learnHours):
    # toolCost＝系統月費；setupCost＝一次性導入費（建置／顧問）；learnHours＝每人訓練時數
    return dict(id=id, name=name, categoryId=cat, people=people, freq=freq, minutes=minutes, level=level, potential=potential,
                difficulty=difficulty, tool=tool, toolCost=toolCost, setupCost=setupCost, learnHours=learnHours)

def C(id, name, target):
    return dict(id=id, name=name, targetPct=target)

def G(salary, employees, alert, cap, budget, std=40, hours=176):
    return dict(monthlySalary=salary, monthlyHours=hours, employees=employees, weeklyStdHours=std, alertHours=alert, capEnabled=cap, toolBudget=budget)

def S(strategy, process, cloud, data, auto, security, people, customer):
    return dict(strategy=strategy, process=process, cloud=cloud, data=data, auto=auto, security=security, people=people, customer=customer)

def P(id, emoji, label, blurb, g, skills, cats, tasks):
    o = dict(g); o.update(skills=skills, categories=cats, tasks=tasks)
    return dict(id=id, emoji=emoji, label=label, blurb=blurb, overrides=o)

PRESETS = [
  P("accounting", "⚖️", "會計師事務所", "記帳、申報多已上雲端並導入自動匯入，示範健康的數位化基準。",
    G(55000, 20, 8, True, 300000), S(4,4,4,4,3,4,4,3),
    [C("cat1","記帳",60), C("cat2","稅務申報",70), C("cat3","客戶服務",50), C("cat4","行政",50)],
    [T("t1","客戶單據收件","cat1",4,10,15,2,60,1,"雲端收件匣＋OCR 辨識",1500,0,2),
     T("t2","傳票登打","cat1",4,20,10,3,60,2,"銀行明細自動匯入",2000,20000,3),
     T("t3","營業稅申報","cat2",3,4,40,3,50,3,"申報軟體批次匯入",0,0,4),
     T("t4","客戶詢問回覆","cat3",4,30,5,2,40,1,"常見問答＋AI 回覆草稿",800,0,2),
     T("t5","帳務報告寄送","cat3",2,10,15,2,60,1,"報告自動排程寄送",0,0,1),
     T("t6","收款追蹤","cat4",1,5,20,2,60,2,"應收帳款自動提醒",0,0,2),
     T("t7","員工工時計費","cat4",1,1,120,2,60,2,"工時計費系統（既有授權）",0,0,2)]),
  P("trading", "🚢", "貿易公司", "報價、訂單、出貨文件靠 Excel 與 Email，簡單改就能省下大量人時。",
    G(52000, 25, 6, False, 0), S(3,2,3,2,1,3,3,2),
    [C("cat1","業務",70), C("cat2","進出口作業",65), C("cat3","財務",70), C("cat4","管理",65)],
    [T("t1","報價單製作","cat1",4,8,30,1,65,2,"報價範本＋CRM 自動編號",1200,0,2),
     T("t2","客戶詢價信回覆","cat1",4,30,6,2,40,1,"信件範本＋AI 草稿",0,0,2),
     T("t3","訂單登打","cat2",2,20,15,0,75,2,"訂單表單串接 ERP",0,30000,3),
     T("t4","出貨文件製作","cat2",2,10,40,1,60,3,"文件範本自動帶入",0,60000,6),
     T("t5","匯款與帳款核對","cat3",1,10,20,1,60,2,"網銀匯出＋對帳公式",0,0,4),
     T("t6","費用報銷","cat4",1,1,120,1,60,1,"雲端報帳表單",500,0,1),
     T("t7","業績週報","cat1",1,1,180,1,75,2,"CRM 儀表板",0,0,6)]),
  P("manufacturing", "🏭", "製造業工廠", "工單、品檢、盤點仍用紙本，改善要靠 ERP／條碼投資，回收期較長。",
    G(48000, 80, 8, True, 800000), S(2,3,2,2,1,2,2,2),
    [C("cat1","生產",60), C("cat2","品管",60), C("cat3","採購倉儲",65), C("cat4","管理部",70)],
    [T("t1","生產工單開立（紙本）","cat1",3,15,20,0,70,3,"ERP 工單模組＋條碼",3000,120000,6),
     T("t2","生產日報彙整","cat1",2,5,45,1,75,2,"現場平板回報＋自動彙整",800,20000,3),
     T("t3","品檢紀錄登打","cat2",4,10,15,0,70,2,"平板檢驗表單",600,15000,2),
     T("t4","異常追蹤","cat2",2,5,30,1,50,3,"異常單系統＋自動通知",0,30000,4),
     T("t5","物料請購比價","cat3",2,8,30,1,50,3,"ERP 請購簽核",0,40000,6),
     T("t6","倉庫盤點","cat3",4,1,240,0,60,4,"條碼盤點＋倉儲系統",5000,250000,8),
     T("t7","出勤加班計算","cat4",1,1,300,1,80,2,"雲端打卡＋薪資系統",2500,10000,4),
     T("t8","月結報表","cat4",2,1,360,1,60,4,"BI 月結儀表板",1500,80000,16)]),
  P("retail", "🛍️", "連鎖零售", "POS 已上線，但排班、盤點仍靠店長手工，門市盤點最耗人力。",
    G(42000, 60, 8, True, 450000), S(3,3,3,3,2,3,2,4),
    [C("cat1","門市營運",60), C("cat2","商品採購",70), C("cat3","行銷會員",75), C("cat4","總部管理",70)],
    [T("t1","門市排班","cat1",6,1,180,1,70,2,"線上排班系統",3000,0,3),
     T("t2","每日營收回報","cat1",6,6,20,2,70,1,"POS 自動日報",0,0,1),
     T("t3","門市盤點","cat1",12,1,180,1,60,3,"手持條碼盤點",2000,150000,4),
     T("t4","補貨訂單","cat2",2,5,40,2,60,3,"POS 庫存自動建議量",0,80000,6),
     T("t5","會員活動推播","cat3",2,2,60,3,50,2,"會員分眾推播",2000,0,3),
     T("t6","促銷海報製作","cat3",1,3,90,2,50,1,"設計平台範本＋AI",600,0,4),
     T("t7","銷售分析報表","cat4",1,1,240,2,70,3,"BI 儀表板（既有授權）",0,60000,12)]),
  P("fnb", "🍜", "餐飲連鎖", "叫貨、盤點、排班多用紙本與群組訊息，手工警示最多。",
    G(40000, 45, 6, True, 200000), S(2,2,2,2,1,2,2,3),
    [C("cat1","門店營運",55), C("cat2","中央廚房",60), C("cat3","人事行政",65), C("cat4","行銷外送",70)],
    [T("t1","每日叫貨","cat1",5,6,20,0,70,2,"線上叫貨系統",1500,20000,2),
     T("t2","食材盤點","cat1",5,1,120,0,60,3,"平板盤點表＋庫存系統",1000,30000,3),
     T("t3","排班與換班","cat3",5,1,120,1,70,1,"排班 App",2000,0,2),
     T("t4","衛生檢核表","cat1",5,7,10,0,60,1,"線上檢核表單",0,0,1),
     T("t5","中央廚房生產排程","cat2",1,6,45,1,50,3,"排程試算表＋需求預測",0,40000,8),
     T("t6","外送平台對帳","cat4",1,4,60,1,70,2,"平台報表匯入對帳範本",0,0,3),
     T("t7","薪資計算","cat3",1,1,300,1,70,3,"薪資系統串打卡",1500,15000,6)]),
  P("logistics", "🚚", "物流倉儲", "點收、盤點、簽收全靠紙本，成熟度最低，釋放人力也最多。",
    G(42000, 70, 8, True, 1000000), S(1,2,1,2,1,2,1,2),
    [C("cat1","倉儲作業",55), C("cat2","運輸調度",60), C("cat3","客服",65), C("cat4","管理",60)],
    [T("t1","進貨點收","cat1",6,10,20,0,70,3,"手持掃碼點收",2000,120000,3),
     T("t2","揀貨單列印分派","cat1",3,15,15,1,60,2,"倉儲系統波次揀貨",3000,100000,4),
     T("t3","庫存盤點","cat1",8,1,240,0,60,4,"條碼／RFID 盤點",4000,300000,6),
     T("t4","派車調度","cat2",2,5,60,1,50,4,"路線規劃系統",5000,150000,10),
     T("t5","簽收單整理","cat2",2,5,40,0,70,2,"電子簽收 App",1500,30000,2),
     T("t6","貨況查詢回覆","cat3",3,40,4,1,60,1,"貨況查詢頁＋自動回覆",500,20000,2),
     T("t7","運費請款對帳","cat4",1,4,90,1,60,2,"對帳範本＋Power Query",0,0,8)]),
  P("clinic", "🏥", "診所", "看診系統完整，但預約、提醒、衛教仍靠電話與口頭說明。",
    G(50000, 15, 5, True, 150000), S(3,3,3,2,2,4,2,3),
    [C("cat1","掛號櫃台",65), C("cat2","醫護",60), C("cat3","行政",60)],
    [T("t1","電話預約掛號","cat1",2,60,4,1,60,1,"線上預約掛號系統",1500,10000,2),
     T("t2","回診提醒電話","cat1",1,40,4,0,80,1,"簡訊／LINE 自動提醒",800,0,1),
     T("t3","衛教資料說明","cat2",3,40,5,1,40,2,"衛教影片＋QR Code",0,15000,2),
     T("t4","耗材盤點","cat3",1,1,120,0,60,2,"庫存表單＋安全存量提醒",0,0,2),
     T("t5","健保申報整理","cat3",1,1,240,3,50,3,"申報系統檢核",0,0,4),
     T("t6","人員排班","cat3",1,1,180,1,70,2,"排班系統",800,0,2),
     T("t7","病歷摘要撰寫","cat2",2,60,3,2,50,4,"語音轉文字（需符合個資規範）",3000,50000,6)]),
  P("education", "🏫", "補習班", "點名、批改、家長溝通都靠人工，自動通知就是速贏。",
    G(40000, 18, 5, True, 100000), S(2,2,3,2,1,2,3,3),
    [C("cat1","招生",65), C("cat2","教務",60), C("cat3","班務",60), C("cat4","財務",65)],
    [T("t1","點名與出缺勤通知","cat3",4,15,10,0,75,1,"QR 簽到＋自動通知家長",800,0,1),
     T("t2","繳費通知與對帳","cat4",1,10,20,1,70,1,"線上繳費＋自動對帳",1000,10000,2),
     T("t3","試卷批改登分","cat2",4,10,20,1,50,2,"線上測驗自動批改",1500,0,3),
     T("t4","家長溝通回覆","cat3",4,40,4,1,40,1,"官方帳號＋常見問答",800,0,2),
     T("t5","招生活動報名","cat1",2,5,20,2,60,1,"線上報名表",0,0,1),
     T("t6","排課","cat2",1,1,180,1,60,3,"排課系統",1000,20000,4)]),
  P("ecommerce", "🛒", "電商品牌", "自動化程度最高，但系統訂閱疊太多：年費超過預算，也高於省下的人力成本。",
    G(55000, 22, 6, True, 200000), S(4,4,5,4,3,3,4,5),
    [C("cat1","營運",75), C("cat2","行銷",80), C("cat3","客服",75), C("cat4","財務",70)],
    [T("t1","訂單出貨處理","cat1",2,30,10,3,60,2,"訂單系統自動拋單",4000,0,2),
     T("t2","商品上架文案","cat2",2,8,40,3,60,1,"AI 文案生成",2000,0,3),
     T("t3","廣告成效報表","cat2",1,3,90,2,70,3,"廣告數據自動儀表板",3000,40000,10),
     T("t4","客服訊息回覆","cat3",3,60,3,3,50,2,"AI 客服機器人",6000,30000,4),
     T("t5","退換貨處理","cat3",2,10,15,2,60,2,"退貨自助申請頁",1500,20000,2),
     T("t6","多平台對帳","cat4",1,4,60,1,70,2,"多平台對帳工具",2500,0,4),
     T("t7","社群排程發布","cat2",1,10,15,3,60,1,"社群排程工具",1200,0,1)]),
  P("construction", "🏗️", "營建工程", "工地日報、估驗請款靠紙本，需要較大投資，回收期最長。",
    G(55000, 40, 6, True, 1000000), S(2,2,2,2,1,2,2,2),
    [C("cat1","工地現場",55), C("cat2","工務管理",60), C("cat3","採購發包",65), C("cat4","財務行政",65)],
    [T("t1","施工日報","cat1",4,5,40,0,70,3,"工地 App 日報＋照片",3000,80000,4),
     T("t2","工地照片整理","cat1",4,5,20,1,70,2,"雲端相簿自動歸檔",500,0,1),
     T("t3","進度會議資料","cat2",2,1,180,1,50,3,"專案管理系統",4000,120000,10),
     T("t4","估驗請款","cat4",2,2,180,1,60,4,"請款系統串預算",3000,200000,12),
     T("t5","材料詢價發包","cat3",2,5,40,1,50,3,"電子詢價平台",2000,50000,6),
     T("t6","工安檢查表","cat1",3,5,15,0,60,1,"線上檢查表＋缺失追蹤",0,0,1),
     T("t7","變更設計文件","cat2",2,2,60,1,40,4,"BIM 協作平台",5000,250000,30)]),
]

SKILL_IDS = ["strategy","process","cloud","data","auto","security","people","customer"]

def model(o):
    rate = o["monthlySalary"] / o["monthlyHours"]
    rows = []
    for t in o["tasks"]:
        wh = t["people"] * t["freq"] * t["minutes"] / 60
        saved = wh * t["potential"] / 100 * (1 - t["level"] / 4)
        mval = saved * 52 / 12 * rate
        net = mval - t["toolCost"]
        once = t["setupCost"] + t["people"] * t["learnHours"] * rate
        pay = (0 if once == 0 else once / net) if net > 0 else None
        alert = "urgent" if (t["level"] == 0 and wh >= o["alertHours"]) else ("watch" if (t["level"] <= 1 and wh >= o["alertHours"]) else None)
        rows.append(dict(name=t["name"], wh=wh, saved=saved, mval=mval, net=net, once=once, pay=pay, alert=alert, diff=t["difficulty"], level=t["level"], cost=t["toolCost"], setup=t["setupCost"]))
    n = len(rows); avg = sum(r["saved"] for r in rows) / n
    for r in rows:
        hi = r["saved"] > 0 and r["saved"] >= avg; easy = r["diff"] <= 2
        r["q"] = "later" if r["saved"] <= 0 else (("quick" if easy else "invest") if hi else ("tidy" if easy else "later"))
    tw = sum(r["wh"] for r in rows); sv = sum(r["saved"] for r in rows)
    taskPct = sum(r["wh"] * r["level"] / 4 for r in rows) / tw * 100
    sk = o["skills"]; skillPct = (sum(sk[k] for k in SKILL_IDS) / 8 - 1) / 4 * 100
    mval = sum(r["mval"] for r in rows); cost = sum(r["cost"] for r in rows); once = sum(r["once"] for r in rows)
    net = mval - cost; setup = sum(r["setup"] for r in rows)
    firstYear = setup + cost * 12
    return dict(rate=round(rate, 2), wh=tw, saved=sv, fte=sv / o["weeklyStdHours"], coverage=tw / (o["employees"] * o["weeklyStdHours"]) * 100,
                annualValue=mval * 12, annualFee=cost * 12, annualNet=net * 12, once=once, payback=(once / net if net > 0 else None),
                firstYear=firstYear, overBudget=bool(o["capEnabled"] and o["toolBudget"] > 0 and firstYear > o["toolBudget"]),
                mat=taskPct * 0.6 + skillPct * 0.4, manual=sum(r["wh"] for r in rows if r["level"] <= 1) / tw * 100,
                urgent=sum(r["alert"] == "urgent" for r in rows), watch=sum(r["alert"] == "watch" for r in rows),
                quads={q: [r["name"] for r in rows if r["q"] == q] for q in ["quick","invest","tidy","later"]},
                negNet=[r["name"] for r in rows if r["cost"] > 0 and r["net"] < 0])

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    for p in PRESETS:
        m = model(p["overrides"])
        q = {k: len(v) for k, v in m["quads"].items()}
        print(f"{p['label']:7} wh={m['wh']:.1f} saved={m['saved']:.1f} fte={m['fte']:.2f} cov={m['coverage']:.0f}% "
              f"年省={m['annualValue']:.0f} 年費={m['annualFee']:.0f} 年淨={m['annualNet']:.0f} 投入={m['once']:.0f} "
              f"回收={m['payback'] and round(m['payback'],1)} 首年={m['firstYear']:.0f} 超預算={m['overBudget']} "
              f"成熟={m['mat']:.1f} 手工={m['manual']:.0f}% 警示={m['urgent']}/{m['watch']} q={q} neg={m['negNet']}")
