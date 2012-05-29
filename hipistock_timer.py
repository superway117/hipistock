import yaml
from ifengstock import IfengStock
from sinastock import SinaStock
import urllib2  
import sys
import threading

def set_proxy():
	enable_proxy = True  
	#proxy_handler = urllib2.ProxyHandler({"http" : 'http://proxyconf'})  
	proxy_handler = urllib2.ProxyHandler({"http" : '10.217.252.73:911'})
	null_proxy_handler = urllib2.ProxyHandler({})  
	  
	if enable_proxy:  
	    opener = urllib2.build_opener(proxy_handler)  
	else:  
	    opener = urllib2.build_opener(null_proxy_handler)  
	urllib2.install_opener(opener)  

def is_in_money_negative_growth(item):
	if item["all"][0] != '-' and item["growth"][0] == '-' :
		return True
	else:
		return False
def get_hot_level(money_list):
	first_item=money_list[0]
	
	level=0
	if is_in_money_negative_growth(first_item):
		level+=1
		sec_item=money_list[1]
		if is_in_money_negative_growth(sec_item):
			level+=1
			third_item=money_list[2]
			if is_in_money_negative_growth(third_item):
				level+=1
	return level 
	
def parse_all_plate():
	f=open("stock_list.yaml")
	data=yaml.load(f)
	for plate in data:
		print ("\n----------------------%s---------------------------------" % (plate))
		stock_list=data[plate]
		red =0
		green=0
		in_red_num =0
		in_green_num=0
		big_5_list=[]
		hot_list1=[]
		hot_list2=[]
		hot_list3=[]
		for stock in stock_list:
			ifeng_stock = IfengStock(stock[0],stock[1])
			money_list = ifeng_stock.get_money_flow()  
			
			list_len= len(money_list)
			
			if list_len > 1:
				hot=""
				first_item=money_list[0]
				level = get_hot_level(money_list)
				if level == 1:
					hot_list1.append(stock[1])
				elif level == 2:
					hot="HOT!!!"
					hot_list2.append(stock[1])
				elif level == 3:
					hot="HOT!!!!!!" 
					hot_list3.append(stock[1])
				if level > 0:
					print ("%s:%-6s\tAll:%-10s\tGrowth:%-5s\t%s" % (stock[0],stock[1],first_item["all"],first_item["growth"],hot))
					
				if first_item["growth"][0] != '-' :
					red+=1
					if first_item["growth"][0] >= '5' or (len(first_item["growth"].split('.')[0])==2) :
						big_5_list.append(stock[1])
				else:
					green+=1
				if first_item["all"][0] != '-' :
					in_red_num+=1
				else:
					in_green_num+=1
				
				"""
				i=0
				for item in money_list:
					i+=1
					print "Date:	"+item["date"]
					print "All:	"+item["all"]
					print "Small:	"+item["small"]
					print "Mediate:	"+item["mediate"]
					print "Large:	"+item["large"]
					print "Super:	"+item["super"]
						
					if i<list_len:
						print "Volume:	"+item["volume"]	
						print "Growth:	"+item["growth"]
				"""
		print ("Summary:")
		print (u"当天 %d 只股票涨, %d 只股票跌" % (red,green))	
		print (u"当天 %d 只股票资金流入, %d 只股票资金流出" % (in_red_num,in_green_num))	
		print (u"当天 %d 只股票涨幅超过5个点" % (len(big_5_list),))	
		if len(big_5_list)>0:
			print (u"涨幅超过5个点的股票有:")	
			for big_5_stock in big_5_list:	
				print (big_5_stock),
		if len(big_5_list)>0 and ((100*red)/(red+green))>=70 and ((100*in_red_num)/(in_red_num+in_green_num))>=70:
			print u"\n\n该板块是当前热门板块 HOT!!!"
		elif red<green and ((100*in_red_num)/(in_red_num+in_green_num))>=70:
			print u"\n该板块可能是下一个热门板块 HOT!!!"

	f.close
	
