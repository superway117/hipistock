from BeautifulSoup import BeautifulSoup, SoupStrainer
from stockparser import Stock
class SinaStock(Stock):
	def __init__(self, stock_id,name=""):
		Stock.__init__(self,"Ifeng",stock_id,name)
		
	def produce_url(self,type):
		if self.get_stockid()== None :
			return None
		if type == "info":
			return "http://hq.sinajs.cn/list="+self.get_stockid()
		
	def get_stock_info_impl(self,page):
		result_hash={}
		info_index= page.find('=')
		if info_index== -1:
			return None
		info_str1 = page[info_index+2:len(page)-3]
		info_str = unicode(info_str1,'gbk','ignore')
		info_list = info_str.split(',')
		#for item in info_list:
		#	print (u"%s" % (unicode(item,'gbk','ignore'),))
		result_hash["name"] = info_list[0]
		result_hash["open_price"] = info_list[1]
		result_hash["close_price"] = info_list[2]
		result_hash["cur_price"] = info_list[3]
		result_hash["highest_price"] = info_list[4]
		result_hash["lowest_price"] = info_list[5]
		result_hash["deal_stock_num"] = info_list[8]  #6,7 also the buy first price and sell first price
		result_hash["deal_money_num"] = info_list[9]
		
		result_hash["buy_1_num"] = info_list[10]
		result_hash["buy_1_price"] = info_list[11]
		result_hash["buy_2_num"] = info_list[12]
		result_hash["buy_2_price"] = info_list[13]
		result_hash["buy_3_num"] = info_list[14]
		result_hash["buy_3_price"] = info_list[15]
		result_hash["buy_4_num"] = info_list[16]
		result_hash["buy_4_price"] = info_list[17]
		result_hash["buy_5_num"] = info_list[18]
		result_hash["buy_5_price"] = info_list[19]
		
		result_hash["sell_1_num"] = info_list[20]
		result_hash["sell_1_price"] = info_list[11]
		result_hash["sell_2_num"] = info_list[22]
		result_hash["sell_2_price"] = info_list[23]
		result_hash["sell_3_num"] = info_list[24]
		result_hash["sell_3_price"] = info_list[25]
		result_hash["sell_4_num"] = info_list[26]
		result_hash["sell_4_price"] = info_list[27]
		result_hash["sell_5_num"] = info_list[28]
		result_hash["sell_5_price"] = info_list[29]
		
		result_hash["date"] = info_list[30]
		result_hash["time"] = info_list[31]
		return result_hash
        
if __name__ == '__main__': 
  main()