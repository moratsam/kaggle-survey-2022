import json
import requests
from time import sleep
from typing import Any, Dict, List, Tuple
from datetime import datetime

from kaggle_io.constants import HEADERS, BASE_URL
from kernel import Dataset, Kernel

import brotli
from webdriver_manager.firefox import GeckoDriverManager
from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service

def download_notebook(session, notebook_id: int, language) -> Tuple[str, str]:
   """
   Return a raw notebook string.
   """
   url = f'https://www.kaggle.com/kernels/scriptcontent/{notebook_id}/download' 
   resp = session.get(url, headers=HEADERS)
   if resp.status_code != 200:
      raise ValueError(f'{notebook_id} {resp.reason} {resp.text}')

   notebook = resp.content.decode('utf-8')
   # Helps deal with codecs.
   if language == 'Python':
      try:
         notebook = json.dumps(json.loads(notebook))
      except json.JSONDecodeError:
         print(f"ERROR: Unrecognised format for notebook id: {notebook_id}")
         language = "UNKNOWN"

   return notebook, language


def objectivise_kernel(kernel_dict: Dict[str, Any]) -> Kernel:
   """
   Transform a kernel dict returned by kernel queries into a Kernel object.
   """

   # Create datasets.
   datasets = []
   for d in kernel_dict['dataSources']:
      dataset = Dataset(
         id=d['reference']['sourceId'],
         name=d['name'],
         url=BASE_URL+d.get('dataSourceUrl', "PRIVATE"),
      )
      datasets.append(dataset)

   kernel = Kernel(
      id=kernel_dict['id'],
      notebook_id=kernel_dict['scriptVersionId'],
      title=kernel_dict['title'],
      created_at=datetime.strptime('1970', '%Y'), # Will be taken from kaggle-meta.
      evaluation_date=datetime.strptime('1970', '%Y'), # Will be taken from kaggle-meta.
      year=1970, # Will be taken from kaggle-meta.
      made_public_date=datetime.strptime('1970', '%Y'), # Will be taken from kaggle-meta.
      url=BASE_URL+kernel_dict['scriptUrl'],
      language=kernel_dict['languageName'],
      datasets=datasets,
      medal=kernel_dict.get('medal'),
      libs=[], # Will be populated by the notebook_parser.
      keywords=[],
      tags=[],
      tier=kernel_dict['author'].get('performanceTier'),
      questions=[], # Will be populated by the notebook_parser.
      comments=kernel_dict.get('totalComments', 0),
      views=kernel_dict.get('totalViews', 0),
      votes=kernel_dict.get('totalVotes', 0),
   )
   
   return kernel

def query_kernels_year(year: int) -> List[Dict[str, Any]]:
   """
   Get a list of all the kernels for a given year.
   """
   driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
   driver.scopes = ['https://www.kaggle.com/api/i/kernels.KernelsService/ListKernels']

   if year in (2017, 2018):
      url = f'https://www.kaggle.com/datasets/kaggle/kaggle-survey-{year}/code'
   else:
      url = f'https://www.kaggle.com/competitions/kaggle-survey-{year}/code'

   driver.get(url)
   sleep(10)

   kernels_cnt = 0
   while True:
      elems = driver.find_elements_by_class_name('sc-jfmDQi')
      if kernels_cnt == len(elems):
         break
      kernels_cnt = len(elems)
      driver.execute_script("arguments[0].scrollIntoView();", elems[-1])
      sleep(6)

   kernels = {}
   for req in driver.requests:
      if 'api/i/kernels.KernelsService/ListKernels' not in req.url:
         continue
      for k in json.loads(str(brotli.decompress(req.response.body), 'utf-8'))['kernels']:
         kernels.append(k)

   driver.close()
   return kernels

def query_kernels() -> List[Dict[str, Any]]:
   all_kernels = dict() # Store them in a dict to prevent duplicates.
   for year in range(2017, 2022):
      kernels = query_kernels_year(year)
      for k in kernels:
         all_kernels[k['id']] = k

   print(f"all kernels: {len(all_kernels)}")

   return list(all_kernels.values()) 
