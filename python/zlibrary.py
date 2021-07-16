import requests
import curses
from bs4 import BeautifulSoup

import time
start_time = time.time()

def input_validation():
    #search=input("Enter a book name: ")
    #search_url = "https://1lib.in/s/" + search
    search_url = "https://1lib.in/s/linux"
    scrap_data(search_url)

def scrap_data(url):

    print("Scraping Site...")

    count = 0
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    global book_name, file
    book_name, book_id, publisher, author, file, year, lang = ([] for _ in range(7))

    for data in soup.find_all("div", class_ = "resItemBox resItemBoxBooks exactMatch"):
        
        x = data.table.tr
        y = x.find("td", style="vertical-align: top;")
        z = x.find("div", class_ = "bookDetailsBox")

        book_id.append(x.td.a['href'])

        book_name.append(y.a.string)
        publisher.append(y.div.string)

        for authors in y.find("div", class_="authors"):
            temp = authors.string
            if temp == ", ":
                count = 1
            else:
                if count == 1:
                    count = 0
                    author[-1].append(temp)
                else:
                    author.append([temp])

        file.append(z.find("div", class_ = "bookProperty property__file").find("div", class_="property_value").string)

        try:
            year.append(z.find("div", class_ ="bookProperty property_year").find("div", class_="property_value").string)
        except AttributeError:
            year.append("")

        try:
            lang.append(z.find("div", class_ ="bookProperty property_language").find("div", class_="property_value").string)
        except AttributeError:
            lang.append("")

def main(stdscr):
    curses.curs_set(0)
    current_row = 0
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    print_screen(stdscr, current_row)

    while 1:
        key = stdscr.getch()
        h, w = height_width(stdscr)

        if (key == curses.KEY_UP or key == 107) and current_row > 0:
            current_row -=1
        elif (key == curses.KEY_DOWN or key == 106) and current_row < len(book_name[:h])-1:
            current_row += 1

        print_screen(stdscr, current_row)

def height_width(stdscr):
    h, w = stdscr.getmaxyx()
    if h > len(book_name)-1:
        h = len(book_name)-1
    return h, w

def print_screen(stdscr, selected_row):
    stdscr.clear()
    h, w = height_width(stdscr)

    sp_im = 30
    if w < 60:
        sp_im = 1
    
    for index, book in enumerate(book_name[:h]):
        if index == selected_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(index, sp_im, book[:w-sp_im])
            stdscr.attroff(curses.color_pair(1))    
        else:
            stdscr.addstr(index, sp_im, book[:w-sp_im])

    stdscr.refresh()
            


input_validation()
curses.wrapper(main)

print("--- %s seconds ---" % (time.time() - start_time))
