import requests
from bs4 import BeautifulSoup
import random

url = 'https://arca.live/b/bluearchive/81644362'
response = None


def get_num_comment(soup):
    num_comment = soup.select_one('body > div.root-container > div.content-wrapper.clearfix > article > div > div.article-wrapper > div.article-head > div.info-row > div.article-info.article-info-section > span:nth-child(8)')
    return int(num_comment.get_text())

def get_candidates(soup, num_comment):
    candidates = []
    for i in range(1, num_comment + 1):
        try:
            comment = soup.select_one(f'#comment > div.list-area > div:nth-child({i}) > div > div > div > span > a')
            name = comment['data-filter']
        except:
            # 답글 때문에 불어난 숫자, no count
            print(f'Load done.')
            break
        if name == '불나무' or name in candidates:
            continue
        
        candidates.append((i, name))
    return candidates

def get_url_usr_info(user_name : str):
    us = user_name.split('#')
    base_url = 'https://arca.live/u/@'
    if len(us) == 1:
        url = base_url + us[0]
    else:
        url = base_url + us[0] + '/' + us[1]
    
    return url

def atari(candidates, n=1):
    """추첨 함수

    Args:
        candidates (list): list of tuple (index, name)
        n (int, optional): number of winners. Defaults to 1.
    """
    atari_indices = []
    while len(atari_indices) < n:
        atari_index = random.randint(0, len(candidates))
        if atari_index not in atari_indices:
            atari_indices.append(atari_index)
    print('Final: ')
    for atari_index in atari_indices:
        selected_name = candidates[atari_index][1]
        user_info_url = get_url_usr_info(selected_name)
        print(selected_name, user_info_url)
    print('')

def main():
    global response
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        
    else:
        print(response.status_code)
        return

    num_comment = get_num_comment(soup)
    candidates = get_candidates(soup, num_comment=num_comment)
    
    atari(candidates=candidates, n=2)
    
    

if __name__ == '__main__':
    main()
        