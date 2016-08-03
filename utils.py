#-*- coding: utf-8 -*-

import os

import urllib
import BeautifulSoup
import sys

# This function returns a title of url
# Input : url (e.g: http://...)
# Ouput : string (title)
def get_url_title(url):
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')

    data = urllib.urlopen(url)
    text = data.read()

    try :
        # charset encoding is utf-8
        decoded_text = text.decode('utf-8')
        soup = BeautifulSoup.BeautifulSoup(decoded_text)
        return soup.title.string if soup.title else "None-Title"
    except UnicodeDecodeError:
        try :
            # charset encoding is euc-kr
            decoded_text = text.decode('cp949')
            soup = BeautifulSoup.BeautifulSoup(decoded_text)
            if soup.title and soup.title.string:
                return soup.title.string
            title = soup.find("meta",  property="og:title")
            return title["content"] if title else "None-Title"
        except UnicodeDecodeError:
            # Unknow encoding type
            return "None-Title"

def getTerminalSize():
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])

def rjust(input_unicode, screen_width, fill):
    input_str = str(input_unicode.encode('utf-8'))

    # Calcalte length in case mixed string(eng and kor)
    str_length = (len(input_unicode) + len(input_str))/2
    return fill*(screen_width-str_length) + input_str

def transColor(str, color='\033[97m'):
    # default color is white
    ENDC = '\033[0m'

    return color+str+ENDC
