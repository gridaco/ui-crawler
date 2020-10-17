

class MobbinImageModel:
    def __init__(self):
        self.url = ""
        self.image_id = "" # identical with file name
        self.file_url = "" # this may not work due to downloadable time
        self.app: str = ""
        self.app_desc: str = ""
        self.app_url:str = ""
        self.category: str = ""
        self.mobbin_patterns: str = ""
        self.mobbin_elements: str = ""


    def __str__(self):
        return self.app + "::" + self.file_url

    def __repr__(self):
        return self.__str__()
