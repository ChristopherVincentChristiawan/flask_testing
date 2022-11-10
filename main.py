from flask import Flask, render_template, request, redirect, session
# from werkzeug.wrappers.response import ResponseStreamMixin

from category.catgr_edit import CatgrEdit
from category.catgr_dal import CatgrDal
from product.product_dal import ProductDal
from product.product_edit import ProductEdit

app = Flask(__name__)

app.secret_key = b'auahgelap'

@app.route('/')
@app.route('/home')
def home():
    dal = CatgrDal()
    catgrs = dal.getAll()
    product_dal = ProductDal()
    products = product_dal.getAll()
    return render_template('index.html', catgrs=catgrs, products=products)


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/login-admin', methods = ['POST', 'GET'])
def login_admin():
    user_admin = {"username": "badia", "password": "abcdef"}

    if('user_admin' in session and session['user_admin'] == user_admin['username']):
        return redirect('/admin')
    else:
        if(request.method == 'POST'):
            username = request.form.get('username')
            password = request.form.get('password')     
            if username == user_admin['username'] and password == user_admin['password']:                
                session['user_admin'] = username
                return redirect('/admin')
            return render_template("/login/login-admin.html")
        return render_template("/login/login-admin.html")


@app.route('/logout-admin')
def logout():
    session.pop('user_admin')
    return redirect('/login-admin')


@app.route('/category')
def category():
    # Fetch catgrs from database to be displayed
    dal = CatgrDal()
    catgrs = dal.getAll()
    return render_template('/category/category.html', catgrs=catgrs)


@app.route('/category/', defaults={'id': 0}, methods=['GET', 'POST'])
@app.route('/category/<id>', methods=['GET', 'POST'])
def category_edit(id=0):
    if request.method == 'POST':
        dal = CatgrDal()
        id = int(id)

        # Get FORM data
        _name = request.form['name']

        # a. Check Apakah Data yang di kirim ( request ) ada di database atau tidak
        #    Jika Ada berati lama, Jika tidak ada berarti baru
        # b. Check id of category object is 0 or not
        if id == 0:
            # New Category
            catgr = CatgrEdit(id, _name)

            # Business Process / Logic
            if catgr.validate() == True:
                # Save to DB
                dal.create(catgr)
                #return "Data Kategori berhasil Di simpan!"
                return redirect('/category')
            else:
                # Return Back with error message
                error = "Kategori Tidak Valid"    
        else:
            # Old Category
            catgr = CatgrEdit(id, _name)
            if catgr.validate() == True:
                # Save to DB
                dal.update(catgr)
                #return "Data Kategori berhasil Di simpan!"
                return redirect('/category')
            else:
                # Return Back with error message
                error = "Kategori Tidak Valid"    
    else:
        # GET HTTP REQUEST
        if id == 0:
            catgr = CatgrEdit(0, '')
        else:
            dal = CatgrDal()
            catgr = dal.getCatgrById(id)

        return render_template('/category/catgr_edit.html', catgr=catgr)


@app.route('/product/by/catgr-id', defaults={'catgrId':0})
@app.route('/product/by/catgr-id/<catgrId>')
def product_by_catgr_id(catgrId=0):
    catgrDal = CatgrDal()
    catgrs = catgrDal.getAll()
    
    productDal = ProductDal()
    products = productDal.getAllByCatgrId(catgrId)

    return render_template('index.html', catgrs=catgrs, products=products)


@app.route('/product/selected', defaults={'id':0})
@app.route('/product/selected/<id>')
def select_product(id=0):
    # load from database
    productDal = ProductDal()
    products = productDal.getProductById(id)
    return render_template('/product/product-detail.html', product=products)


@app.route('/add/to/cart/<productId>')
def addToCart(productId=0):
    # Add cart list into session
    dal = ProductDal()
    product = dal.getProductById(productId)
    dict = {'id': product.id, 'name': product.name, 'price': product.price}
    if 'cart_list' in session:
        cart_list = session['cart_list']
        cart_list.append(dict)
    else:
        cart_list = []
        cart_list.append(dict)
    
    session['cart_list'] = cart_list

    # load from database all product based on cart_list

    return render_template('/cart/cart.html', message="Selamat datang di keranjang belanjaan", cart_list=session['cart_list'])


