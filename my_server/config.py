import logging

class Config:
    DEBUG = True

    @staticmethod
    def schedule_url() -> str:
        return "https://uis.ptithcm.edu.vn/api/sch/w-locdstkbtuanusertheohocky"

    @staticmethod
    def login_url() -> str:
        return "https://uis.ptithcm.edu.vn/api/pn-signin"

    @staticmethod
    def semester_url() -> str:
        return "https://uis.ptithcm.edu.vn/api/sch/w-locdshockytkbuser"

    @staticmethod
    def notification_url() -> str:
        return "https://uis.ptithcm.edu.vn/api/web/w-locdsthongbao"
    
    