def get_stock_info(stock_str):
	f=open("stock_list.yaml")
	data=yaml.load(f)
	for plate in data:
		stock_list=data[plate]
		for stock in stock_list:
			if stock[0] == stock_str or stock[1] == stock_str or stock[2] == stock_str :
				sina_stock = SinaStock(stock[0],stock[1])
				info_list = sina_stock.get_stock_info()
				ifeng_stock = IfengStock(stock[0],stock[1])
				money_list = ifeng_stock.get_money_flow()  
				growth = (float(info_list['cur_price'])-float(info_list['close_price']))/float(info_list['close_price'])*100
				buy_num=float(info_list['buy_1_num'])+float(info_list['buy_2_num'])+float(info_list['buy_3_num'])+float(info_list['buy_4_num'])+float(info_list['buy_5_num'])
				sell_num=float(info_list['sell_1_num'])+float(info_list['sell_2_num'])+float(info_list['sell_3_num'])+float(info_list['sell_4_num'])+float(info_list['sell_5_num'])
				weibi=((buy_num-sell_num)/(buy_num+sell_num))*100
				print ("----------------------------------------------------------")	
				print (u"股票名称:%s\t%s %s" % (info_list['name'],info_list['date'],info_list['time']))	
				print (u"当前价格:%-10s\t跌涨幅:%f%%\t委比:%f%%" % (info_list['cur_price'],growth,weibi))
				if len(money_list) >=5:
					print (u"\n最近五天资金流向:")
					print (u"%-10s\t%-10s\t%-10s" % (money_list[0]['date'],money_list[0]['all'],money_list[0]['growth']))
					print (u"%-10s\t%-10s\t%-10s" % (money_list[1]['date'],money_list[1]['all'],money_list[1]['growth']))
					print (u"%-10s\t%-10s\t%-10s" % (money_list[2]['date'],money_list[2]['all'],money_list[2]['growth']))
					print (u"%-10s\t%-10s\t%-10s" % (money_list[3]['date'],money_list[3]['all'],money_list[3]['growth']))
					print (u"%-10s\t%-10s\t%-10s" % (money_list[4]['date'],money_list[4]['all'],money_list[4]['growth']))
				print
				print (u"开盘价  :%-10s\t上个交易日收盘价:%-10s" % (info_list['open_price'],info_list['close_price']))
				print (u"最高价  :%-10s\t最低价  :%-10s" % (info_list['highest_price'],info_list['lowest_price']))
				print (u"成交股数:%-10s\t成交金额:%-10s" % (info_list['deal_stock_num'],info_list['deal_money_num']))	
				print
				print (u"买一股数:%-10s\t买一报价:%-10s" % (info_list['buy_1_num'],info_list['buy_1_price']))	
				print (u"买二股数:%-10s\t买二报价:%-10s" % (info_list['buy_2_num'],info_list['buy_2_price']))
				print
				print (u"卖一股数:%-10s\t卖一报价:%-10s" % (info_list['sell_1_num'],info_list['sell_1_price']))	
				print (u"卖二股数:%-10s\t卖二报价:%-10s" % (info_list['sell_2_num'],info_list['sell_2_price']))	
				print
	f.close		


class PoolingQuery:
	def __init__(self,count):
		self.m_timer=threading.Timer(10,self.run)
		self.m_total_count=count
		self.m_run_count=0
		
	def start(self):
		if(self.m_run_count<self.m_total_count):
			self.m_timer.start()
			
	def restart(self):
		if(self.m_run_count<self.m_total_count):
			self.m_timer.cancel()
			self.m_timer=threading.Timer(10,self.run)
			self.m_timer.start()
			
	def run(self):
		if len(sys.argv) > 1:
			self.m_run_count+=1
			for stock in sys.argv[1:]:
				get_stock_info(stock)
			self.restart()
		
		
		
		
		
	
	

if __name__ == "__main__":
	set_proxy()
	query = PoolingQuery(10)
	query.start()