from lxml import html
import requests
from datetime import datetime
import smtplib


def magic_inside():
    #links u want to track
    page_list = [
        'http://www.imdb.com/title/tt1632701/episodes?season=6&ref_=tt_eps_sn_6',  #suits
        'http://www.imdb.com/title/tt1520211/episodes?season=7&ref_=tt_eps_sn_7',  #twd
        'http://www.imdb.com/title/tt2632424/episodes?season=4&ref_=tt_eps_sn_4',  #originals
        'http://www.imdb.com/title/tt2306299/episodes?season=5&ref_=tt_eps_sn_5',  #vikings
        'http://www.imdb.com/title/tt1405406/episodes?season=8&ref_=tt_eps_sn_8'  #tvd
    ]
    yesterday = ['\nZ WCZORAJ: \n']
    today = ['\nJUZ DZISIAJ: \n']
    tommorow = ['\nJUTRO: \n']
    for p in page_list:
        page = requests.get(p)
        tree = html.fromstring(page.content)
        ep_title = tree.xpath('//a[@class="subnav_heading"]/text()')
        ep_date = tree.xpath('//div[@class="airdate"]/text()')
        now_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for val in ep_date:
            ep_date_loop = datetime.strptime(val.strip().replace('.', ''), '%d %b %Y')
            diff = (now_date - ep_date_loop).days
            if diff == 1:
                yesterday.append('Byl nowy odcinek "%s" \n' % ep_title[0])
            if diff == 0:
                today.append('Premiera "%s" \n' % ep_title[0])
            if diff == -1:
                tommorow.append('Juz jutro nowy odcinek "%s" \n' % ep_title[0])

    msg = '%s%s%s' % (''.join(yesterday), ''.join(today), ''.join(tommorow))
    if msg == '\nZ WCZORAJ: \n\nJUZ DZISIAJ: \n\nJUTRO: \n':
        msg = ''
    return msg.encode("utf-8")



server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
#below insert login data and destination address
server.login("ur_gmail_acc", "pass")

server.sendmail("from_above_email_address", "to_email_address", magic_inside())
server.quit()


