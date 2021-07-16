import curses
import requests
from bs4 import BeautifulSoup

def main(stdscr):
    curses.curs_set(0)
    current_row = 0
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    print_news(stdscr, current_row)
    
    while 1:
        key = stdscr.getch()
        height = height_width(stdscr)

        if (key == curses.KEY_UP or key == 107) and current_row > 0:
            current_row -= 1
        elif (key == curses.KEY_DOWN or key == 106 ) and current_row < len(news_heading[:height])-1:
            current_row += 1

        print_news(stdscr, current_row)

def height_width(stdscr):
    h, w = stdscr.getmaxyx()
    if h > len(news_heading)-1:
        h = len(news_heading)-1
    return h

def print_news(stdscr, selected_row):
    stdscr.clear() 
    height = height_width(stdscr)

    for index, heading in enumerate(news_heading[:height]):
        if index == selected_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(index, 1, heading)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(index, 1, heading)
        
    stdscr.refresh()

def scrap():
    url = "https://www.bbc.com/"
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    global news_heading
    news_heading = []
    for news_header in soup.find("div", id="orb-modules").find_all("li"):
        try:
            x = news_header.find("div", class_="media__content").h3.a.string.strip()
        except AttributeError:
            pass
        else:
            news_heading.append(x) 

scrap()
curses.wrapper(main)
