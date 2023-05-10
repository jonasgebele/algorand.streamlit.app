import csv
from Market import Market

DEX_CSV_FILE_PATH = "./data/dex_markets.csv"
CEX_CSV_FILE_PATH = "./data/cex_markets.csv"

def read_csv_column(column) -> set:
    set_ = set()
    with open(DEX_CSV_FILE_PATH, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            set_.add(row[column])
    return set_

def get_dex_market_names() -> set:
    market_names = read_csv_column('market_name')
    return market_names

def get_dex_pimary_assets() -> set:
    prim_assets = read_csv_column('asset_0')
    return prim_assets

def get_dex_secondary_assets() -> set:
    sec_assets = read_csv_column('asset_1')
    return sec_assets

def get_dex_addresses() -> set:
    sec_assets = read_csv_column('address')
    return sec_assets

def get_dex_application_ids() -> set:
    sec_assets = read_csv_column('application_id')
    return sec_assets

def get_dex_markets() -> dict:
    dex_markets = dict()
    with open(DEX_CSV_FILE_PATH, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            market_name = row['market_name']
            asset_0 = row['asset_0']
            asset_1= row['asset_1']
            address = row['address']
            application_id = row['application_id']
            key = market_name + '_' + asset_0 + "_"  + asset_1
            dex_markets[key] = Market(market_name, asset_0, asset_1, address, application_id)
    return dex_markets

def get_cex_markets():
    cex_markets = {}
    with open(CEX_CSV_FILE_PATH, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            market_name = row['name']
            asset_0 = row['asset_0']
            asset_1 = row['asset_1']
            key = market_name + '_' + asset_0 + asset_1
            cex_markets[key] = Market(market_name, asset_0, asset_1)
    return cex_markets