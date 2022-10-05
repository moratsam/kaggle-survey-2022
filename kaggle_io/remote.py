import json
import requests

from typing import Any, Dict, List

from kaggle_io.constants import BODY, HEADERS, PARAMS, POST_URL, BASE_URL

from kernel import Dataset, Kernel

def download_notebook(notebook_id) -> str:
    """
    Return a raw notebook string.
    """
    url = f'https://www.kaggle.com/kernels/scriptcontent/{notebook_id}/download' 
    return str(requests.get(url).content)


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
        url=BASE_URL+kernel_dict['scriptUrl'],
        language=kernel_dict['languageName'],
        datasets=datasets,
        medal=kernel_dict.get('medal'),
        libs=[], # Keep it empty at this point.
        keywords=[],
        questions=[],
        comments=kernel_dict.get('totalComments', 0),
        views=kernel_dict.get('totalViews', 0),
        votes=kernel_dict.get('totalVotes', 0),
    )
    
    return kernel

def query_kernels_page(year: int, page: int) -> Dict[str, Any]:
    """
    Request a page of kernels.
    """
    # Prepare POST body.
    body = BODY.copy() # Make a copy of the body.
    body['kernelFilterCriteria']['listRequest']['page'] = page # Insert page.
    for k,v in PARAMS[year]['body_params'].items():
        body['kernelFilterCriteria']['listRequest'][k] = v # Insert datasetId/competitionId.

    # Copy POST headers, insert Referer.
    headers = {**HEADERS, 'Referer': PARAMS[year]['url']}

    # Make the request.
    response = requests.post(POST_URL, data=json.dumps(body), headers=headers)

    return response.json()

def query_kernels_year(year: int) -> List[Dict[str, Any]]:
    """
    Get a list of all the kernels for a given year.
    """
    kernels = []
    page = 0
    while True:
        page += 1
        response = query_kernels_page(year, page)
        if 'kernels' in response:
            kernels += response['kernels']
        else:
            break

    return kernels

def query_kernels() -> List[Dict[str, Any]]:
    all_kernels = dict() # Store them in a dict to prevent duplicates.
    for year in range(2017, 2022):
        kernels = query_kernels_year(year)
        for k in kernels:
            all_kernels[k['id']] = k

    print(f"all kernels: {len(all_kernels)}")

    return list(all_kernels.values()) 
