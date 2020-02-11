# coding=gbk
import requests
from Module import sptool
from pyquery import PyQuery as pq
from queue import Queue
from threading import Thread
import time
import pandas as pd

class Book:
    def __init__(self):
        self.Sp = sptool.spider()
        self.Url_list = []
        self.Room_thread_num = 15
        self.Roomdict = {}
        self.Room_Q = Queue()

    def Get_Room_Allpage(self):
        url = 'https://www.booking.com/searchresults.zh-tw.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaOcBiAEBmAEwuAEXyAEM2AEB6AEB-AELiAIBqAIDuAKCmuHpBcACAQ&sid=2c38f9fac2220ddab8a92ef1b092884a&tmpl=searchresults&checkin_month=9&checkin_monthday=1&checkin_year=2019&checkout_month=9&checkout_monthday=6&checkout_year=2019&city=-240905&class_interval=1&dest_id=-240905&dest_type=city&from_sf=1&group_adults=6&group_children=0&highlighted_hotels=4219946&label_click=undef&no_rooms=1&raw_dest_type=city&room1=A%2CA%2CA%2CA%2CA%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&src=searchresults&srpvid=e9f474a3154300e1&ss=%E5%A4%A7%E9%98%AA&ssb=empty&ssne=%E5%A4%A7%E9%98%AA&ssne_untouched=%E5%A4%A7%E9%98%AA&rows=20'
        self.Url_list.append(url)
        for i in range(1, 50):
            self.Url_list.append(url + '&offset={}'.format(i*20))
        self.Sp.temptxt(self.Url_list, 'urlist.txt')
        print(self.Url_list)
        return self.Url_list

    def Get_Room(self, url):
        headers = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3###Cache-Control: max-age=0###Connection: keep-alive###Host: www.booking.com###Sec-Fetch-Mode: navigate###Sec-Fetch-Site: none###Sec-Fetch-User: ?1###Upgrade-Insecure-Requests: 1###User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3###'
        headers = self.Sp.str2dict(headers)
        res = requests.get(url, headers=headers)
        data = pq(res.content.decode())
        rooms = data('div.sr_item.sr_item_new.sr_item_default.sr_property_block.sr_flex_layout')
        # print(rooms)
        for room in rooms:
            dlist = []
            name = pq(room)('span.sr-hotel__name').text()
            price = pq(room)('div.bui-price-display__value.prco-inline-block-maker-helper').text()
            price = price[4:].replace(',', '')
            rurl = pq(room)('a.b-button.b-button_primary.sr_cta_button').attr('href')
            bed = pq(room)('div.sr-group_recommendation__bed_wrapper--bigger').text()
            score = pq(room)('div.bui-review-score__badge').text()
            if not price:
                price = 0
                reurl = 0
                score = 0
            else:
                rurl = 'https://www.booking.com' + rurl
                reurl = self.Sp.tiny('https://www.booking.com' + rurl)

            dlist.append(int(price))
            dlist.append(rurl)
            dlist.append(reurl)
            dlist.append(bed)
            dlist.append(score)
            self.Roomdict[name] = dlist
        print(self.Roomdict)

    def Thread_Get_Room(self):
        while self.Room_Q.qsize() != 0:
            link = self.Room_Q.get()
            self.Get_Room(link)
            time.sleep(0.5)

    def Get_Room_Start_Thread(self):
        self.Get_Room_Allpage()
        for link in self.Url_list:
            self.Room_Q.put(link)
        for i in range(self.Room_thread_num):
            t = Thread(target=self.Thread_Get_Room)
            t.start()
        print('start to fetch data')
        total_mission = self.Room_Q.qsize()
        while self.Room_Q.qsize() != 0:
            print('loading: {}/{}'.format(self.Room_Q.qsize(), total_mission))
            time.sleep(1)
        print('\nclear')
        # print(self.Roomlist)

    def Dictrans(self, rdict):
        adict = {}
        name = []
        price = []
        url = []
        reurl = []
        bed = []
        score = []
        for i in rdict:
            if rdict[i][0] != 0:
                name.append(i)
                price.append(rdict[i][0])
                url.append(rdict[i][1])
                reurl.append(rdict[i][2])
                bed.append(rdict[i][3])
                score.append(rdict[i][4])
        adict['name'] = name
        adict['price'] = price
        adict['url'] = url
        adict['reurl'] = reurl
        adict['bed'] = bed
        adict['score'] = score
        return adict

    def Room2df(self, rdict):
        df = pd.DataFrame.from_dict(rdict)
        df = df.iloc[0:, 0:5]
        df.set_index('name', inplace=True)
        df.sort_values(by=['price'], ascending=True, inplace=True)
        print(df.head(10))
        return df

    def df2html(self, df):
        old_width = pd.get_option('display.max_colwidth')
        pd.set_option('display.max_colwidth', -1)
        export_html = df.to_html('Booking.html', escape=False, index=False, sparsify=True, border=0, index_names=False, header=False)
        pd.set_option('display.max_colwidth', old_width)
        return(export_html)


    def df2csv(self, df):
        export_csv = df.to_csv('Booking.csv')
        return export_csv



if __name__ == '__main__':
    obj = Book()
    # obj.Get_Room_Allpage()
    url = 'https://www.booking.com/searchresults.zh-tw.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaOcBiAEBmAEwuAEXyAEM2AEB6AEB-AELiAIBqAIDuAKCmuHpBcACAQ&sid=dede15a308d0eeca9483f7aee739e439&sb=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.zh-tw.html%3Faid%3D304142%3Blabel%3Dgen173nr-1FCAEoggI46AdIM1gEaOcBiAEBmAEwuAEXyAEM2AEB6AEB-AELiAIBqAIDuAKCmuHpBcACAQ%3Bsid%3Ddede15a308d0eeca9483f7aee739e439%3Bsb_price_type%3Dtotal%3Bsrpvid%3D4c975dacefd2008c%26%3B&ss=%E5%A4%A7%E9%98%AA&is_ski_area=0&checkin_year=2019&checkin_month=9&checkin_monthday=18&checkout_year=2019&checkout_month=9&checkout_monthday=28&group_adults=6&group_children=0&no_rooms=2&b_h4u_keep_filters=&from_sf=1&ss_raw=%E5%A4%A7%E9%98%AA&search_pageview_id=15f16c448ff200d9'
    obj.Get_Room(url)


    # obj.Get_Room_Start_Thread()
    # # print(obj.Roomdict)
    # rdict = obj.Roomdict
    # newdict = obj.Dictrans(rdict)
    # df = obj.Room2df(newdict)
    # export_csv = obj.df2csv(df)
    #
    # # print(df)
    # # export_html = obj.df2html(df)







