from database.db import DB
from category.catgr_edit import CatgrEdit

class CatgrDal:

    def __init__(self):
        self.db = DB()

    def create(self, catgr):
        _SQL = f"INSERT INTO catgr_list(name) values('{catgr.name}')"
        _lastId = self.db.do_insert(_SQL)
        return _lastId
    
    def getAll(self):
        _SQL = "SELECT * FROM catgr_list"
        rows = self.db.do_fetch_all(_SQL)
        catgrs = []
        for row in rows:
            catgrs.append(CatgrEdit(row[0], row[1]))

        self.db.close()
        return catgrs

    def getCatgrById(self, id):
        _SQL = f"SELECT * FROM catgr_list WHERE id={id}"
        row = self.db.do_fetch_one(_SQL)
        catgr = CatgrEdit(row[0], row[1])
        self.db.close()
        return catgr

    def update(self, data):
        _SQL = f"UPDATE catgr_list SET name='{data.name}' WHERE id={data.id}"
        self.db.do_update(_SQL)
        self.db.close()

    def delete(self, id):
        _SQL = f"DELETE from catgr_list WHERE id={id}"
        self.db.do_update(_SQL)
        self.db.close()