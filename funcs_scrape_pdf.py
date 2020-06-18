from tika import parser
from bs4 import BeautifulSoup
import requests


def get_index_all_ideas_lines(path_pdf):
    raw = parser.from_file(path_pdf)
    all_lines = raw['content'].splitlines()
    all_lines = [line for line in all_lines if line != '']

    return all_lines


def get_philosophical_domains(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.find('div', attrs = {'class': 'txt'})
    headers = table.find_all_next('td', attrs = {'class': 'gists'})
    
    domains = []
    for header in headers:
        substr_start = [idx for idx, x in enumerate(str(header)) if x == '>'][1]
        substr_end = str(header).index(' </a')
        domain = str(header)[(substr_start+1):substr_end]
        domains.append(domain)
    domains = [f'{i+1}. {j}' for i, j in zip(range(len(domains)), domains)]
        
    return domains


def write_domain_idea_ids(domain, domains, index_all_ideas_lines):

    start_idx = index_all_ideas_lines.index(domain) + 1
    end_idx = index_all_ideas_lines.index(domains[domains.index(domain) + 1])
    
    lines_desired = index_all_ideas_lines[start_idx:end_idx]
    lines_desired = [line for line in lines_desired if line[-1].isdigit()]
    idea_ids_desired = [int(line.split(']')[1]) for line in lines_desired]
    
    with open(f"./idea_ids_{domain.replace(' ', '_')}.txt", 'w') as f:
        for id in idea_ids_desired[:-1]:
            f.write('%s\n' % id)
        f.write('%s' % idea_ids_desired[-1])
        
    print(f'# of ideas: {len(idea_ids_desired)}')