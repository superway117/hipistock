from BeautifulSoup import BeautifulSoup, SoupStrainer
from stockparser import Stock
class IfengStock(Stock):
    def __init__(self, stock_id,name=""):
        Stock.__init__(self,"Ifeng",stock_id,name)
		
    def produce_url(self,type):
        if self.get_stockid()== None :
			return None
        if type == "money":
            return "http://app.finance.ifeng.com/hq/trade/stock_zijin.php?code="+self.get_stockid()
        elif type == "info":
            return "http://finance.ifeng.com/app/hq/stock/"+self.get_stockid()+"/index.shtml"
		
    def get_stock_info_impl(self,page):
        result_hash={}
        links = SoupStrainer('div', attrs={"class" : "date_list01"})
        product_list_start = BeautifulSoup(page.content,parseOnlyThese=links)
        return product_list_start
        product_list = product_list_start.contents[0].table.findAll("tr")
        i=0
        list_len = len(product_list)
        for product in product_list: 
            item_list = product.findAll("td")
            i+=1
            """
            if i == 1:
                try:
                    result_hash["eps"] = item_list[1].string

                except AttributeError:
                    continue
                try:
                    result_hash["netasset"] = item_list[3].string

                except AttributeError:
                    continue
            """
            if i == 2:
                try:
                    result_hash["naer"] = product.contents[0].string
                except AttributeError:
                    continue
                try:
                    result_hash["expirate"] = product.contents[1].string
                except AttributeError:
                    continue
            elif i == 3:
                try:
                    result_hash["totalequity"] = item_list[0].string
                except AttributeError:
                    continue
                try:
                    result_hash["circulation"] = item_list[1].string
                except AttributeError:
                    continue
            elif i == 4:
                try:
                    result_hash["yesterdaygrowth"] = item_list[1].string
                except AttributeError:
                    continue
                try:
                    result_hash["weekgrowth"] = item_list[2].string
                except AttributeError:
                    continue
            elif i == 5:
                try:
                    result_hash["monthgrowth"] = item_list[0].string
                except AttributeError:
                    continue
                try:
                    result_hash["yeargrowth"] = item_list[1].string
                except AttributeError:
                    continue
        return result_hash
		
    def get_money_flow_impl(self,page):
		result_list=[]
		links = SoupStrainer('div', attrs={"class" : "tab01"})
		product_list_start = BeautifulSoup(page,parseOnlyThese=links)
		product_list = product_list_start.contents[0].table.findAll("tr")
		i=0
		list_len = len(product_list)
		for product in product_list: 
			if i == 0:
				i+=1
				continue
			i+=1
			item_list = product.findAll("td")
			result_hash ={}
			try:
				result_hash["date"] = product.td.string.strip().strip()				
			except AttributeError:
				continue
			try:
				result_hash["all"]  = item_list[1].span.string.strip()
			except AttributeError:
				continue
			try:
				result_hash["small"]  = item_list[2].span.string.strip()
			except AttributeError:
				continue
			try:
				result_hash["mediate"] = item_list[3].span.string.strip()
			except AttributeError:
				continue
			try:
				result_hash["large"] = item_list[4].span.string.strip()
			except AttributeError:
				continue
			try:
				result_hash["super"] = item_list[5].span.string.strip()
			except AttributeError:
				continue
			if i == list_len:
				result_list.append(result_hash)
				continue
			try:
				result_hash["volume"] = item_list[6].string.strip()
			except AttributeError:
				print "get volume error"
				continue
			try:
				result_hash["growth"] =  item_list[7].span.string.strip()
			except AttributeError:
				print "get growth error"
				continue
			result_list.append(result_hash)
		return result_list
        
if __name__ == '__main__': 
  main()