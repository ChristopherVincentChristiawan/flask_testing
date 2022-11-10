from database.db import DB
from product.product_edit import ProductEdit

class ProductDal:
    def __init__(self):
        self.db = DB()
    
    def create(self, product):
        _SQL = f"INSERT INTO product_master(code, name, price, catgr_id) values('{product.code}', '{product.name}', '{product.price}', '{product.catgrId}')"
        _lastId = self.db.do_insert(_SQL)
        return _lastId

    def getAll(self):
        _SQL = "SELECT * FROM product_master"
        rows = self.db.do_fetch_all(_SQL)
        products = []
        for row in rows:
            products.append(ProductEdit(row[0], row[1], row[2], row[3], row[4]))

        self.db.close()
        return products

    def getAllByCatgrId(self, catgrId):
        _SQL = "SELECT * FROM product_master"  
        if catgrId != 0:
            _SQL = f"SELECT * FROM product_master WHERE catgr_id={catgrId}"
        
        rows = self.db.do_fetch_all(_SQL)

        products = []
        for row in rows:
            products.append(ProductEdit(row[0], row[1], row[2], row[3], row[4]))

        return products
    
    def getProductById(self, id):
        _SQL = f"SELECT * FROM product_master WHERE id={id}"
        row = self.db.do_fetch_one(_SQL)
        catgr = ProductEdit(row[0], row[1], row[2], row[3], row[4])
        self.db.close()
        return catgr

    def update(self, data):
        _SQL = f"UPDATE product_master SET code='{data.code}',name='{data.name}', price='{data.price}', catgr_id='{data.catgrId}' WHERE id={data.id}"
        self.db.do_update(_SQL)
        self.db.close()

    def delete(self, id):
        _SQL = f"DELETE from product_master WHERE id={id}"
        self.db.do_update(_SQL)
        self.db.close()