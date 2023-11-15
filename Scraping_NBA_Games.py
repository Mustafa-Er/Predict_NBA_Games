import os # Import os module
from bs4 import BeautifulSoup, Comment #Import BeautifulSoup module
import requests #Import requests module
import time #Import time module


current_file = os.path.abspath("")
data_dir = "data-nbagames"
standings_dir = os.path.join(data_dir, "standings")
scores_dir = os.path.join(data_dir, "scores")
seasons = list(range(2016, 2025))




def get_html(url: str, sleep: int = 10, retries: int = 3):
    """
    This function allows us to retrieve the text in the html with the desired number of trials

    Parameters:
        url: url which will be download
        sleep: seconds to sleep
        retries: numebr of trials
    
    """
    html_content = None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,\
        #    image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        #"Accept-Encoding" : "gzip, deflate, br",
        #"Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        #"Cache-Control" : "max-age=0",
        #"Cookie" : "__qca=P0-1865254990-1698072165035; _pbjs_userid_consent_data=3524755945110770;\
        #    cookie=d7a81a55-0183-499e-bc2b-5aeb22462916; _gcl_au=1.1.1605865564.1698072166;\
        #        au_1d=AU1D-0100-001698072166-NHTSF44V-EM1D; _cc_id=a02080bf5a1c80078b7eae58a82f9357;\
        #            hubspotutk=80aedd67f612767a0feea1e0b4fb6e82; _fbp=fb.1.1698072192360.963113386;\
        #                sr_note_box_countdown=69; srcssfull=yes; is_live=true;\
        #                    _ga_NR1HN85GXQ=GS1.1.1698257508.3.0.1698257508.60.0.0;\
        #                        _ga_80FRT7VJ60=GS1.1.1698257508.3.0.1698257508.60.0.0;\
        #                            __hstc=180814520.80aedd67f612767a0feea1e0b4fb6e82.1698072191932.1698095928193.1698257509916.3; \
        #                                __hssrc=1;\
        #                                    _au_last_seen_pixels=eyJhcG4iOjE2OTgyNTc1MTEsInR0ZCI6MTY5ODI1NzUxMSwicHViIjoxNjk4MjU3NTExLCJydWIiOjE2OTgyNTc1MTEsInRhcGFkIjoxNjk4MjU3NTExLCJhZHgiOjE2OTgyNTc1MTEsImdvbyI6MTY5ODI1NzUxMSwiaW1wciI6MTY5ODA3MjE2NiwiYW1vIjoxNjk4MjU3NTExLCJpbmRleCI6MTY5ODI1NzUxMSwiYWRvIjoxNjk4MDcyNzMyLCJjb2xvc3N1cyI6MTY5ODA3MjczMiwic21hcnQiOjE2OTgwNzI3MzIsImJlZXMiOjE2OTgwNzI3MzIsInBwbnQiOjE2OTgwNzI3MzIsInVucnVseSI6MTY5ODA3MjczMiwidGFib29sYSI6MTY5ODI1NzUxMSwic29uIjoxNjk4MDcyNzMyLCJvcGVueCI6MTY5ODA3MjczMn0%3D; _ga=GA1.2.391566569.1698072165; _gid=GA1.2.1886221910.1698257511; cto_bundle=Hp-WDV9teDNQdTdqbFh3YUxYb3JlTUN0YWZ1R0tDZEJMQXduOHMlMkJqRDJla0o3RWZWUGZKajAlMkZzZ29acjZvNmdsMlJKaldwUkowNzJIWmlMb2JBJTJGYXZjWXI5aThvNE12STR4bE5VbFI4RmRnWjJXN1dqMzVjSjFxUlFPVzliZGlBRWphS2xPeTUlMkZDbXh1NFRzRmNmb1dYN0VqTFd3Q2hHYXozcVFlN05NUUp1RFF6byUzRA; cto_bidid=__aaEF94aGQ5SmlhTHNxR3EwRGtDZ2JaQnYlMkJzSU5YNFRFSzZmalJwSG1TJTJGc0kzTDVWMk9ldUlzTUdQckNzNVVVNFRGV0h6YkJBTCUyRkZZNlNlOHR6WCUyQlZlVVZQYVllOCUyRnA0JTJGS2wwQ1dXU0o1dnVXUXY3aHNJNVk1UDEwakQ2aSUyRjhDQ2Fm; panoramaId_expiry=1698343912632; panoramaId=f16041dc3403fd50e0f63db8baefa9fb927a0f299dbdbade0380e82f9a6c429c; panoramaIdType=panoDevice; __gads=ID=e55d246d224e6d9f-221948a3d7e700ab:T=1698072166:RT=1698259529:S=ALNI_MYJ90U6f1o1c8-iF0MFt04AsrJMgw; __gpi=UID=00000ca05bd3b563:T=1698072166:RT=1698259529:S=ALNI_MZrCTYdrsR0HLTKxBPaGYbyOyKu4g",
        #"Sec-Ch-Ua" : "\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
        #"Upgrade-Insecure-Requests": "1",
        #"Sec-Fetch-User": "?1",
        #"Sec-Fetch-Site": "none",
        #"Sec-Fetch-Mode": "navigate",
        #"Sec-Fetch-Dest": "document",
        #"Sec-Ch-Ua-Mobile": "?0"

    }
    for i in range(1, retries+1):
        time.sleep(sleep * i)
        try:
            html_content = requests.get(url, headers=headers, timeout = 10).content
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
        except KeyboardInterrupt:
            print("Someone closed the program")
        else:
            break
    return html_content
