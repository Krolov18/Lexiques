import bs4


def main():
    x = bs4.BeautifulSoup(open("test1.html"), 'lxml').find_all("input")
    print(x)

if __name__ == '__main__':
    main()