@app.route('/cart')
def cart():
    if 'cart_list' in session:
        return render_template('/cart/cart.html', message="Selamat datang di keranjang belanjaan", cart_list=session['cart_list'])
    else:
        return render_template('/cart/cart.html', message="Keranjang belanja anda kosong")


@app.route('/product')
def product():
    # Fetch catgrs from database to be displayed
    dal = ProductDal()
    products = dal.getAll()
    return render_template('/product/product.html', products=products)


@app.route('/product/', defaults={'id': 0}, methods=['GET', 'POST'])
@app.route('/product/<id>', methods=['GET', 'POST'])
def products_edit(id=0):
    if request.method == 'POST':
        dal = ProductDal()
        id = int(id)

        # Get FORM data
        _code = request.form['code']
        _name = request.form['name']
        _price = request.form['price']
        _catgrId = request.form['catgr_id']
        
        # a. Check Apakah Data yang di kirim ( request ) ada di database atau tidak
        #    Jika Ada berati lama, Jika tidak ada berarti baru
        # b. Check id of category object is 0 or not
        if id == 0:
            # New Category
            product = ProductEdit(id, _code, _name, _price, _catgrId)

            # Business Process / Logic
            if product.validate() == True:
                # Save to DB
                dal.create(product)
                #return "Data Kategori berhasil Di simpan!"
                return redirect('/product')
            else:
                # Return Back with error message
                error = "Produk Tidak Valid"    
        else:
            # Old Category
            product = ProductEdit(id, _code, _name, _price, _catgrId)
            if product.validate() == True:
                # Save to DB
                dal.update(product)
                #return "Data Kategori berhasil Di simpan!"
                return redirect('/product')
            else:
                # Return Back with error message
                error = "Produk Tidak Valid"    
    else:
        # GET HTTP REQUEST
        if id == 0:
            product = ProductEdit(0, '', '', '', '')
        else:
            dal = ProductDal()
            product = dal.getProductById(id)

        return render_template('/product/product_edit.html', product=product)


@app.route('/cart/clear')
def clear_cart():
    session.pop('cart_list')
    return redirect('/cart')


@app.route('/delete/product/<id>')
def delete_product(id=0):
    dal = ProductDal()
    dal.delete(id)
    return redirect('/product')

@app.route('/delete/category/<id>')
def delete_category(id=0):
    dal = CatgrDal()
    dal.delete(id)
    return redirect('/category')

@app.route('/login-client', methods = ['POST', 'GET'])
def login_client():
    user_client = {"username": "stefanus", "password": "stef"}

    if('user_client' in session and session['user_client'] == user_client['username']):
        return redirect('/checkout')
    else:
        if(request.method == 'POST'):
            username = request.form.get('username')
            password = request.form.get('password')     
            if username == user_client['username'] and password == user_client['password']:                
                session['user_client'] = username
                return redirect('/checkout')
            return render_template("/login/login-client.html") 
        return render_template("/login/login-client.html")


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/delete/product/from')
@app.route('/delete/product/from/cart/<productId>')
def delete_product_from_cart(productId=0):
    dal = ProductDal()
    product = dal.getProductById(productId)
    dict = {'id': product.id, 'name': product.name, 'price': product.price}
    if 'cart_list' in session:
        cart_list = session['cart_list']
        cart_list.remove(dict)
    else:
        cart_list = []
        cart_list.remove(dict)
    session['cart_list'] = cart_list

    return render_template('/cart/cart.html', cart_list=session['cart_list'])

@app.route('/logout-client')
def logout_client():
    session.pop('user_client')
    return redirect('/login-client')

@app.route('/profile')
def profile():
    return render_template('/login/login-from-home.html')

@app.route('/finish')
def finish():
    session.pop('cart_list')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)