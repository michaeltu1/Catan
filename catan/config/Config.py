class Config:

    def __init__(self):
        self.config = {"standard": {"dice": "fair",
                                    "board": "random"},
                       }

    def get_config(self, mode="standard"):
        return self.config[mode]
