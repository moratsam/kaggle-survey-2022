# Used to make the POST request to query for kernels.
POST_URL = "https://www.kaggle.com/api/i/kernels.KernelsService/ListKernels"
# Used to construct a valid full url.
BASE_URL = 'https://kaggle.com'


# Parameters used in kernel queries.
PARAMS = {
    2017: {
        'body_params': {'datasetId': 2733},
        'url': 'https://www.kaggle.com/datasets/kaggle/kaggle-survey-2017/code',
    },
    2018: {
        'body_params': {'datasetId': 70947},
        'url': 'https://www.kaggle.com/datasets/kaggle/kaggle-survey-2018/code',
    },
    2019: {
        'body_params': {'competetionId': 16394},
        'url': 'https://www.kaggle.com/competitions/kaggle-survey-2019/code',
    },
    2020: {
        'body_params': {'competetionId': 23724},
        'url': 'https://www.kaggle.com/competitions/kaggle-survey-2020/code',
    },
    2021: {
        'body_params': {'competetionId': 31480},
        'url': 'https://www.kaggle.com/competitions/kaggle-survey-2021/code',
    },
}

# Base body used in kernel query POST request.
BODY = {'kernelFilterCriteria': {'search': '',
  'listRequest': {'sortBy': 'HOTNESS',
   'pageSize': 100,
   'group': 'EVERYONE',
   # 'page': 1,
   # 'datasetId': 2733,
   'tagIds': '',
   'excludeResultsFilesOutputs': False,
   'wantOutputFiles': False}},
 'detailFilterCriteria': {'deletedAccessBehavior': 'RETURN_NOTHING',
  'unauthorizedAccessBehavior': 'RETURN_NOTHING',
  'excludeResultsFilesOutputs': False,
  'wantOutputFiles': False,
  'kernelIds': [],
  'outputFileTypes': [],
  'includeInvalidDataSources': False}}

# Base headers used in kernel query POST request.
HEADERS = {
    'Host': 'www.kaggle.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    #'Accept-Encoding': 'gzip, deflate, br', # fuck gzip
    # 'Referer': 'https://www.kaggle.com/datasets/kaggle/kaggle-survey-2017/code',
    'Content-Length': '455',
    'Origin': 'https://www.kaggle.com',
    'Connection': 'keep-alive',
    'Cookie': 'ka_sessionid=40ef412068d39349c7411cfd27fc072e; CSRF-TOKEN=CfDJ8PSMPbR3HMFPmfBlccWrC-DFyCmrVSbJJIFRoU5aj23Pdj1s3U3kUu-NtgTAO6SC1Cb9V9W3is96Ts6kdIgnhi_d0dFM15FHc0WTeW4Cag; XSRF-TOKEN=CfDJ8PSMPbR3HMFPmfBlccWrC-BettW6cUn2vR7Ql2lR2Pm1oO4N423dHcoCXUqJ5v_8pWsvM3He0dxPG3UM-3ZyF-bGSaMBlm_f8n5lzy0bTA5AeA; CLIENT-TOKEN=eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpc3MiOiJrYWdnbGUiLCJhdWQiOiJjbGllbnQiLCJzdWIiOm51bGwsIm5idCI6IjIwMjItMTAtMDNUMjA6MjM6NTcuNjM1MTU3MVoiLCJpYXQiOiIyMDIyLTEwLTAzVDIwOjIzOjU3LjYzNTE1NzFaIiwianRpIjoiMDhmM2RhMDAtOGE1MC00NGVlLWI0MGItOGYyMzEzMDY3MDVmIiwiZXhwIjoiMjAyMi0xMS0wM1QyMDoyMzo1Ny42MzUxNTcxWiIsImFub24iOnRydWUsImZmIjpbIktlcm5lbHNSZXN1bWUiLCJLZXJuZWxzRmlyZWJhc2VMb25nUG9sbGluZyIsIktlcm5lbHNTdGFja092ZXJmbG93U2VhcmNoIiwiQ29tbXVuaXR5S21JbWFnZVVwbG9hZGVyIiwiVFBVQ29tbWl0U2NoZWR1bGluZyIsIkFsbG93Rm9ydW1BdHRhY2htZW50cyIsIktlcm5lbEVkaXRvckdvb2dsZVNpZ25JbkF1dGgiLCJLTUxlYXJuRGV0YWlsIiwiRnJvbnRlbmRDb25zb2xlRXJyb3JSZXBvcnRpbmciLCJQaG9uZVZlcmlmeUZvckNvbW1lbnRzIiwiUGhvbmVWZXJpZnlGb3JOZXdUb3BpYyIsIkxpaHBOZXh0U3RlcHMiLCJMaWhwTmV4dFN0ZXBzTWV0cmljcyIsIkttQ29tcHNEYXRhUGFnZSIsIkNvbXBldGl0aW9uc0Nsb25lIiwiTGVhcm5HdWlkZXMiLCJLZXJuZWxFZGl0b3JIYW5kbGVNb3VudE9uY2UiXSwiZmZkIjp7Iktlcm5lbEVkaXRvckF1dG9zYXZlVGhyb3R0bGVNcyI6IjMwMDAwIiwiRnJvbnRlbmRFcnJvclJlcG9ydGluZ1NhbXBsZVJhdGUiOiIwLjAxIiwiRW1lcmdlbmN5QWxlcnRCYW5uZXIiOiJ7IH0iLCJDbGllbnRScGNSYXRlTGltaXQiOiI0MCIsIkZlYXR1cmVkQ29tbXVuaXR5Q29tcGV0aXRpb25zIjoiMzUzMjUsMzcxNzQsMzM1NzksMzc4OTgsMzczNTQsMzc5NTkiLCJBZGRGZWF0dXJlRmxhZ3NUb1BhZ2VMb2FkVGFnIjoiZGF0YXNldHNNYXRlcmlhbERldGFpbCJ9LCJwaWQiOiJrYWdnbGUtMTYxNjA3Iiwic3ZjIjoid2ViLWZlIiwic2RhayI6IkFJemFTeUE0ZU5xVWRSUnNrSnNDWldWei1xTDY1NVhhNUpFTXJlRSIsImJsZCI6ImIwMjM2OGU4ZjczZjE1MTMxNWE3YzQ1ZjMyN2ZjYWY4NmVkODVmYjEifQ.; GCLB=CNel8t6unar4xQE; _ga=GA1.2.1171203665.1664828638; _gid=GA1.2.2017036065.1664828638',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
    'content-type': 'application/json',
    'x-xsrf-token': 'CfDJ8PSMPbR3HMFPmfBlccWrC-BettW6cUn2vR7Ql2lR2Pm1oO4N423dHcoCXUqJ5v_8pWsvM3He0dxPG3UM-3ZyF-bGSaMBlm_f8n5lzy0bTA5AeA',
    'Alt-Used': 'www.kaggle.com',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
 }
