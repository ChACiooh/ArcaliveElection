import requests
from bs4 import BeautifulSoup
import random

url = 'https://arca.live/b/bluearchive/81807113'
response = None


def get_num_comment(soup):
    num_comment = soup.select_one('body > div.root-container > div.content-wrapper.clearfix > article > div > div.article-wrapper > div.article-head > div.info-row > div.article-info.article-info-section > span:nth-child(8)')
    return int(num_comment.get_text())

def get_n_comment_pages(soup):
    comment_page = soup.select('#comment > div.pagination-wrapper.my-2 > ul')
    if len(comment_page) > 0:
        return int(comment_page[0].getText().split()[-1])
    
    return 1

def get_candidates(soup, num_comment):
    candidates = []
    invalid_candidate = 0
    for i in range(1, num_comment + 1):
        try:
            comment = soup.select_one(f'#comment > div.list-area > div:nth-child({i}) > div > div > div > span > a')
            name = comment['data-filter']
        except:
            # 답글이 있을 경우 전체 댓글 수에 집계되지 않기 때문에 예외 처리
            print(f'{i - invalid_candidate} people Load done.')
            break
        if name in candidates:
            invalid_candidate += 1
            continue
        elif name == '불나무':
            # 종료
            print(f'{i - invalid_candidate} people Load done.')
            break
        
        candidates.append((i - invalid_candidate, name))
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
    if len(candidates) < n:
        print('Error: given candidates are less than total winners')
        return
    
    atari_indices = []
    while len(atari_indices) < n:
        atari_index = random.randint(0, len(candidates))
        if atari_index not in atari_indices:
            atari_indices.append(atari_index)
            
    result_text = 'Winners:' if n > 1 else 'Winner:'
    print(result_text)
    for atari_index in atari_indices:
        selected_name = candidates[atari_index][1]
        user_info_url = get_url_usr_info(selected_name)
        print(selected_name, user_info_url)
    print('')
    
def get_soup_obj(url):
    global response
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    else:
        print(response.status_code)
    return None

def print_all_candidates(candidates):
    for c in candidates:
        print(c[1])

def main():
    soup = get_soup_obj(url)
    if soup == None:
        return

    n_cmnt_pages = get_n_comment_pages(soup)
    candidates = []
    for ncp in range(1, n_cmnt_pages + 1):
        soup = get_soup_obj(url + f'?cp={ncp}#comment')
        if soup == None:
            break
        num_comment = get_num_comment(soup)
        nth_candidates = get_candidates(soup, num_comment=num_comment)
        candidates += nth_candidates
    
    total_people = len(candidates)
    print(f'Total {total_people} people have participated.')
    atari(candidates=candidates, n=2)
    # print_all_candidates(candidates=candidates)
    
    

if __name__ == '__main__':
    main()
        
