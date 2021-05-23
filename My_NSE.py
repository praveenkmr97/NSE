import requests
import json
import pandas as pd
import pdb
import sys
from time import sleep
#from nsetools import Nse

DELTA_1 = 800
DELTA_2 = DELTA_1 + 500
SYMBOL = "NIFTY"
URL = 'https://www.nseindia.com/api/option-chain-indices?symbol=' + SYMBOL
DAJS = {}
headers = {'User-Agent': 'Mozilla/5.0'}


def fetch_oi(expiry_dt):
    ce_values = [data['CE'] for data in DAJS['records']['data'] if "CE" in data and data['expiryDate'] == expiry_dt]
    pe_values = [data['PE'] for data in DAJS['records']['data'] if "PE" in data and data['expiryDate'] == expiry_dt]

    
    ce_dt = pd.DataFrame(ce_values).sort_values(['strikePrice'])
    pe_dt = pd.DataFrame(pe_values).sort_values(['strikePrice'])
    
    #pdb.set_trace()
    
    ce = ce_dt[['strikePrice', 'expiryDate', 'lastPrice', 'underlyingValue']]
    pe = pe_dt[['strikePrice', 'expiryDate', 'lastPrice', 'underlyingValue']]
    underlying_index = ce['underlyingValue'][0]
    
    # print(ce.head())
    #print(pe.head())

    ce_list = ce[['strikePrice']].values.tolist()
    pe_list = pe[['strikePrice']].values.tolist()
    
    ce_del1 = min(ce_list, key=lambda x:abs(x-(underlying_index - DELTA_1)))
    ce_del2 = min(ce_list, key=lambda x:abs(x-(underlying_index - DELTA_2)))

    pe_del1 = min(pe_list, key=lambda x:abs(x-(underlying_index - DELTA_1)))
    pe_del2 = min(pe_list, key=lambda x:abs(x-(underlying_index - DELTA_2)))
    
    ce_del1_pos = ce_list.index(ce_del1)
    ce_del2_pos = ce_list.index(ce_del2)
    
    pe_del1_pos = pe_list.index(pe_del1)
    pe_del2_pos = pe_list.index(pe_del2)
    
    ce_final_delta = ce.iloc[ce_del1_pos][['lastPrice']].item() - ce.iloc[ce_del2_pos][['lastPrice']].item()
    
    pe_final_delta = pe.iloc[pe_del1_pos][['lastPrice']].item() - pe.iloc[pe_del2_pos][['lastPrice']].item()
    
    
    print("Intrested items:")
    #print("CALLS:")
    #print(ce.iloc[ce_del1_pos])
    #print(ce.iloc[ce_del2_pos])
    print("\n\nPUTS:\nDelta 1:")
    print(pe.iloc[pe_del1_pos])
    print("\nDelta 2:")
    print(pe.iloc[pe_del2_pos])
    #print(f"\n\nCalls delta: {ce_final_delta}")
    print(f"\n\nPUTS delta: {pe_final_delta}\n\n")

def main():
    global DAJS
    """
    nse = Nse()
    
    found = False
    while found is False:
        try:
            underlying_index = nse.get_index_quote("nifty 50")
            if underlying_index:
                found = True
        except:
            pass
        sleep(2)
    """
    #expiry_dt = '24-Jun-2021'
    expiry_dt = sys.argv[1]
    
    found = False
    while found is False:
        try:
            page = requests.get(URL, headers=headers)
            if page.status_code == 200:
                found = True
        except:
            pass
        
    DAJS = json.loads(page.text)
    
    fetch_oi(expiry_dt)

if __name__ == '__main__':
    main()