def scrape_season(season: int):

    """
    This function downloads the NBA season games month by month and saves them in files

    Parameters:
        season: season which will be download
    
    
    """
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_games.html"

    html_content = get_html(url)
    soup = BeautifulSoup(html_content, "lxml")
    contentid_divtag = soup.find("div", id = "content")
    filterclass_divtag = contentid_divtag.find("div", class_ = "filter")
    links = filterclass_divtag.find_all("a")
    standings_pages = [f"https://www.basketball-reference.com{l['href']}" for l in links]

    for url in standings_pages:
        save_path = os.path.join(standings_dir, url.split("/")[-1])
        if os.path.exists(save_path):
            #print(f"{save_path} already exist in folder")
            continue
        
        
        html_content = get_html(url)
        soup = BeautifulSoup(html_content, "lxml")
        allschedule_divtag = soup.find("div", id = "all_schedule").prettify()
        try:
            with open(save_path, "w+", encoding = "utf-8") as f:
                f.write(allschedule_divtag)
                print(f"{save_path} saved succesfully")
    
        except Exception as e:
            print(e)
            continue


#Get the list of directories which files donwloaded 
standings_files = os.listdir(standings_dir)



def scrape_game(standing_file: str):

    """
    This function takes all the details of the matches in the standings folder and 
    saves them in the scores folder
    
    Parameter:

        standing_file: File with the month of the matches we will download
    
    """
    with open(standing_file, 'r') as f:
        html = f.read()

  
    soup = BeautifulSoup(html, "lxml")
    links = soup.find_all("a") 
    hrefs = [l.get('href') for l in links] 
    box_scores = [f"https://www.basketball-reference.com{l}" for l in hrefs if l and "boxscore" in l and '.html' in l]
    for url in box_scores:
        save_path = os.path.join(scores_dir, url.split("/")[-1])
        if os.path.exists(save_path):
            #print(f"{save_path} already exist in folder")
            continue
            

        html_content = get_html(url)
        soup = BeautifulSoup(html_content, "lxml")
        divlinecore = soup.find("div", id = "div_line_score")
        tbodies = soup.find_all('tbody')
        if tbodies:
            for tbody in tbodies:
                tbody.insert_before('\n' + ' ' * 4)
        contentid_divtag = soup.find("div", id = "content").prettify()
        if not contentid_divtag:
            continue
        with open(save_path, "w+", encoding="utf-8") as f:
            f.write(contentid_divtag)
            print(f"{save_path} saved succesfully")



def download_all_file(seasons:list):
    """
    This function downloads the data for the matches in the files for the desired season

        files: Match folder names
        seasons: Seasons which will be download
    
    """
    
    for season in seasons:
        scrape_season(season)

    for season in seasons:
        files = [s for s in standings_files if str(season) in s]
    
    for f in files:
        filepath = os.path.join(standings_dir, f)
        scrape_game(filepath)
    
    

def update_score_file(file: str, season:int):
    """
    This function downloads the data for the matches in the file for the desired month of season

    Parameters:
        file: Folder name corresponding to one month
        season: the Season of that month
    """
    try:
        os.remove(file)
        scrape_season(season)
        scrape_game(file)
    except:
        f"{file} did not updated!!!!!!!!!!!!!!!!!!!!!!!"
    


#for example: Run the update_score_file function 
#update_score_file(os.path.join(standings_dir, "NBA_2023_games-april.html"), 2023)

#Run the download_all_file function
download_all_file(seasons=seasons)