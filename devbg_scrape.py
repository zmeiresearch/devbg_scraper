#!/usr/bin/env python3

import click
import requests
from bs4 import BeautifulSoup
import os
import shutil
import validators
import re
import urllib.request
import lxml
import time
import csv
from alive_progress import alive_bar

company_lists_test = [
        "https://dev.bg/company/it-employees/10-30/",
        "https://dev.bg/company/select/locationruse/",
        ]

company_lists = [
        "https://dev.bg/company/",
        "https://dev.bg/company/select/locationsofia/",
        "https://dev.bg/company/select/locationplovdiv/",
        "https://dev.bg/company/select/locationvarna/",
        "https://dev.bg/company/select/locationburgas/",
        "https://dev.bg/company/select/locationruse/",
        "https://dev.bg/company/headquarters/v-balgaria/",
        "https://dev.bg/company/headquarters/v-chuzhbina/",
        "https://dev.bg/company/it-employees/1-9/",
        "https://dev.bg/company/it-employees/10-30/",
        "https://dev.bg/company/it-employees/31-70/",
        "https://dev.bg/company/it-employees/70/",
        "https://dev.bg/company/company-activity/produktovi-kompanii/",
        "https://dev.bg/company/company-activity/it-konsultirane/",
        "https://dev.bg/company/company-activity/survis-kompanii/",
        "https://dev.bg/company/company-activity/vnedrjavane-na-softuerni-sistemi/",
        "https://dev.bg/company/paid-leave/20-dni/",
        "https://dev.bg/company/paid-leave/21-25-dni/",
        "https://dev.bg/company/paid-leave/25-dni/",
        "https://dev.bg/company/work-hours/chastichno-guvkavo/",
        "https://dev.bg/company/work-hours/fiksirano/",
        "https://dev.bg/company/select/indfintech/",
        "https://dev.bg/company/select/indedutech/",
        "https://dev.bg/company/select/indgaming/",
        "https://dev.bg/company/select/indhrtech/",
        ]

blacklist = [
        "https://dev.bg/company/select/",
        "https://dev.bg/company/headquarters/",
        "https://dev.bg/company/it-employees/",
        "https://dev.bg/company/company-activity/",
        "https://dev.bg/company/paid-leave/",
        "https://dev.bg/company/work-hours/",
        ]

company_regex = re.compile("https:\/\/dev\.bg\/company\/(.+[a-zA-Z0-9])\/", re.IGNORECASE)

# company URLs look like this https://dev.bg/company/dataart/ - i.e. https://dev.bg/company/*/
def is_company_url(url):
    if validators.url(url):
        if re.match(company_regex, url):
            if url not in company_lists:
                if url not in blacklist:
                    return True
    return False

def get_company_urls(company_lists):
    company_urls = []
    for company_list_page in company_lists:
        click.echo(f'Getting list of companies from {company_list_page}')
        r = urllib.request.urlopen(company_list_page)
        s = BeautifulSoup(r, 'lxml', from_encoding=r.info().get_param('charset'))
        for link in s.find_all('a', href=True):
            l = link['href'].split('#', 1)[0]
            if is_company_url(l):
                #click.echo(f"Found company url: {l}")
                company_urls.append(l)
        click.echo(f'Found {len(company_urls)} so far')
    nodups = list(dict.fromkeys(company_urls))
    click.echo(f'Found {len(nodups)} companies')
    #return nodups[:12]
    return nodups

def download_company_description(company_url_list):
    company_info = []
    company_info.append(("Name", "URL", "Established", "Present_In_BG_From"))
    with alive_bar(len(company_url_list)) as bar:
        for url in company_url_list:
            r = urllib.request.urlopen(url)
            s = BeautifulSoup(r, 'lxml', from_encoding=r.info().get_param('charset'))
            name = s.find("h1", class_="company-heading").get_text()
            info = s.find("div", class_="company-info")
            established = info.select('div:-soup-contains("Година на основаване")')[0].select('p:nth-of-type(2)')[0].get_text()
            in_bg = info.select('div:-soup-contains("От кога има офис в България")')[0].select('p:nth-of-type(2)')[0].get_text()
            company_info.append((name, url, established, in_bg))
            bar()
            time.sleep(2)
    return company_info

@click.group()
def cli():
    pass

@cli.command()
def get():
    click.echo('Getting a list of companies')
    companies = get_company_urls(company_lists)
    #print(download_company_description(["https://dev.bg/company/amusnet/"]))
    company_info = download_company_description(companies)
    with open("result.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(company_info)

@cli.command()
def parse():
    click.echo('Parsing company list')

@cli.command()
def clean():
    click.echo(f'Cleaning temp files in {work_dir}')
    shutil.rmtree(work_dir)

if __name__ == '__main__':
    cli()

