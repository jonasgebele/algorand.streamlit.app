class Market():
    def __init__(self, market_name:str, asset_0:int, asset_1:int, address:str = None, application_id:int = None):
        self.market_name = market_name
        self.asset_0 = asset_0
        self.asset_1 = asset_1
        self.address = address
        self.application_id = application_id

    def get_market_name(self):
        return self.market_name

    def get_asset_0(self):
        return self.asset_0

    def set_asset_0(self, new_asset_0):
        self.asset_0 = new_asset_0

    def get_asset_1(self):
        return self.asset_1

    def set_asset_1(self, new_asset_1):
        self.asset_1 = new_asset_1

    def get_address(self):
        return self.address

    def get_application_id(self):
        return self.application_id
    
    def to_string(self):
        return f"Market Name: {self.market_name}\nAsset 0: {self.asset_0}\nAsset 1: {self.asset_1}\nAddress: {self.address}\nApplication ID: {self.application_id}"