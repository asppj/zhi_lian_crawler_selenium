from datetime import datetime

from bs4 import BeautifulSoup
from db_client import mongo_client
from logger import logger_root


class JobItem():
    def __init__(self, elem, browser):
        self.elem = elem
        self.browser = browser
        self.format_item()

    def format_item(self):
        items = self.elem.find_all("a")
        tmp = []
        for item in items:
            url = item.get("href")
            name = item.get_text()
            tmp.append((name, url))
        job = Job(*tmp[0], self.browser)
        tmp_company = [item.get_text() for item in
                       self.elem.find_all("span",
                                          class_="contentpile__content__wrapper__item__info__box__job__comdec__item")]

        company = Company(*tmp[1], *tmp_company, self.browser)
        relation = Relation(job, company)
        relation.save()
        return tmp


class Job():
    dict_item = None

    def __init__(self, name, url, browser):
        '''工作，城市，工资，要求，待遇'''
        pass
        self.name = name
        self.url = url
        self.driver = browser
        try:
            self.wage, self.claim, self.welfare, self.qualifications, self.address = self._get_detail()
        except Exception as e:
            logger_root.exception(e)
            self.driver.close()
            raise e

        self.driver.close()
        self.make_item()

    def _get_detail(self):
        '''
        wage:工资
        claim：要求
        qualifications：岗位职责
        welfare：福利，
        address：工作地点
        :return:
        '''
        self.driver.get(self.url)
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        print()
        wage = soup.find("div", class_="l info-money").get_text().strip()
        claim = [elem.get_text() for elem in soup.find("div", class_="info-three l").find_all("span")]
        welfare = [elem.get_text() for elem in soup.find("div", class_="pos-info-tit").find_all("span")]
        qualifications = ["".join(elem.get_text()) for elem in soup.find("div", class_="pos-ul").find_all("p")]
        address = soup.find("p", class_="add-txt").get_text()
        return wage, claim, welfare, qualifications, address

    def make_item(self):
        self.dict_item = {
            "name": self.name,
            "url": self.url,
            "wage": self.wage,
            "claim": self.claim,
            "welfare": self.welfare,
            "qualifications": self.qualifications,
            "address": self.address
        }
        return self.dict_item

    def save(self):
        return mongo_client.insert_job(self.dict_item)
        pass


class Company():
    dict_item = None

    def __init__(self, name, url, types, count, browser):
        self.name = name
        self.url = url
        self.type = types
        self.count = count
        self.driver = browser
        try:
            self.address, self.detail = self._get_detail()
        except Exception as e:
            logger_root.exception(e)
            self.driver.close()
            raise e
        self.driver.close()
        self.make_item()

    def _get_detail(self):
        self.driver.get(self.url)
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        address_soup = soup.find("p", class_="map-box__adress")
        address = address_soup.string if address_soup else "空地址"
        detail_soup = soup.find_all("span", class_="main__number__content")
        detail = [elem.string for elem in detail_soup] if detail_soup else []
        return address, detail

    def make_item(self):
        self.dict_item = {
            "name": self.name,
            "address": self.address,
            "url": self.url,
            "scale": self.count,
            "type": self.type,
            "detail": self.detail[2] if len(self.detail) == 3 else "空"
        }
        return self.dict_item

    def save(self):
        return mongo_client.insert_company(self.dict_item)


class Relation():
    def __init__(self, job, company):
        self.job = job
        self.company = company
        pass

    def insert_relation(self, job, company):
        pass
        rsp = mongo_client.find_relation_by_urls(job["url"], company["url"])
        if not rsp:
            relation = {
                "relation_name": "招聘",
                "timestamp": datetime.utcnow(),
                "company_name": company["name"],
                "company_id": company["_id"],
                "company_url": company["url"],
                "job_name": job["name"],
                "job_id": job["_id"],
                "job_url": job["url"],
                "wage": job["wage"],
                "city": job["claim"][0]
            }
            mongo_client.insert_relation(relation)
            return relation

        return None

    def save(self):
        job = mongo_client.find_job_by_url(self.job.url)
        if not job:
            job = self.job.dict_item
            job["_id"] = self.job.save().inserted_id
            pass
        company = mongo_client.find_company_by_url(self.company.url)

        if not company:
            company = self.company.dict_item
            company["_id"] = self.company.save().inserted_id
        relation = self.insert_relation(job, company)
        if relation:
            print("relation save:{}".format(relation))
        else:
            print("旧信息")
        pass
