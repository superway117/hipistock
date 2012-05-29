import os 
import urllib2

class Stock:
    def __init__(self, webname,stock_id,name):
		self.stock_id = stock_id.strip()
		self.name = name.strip()
		self.webname = webname
    
    def produce_url(self,type):
        return None
      
    def fetch(self,type):
		url = self.produce_url(type)
		if url==None:
			return None
        #try three times to fetch html page
		for index in range(0,5):
			try:
				page = urllib2.urlopen(url=url).read()
				return page
			except:
				if index == 4:
					print ("fetch %s error" % (self.name,))
					return None
				else:
					continue
					
    def get_stockid(self):
        if self.stock_id[0]=='6':
            return "sh"+self.stock_id
        elif self.stock_id[0]=='0':
		    return "sz"+self.stock_id
        return None
		
    def get_name(self):
        return self.name		
		
    def get_stock_info_impl(self,page):
        return []
		
    def get_money_flow_impl(self,page):
        return []
		
    def get_money_flow(self):
        page = self.fetch("money")
        if page != None:
            return self.get_money_flow_impl(page)
        else:
            return []
		
    def get_stock_info(self):
        page = self.fetch("info")
        if page != None:
            return self.get_stock_info_impl(page)
        else:
            return []
        
if __name__ == '__main__': 
  main()
        
