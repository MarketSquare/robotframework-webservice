class Config:
    """
    Service Config as Singleton
    """
    _instance = None

    _cmd_args = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Config, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    @property
    def cmd_args(self) -> str:
        return self._cmd_args

    @cmd_args.setter
    def cmd_args(self, value: str):
        self._cmd_args = value