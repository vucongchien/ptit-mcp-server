import logging

class Config:
    BASE_URL = "https://uis.ptithcm.edu.vn"
    API_VERSION = "v1"
    DEBUG = True

    @classmethod
    def schedule_url(cls) -> str:
        return f"{cls.BASE_URL}/api/sch/w-locdsdoituongthoikhoabieu"

    @classmethod
    def login_url(cls) -> str:
        return f"{cls.BASE_URL}/api/pn-signin"

    @classmethod
    def semester_url() -> str:
        return "https://uis.ptithcm.edu.vn/api/sch/w-locdshockytkbuser"
