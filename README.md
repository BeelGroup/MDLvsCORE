## MDL Open Recommender API - Analysis

### Requirements

Requires Python 2.7

Required packages can be installed using pip:
pip install -r requirements.txt

### Running

Analyser.py {Path to RARD Dataset}

### Dataset

The RARDII dataset is available at https://dataverse.harvard.edu/dataverse/Mr_DLib

### Metrics

|                                     |         |         |         |         |         |         |         |         |         |        |         | 
|-------------------------------------|---------|---------|---------|---------|---------|---------|---------|---------|---------|--------|---------| 
|  | May-17                              | Jun-17  | Jul-17  | Aug-17  | Sep-17  | Oct-17  | Nov-17  | Dec-17  | Jan-18  | Feb-18  | Mar-18 |         | 
| Jabref CTR                          | 0.823%  | 0.760%  | 0.415%  | 0.603%  | 0.340%  | 0.240%  | 0.163%  | 0.179%  | 0.159%  | 0.201% | 0.171%  | 
| Jabref CORE CTR                     | 0.000%  | 0.694%  | 0.401%  | 0.534%  | 0.294%  | 0.278%  | 0.192%  | 0.221%  | 0.208%  | 0.165% | 0.177%  | 
| Mr. DLib Jabref CTR                 | 0.826%  | 0.760%  | 0.419%  | 0.631%  | 0.360%  | 0.222%  | 0.152%  | 0.163%  | 0.139%  | 0.214% | 0.168%  | 
| Mr. DLib Jabref CBF Terms CTR       | 0.832%  | 0.762%  | 0.424%  | 0.639%  | 0.353%  | 0.220%  | 0.150%  | 0.162%  | 0.139%  | 0.214% | 0.168%  | 
| Mr. DLib Sowiport CTR               | 0.119%  | 0.107%  | 0.100%  | 0.097%  | 0.128%  | 0.147%  | 0.139%  | 0.110%  | 0.065%  | 0.024% | 0.013%  | 
| Jabref Delivered                    | 16888   | 22381   | 21668   | 27508   | 24672   | 130581  | 141880  | 125137  | 172798  | 143896 | 159996  | 
| Jabref Clicked                      | 139     | 170     | 90      | 166     | 84      | 313     | 231     | 224     | 275     | 289    | 273     | 
| Jabref CORE Delivered               | 54      | 144     | 4487    | 7869    | 7154    | 40240   | 38466   | 33988   | 49456   | 38763  | 40637   | 
| Jabref CORE Clicked                 | 0       | 1       | 18      | 42      | 21      | 112     | 74      | 75      | 103     | 64     | 72      | 
| Mr. DLib Jabref Delivered           | 16834   | 22237   | 17181   | 19639   | 17518   | 90341   | 103414  | 91149   | 123342  | 105133 | 119359  | 
| Mr. DLib Jabref Clicked             | 139     | 169     | 72      | 124     | 63      | 201     | 157     | 149     | 172     | 225    | 201     | 
| Mr. DLib Jabref CBF Terms Delivered | 16580   | 22049   | 16998   | 19411   | 17299   | 87747   | 100810  | 88710   | 120558  | 102587 | 116344  | 
| Mr. DLib Jabref CBF Terms Clicked   | 138     | 168     | 72      | 124     | 61      | 193     | 151     | 144     | 168     | 220    | 195     | 
| Mr. DLib Sowiport Delivered         | 2873914 | 2581456 | 2436499 | 2396723 | 1867298 | 2236312 | 2676688 | 2375750 | 3423862 | 941498 | 1686766 | 
| Mr. DLib Sowiport Clicked           | 3431    | 2775    | 2432    | 2314    | 2396    | 3286    | 3718    | 2607    | 2219    | 223    | 211     | 
