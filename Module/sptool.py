from __future__ import with_statement
import contextlib
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import sys


class spider:
    def __init__(self):
        pass

    def tiny(self, url):
        res_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url': url}))
        with contextlib.closing(urlopen(res_url)) as res:
            return res.read().decode('utf-8')

    def str2dict(self, str):
        str = str.replace("https://", "https#")
        str = str.replace("http://", "http#")
        strr = str.split("###")
        fin = dict()
        for item in strr:
            if item != "":
                temp = item.split(":")
                temp[1] = temp[1].replace("https#", "https://")
                temp[1] = temp[1].replace("http#", "http://")
                fin[temp[0].strip()] = temp[1].strip()
        return fin


    def temptxt(self, content, filename):
        with open(filename, 'w') as f:
            for i in content:
                f.write(i)


    # def Stripcomm(self, str):
    #     while 1:
    #         m = p.search(str)
    #         if m:
    #             mm = m.group()
    #             s = s.replace(mm, mm.replace(',', ''))
    #         else:
    #             break



if __name__ == '__main__':
    obj = spider()


    # for tinyurl in map(tiny, sys.argv[1:]):
    #     print(tinyurl)