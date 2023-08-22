from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

# Use the Chrome browser's WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless') 
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options)

def search_books(book_name):
    if not book_name:
        print("请传入要搜索的关键词")
        return
    # Construct the search link
    search_url = "https://search.douban.com/book/subject_search?search_text=" + book_name

    # Send the request
    driver.get(search_url)
    # 等待执行完，设置了headless之后，它不会等，需要显式的设置
    print("开始等待加载完...")
    while driver.execute_script("return document.readyState") != "complete":
        print("还没 ready...")
        sleep(1)
    print("加载完成！")
    
    html = driver.page_source
    # print("get html: ", html)
    soup = BeautifulSoup(html, "html.parser")

    # Find all search results
    result_list = soup.find_all("a", class_="cover-link")

    books = []
    # Output the search results
    if len(result_list) > 0:
        print("共找到%d条搜索结果：" % len(result_list))
        for result in result_list:
            url = result.get("href")
            cover_dom = result.find("img", class_="cover")
            cover = ''
            if cover_dom:
                cover = cover_dom.get("src")
                if cover:
                    cover = cover.strip()

            title = ''
            abstract = ''
            detail_dom = result.find_next_sibling("div", class_="detail")
            if detail_dom:
                title_dom = detail_dom.find("div", class_="title")
                if title_dom:
                    title = title_dom.get_text().strip()
                abstract_dom = detail_dom.find("div", class_="abstract")
                if abstract_dom:
                    abstract = abstract_dom.get_text().strip()
            abstract_dom = result.find("div", class_="abstract")
            if abstract_dom:
                abstract = abstract_dom.get_text().strip()

            book = {"title": title, "abstract": abstract, "url": url, "cover": cover}
            books.append(book)
    else:
        print("没有找到相关书籍，请尝试其他关键词。")

    # Save the search results to an Excel file
    # df = pd.DataFrame(books)
    # df.to_excel("book_search_results.xlsx", index=False)
    print(books)
    return books
