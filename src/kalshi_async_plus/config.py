from kalshi_python_async import Configuration as BaseConfiguration

class Configuration(BaseConfiguration):
    """
    An extended Configuration class that allows passing api_key_id 
    and private_key_pem directly to the constructor.
    """
    def __init__(self, api_key_id: str = None, private_key_pem: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key_id = api_key_id
        self.private_key_pem = private_key_pem
