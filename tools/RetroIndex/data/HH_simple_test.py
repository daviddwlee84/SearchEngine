import os
import sys
from glob import glob

curr_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(curr_dir, '../../Crawler'))

from crawler.manager.combine_results import CombineResult


manager = CombineResult(simplify=True)
for parsed_result in glob(os.path.join(curr_dir, 'result', '*.json')):
    manager.load_from_json(parsed_result)

print(manager.data)

import ipdb
ipdb.set_trace()


from crawler.manager.collect_results import ResultFilter

res_fileter = ResultFilter()
res_fileter.data = manager.data.copy()
HH_result = res_fileter.filter_with_keywords(['华人运通'])
print(HH_result)

import ipdb
ipdb.set_trace()

HH_result.to_csv(os.path.join(curr_dir, 'HH_result.tsv'),
                 sep='\t', header=None)
