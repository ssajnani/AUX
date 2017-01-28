from flask import Blueprint, render_template, request
import mysql.connector
customer_api = Blueprint('customer_api', __name__, template_folder="templates")

@customer_api.route('/customeroptions')
def showingOpts():
	return render_template('customerMainPage.html')

@customer_api.route('/addcustomer')
def newCustomer(customer=None):
	return render_template('formcustomeradd.html', customer=customer)

@customer_api.route('/customeradded', methods = ["POST"])
def submitCustomer():

	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insert_stmt = (
		"INSERT INTO Customer (idCustomer, FirstName, LastName, EmailAddress, Sex)  "
		"VALUES (%s, %s, %s, %s, %s)"
		)
	
	data = (request.form['cid'], request.form['fn'],request.form['ln'],request.form['email'],request.form['sex'])
	data2 = (request.form['cid'],)

	sel_stmt = (
		"SELECT * from Customer "
		"where idCustomer= %s"
		)

	cursor.execute(sel_stmt, data2)

	if cursor.fetchone():
		return render_template('customerAlreadyExists.html')
	
	if (request.form['cid'] == "" or request.form['cid'] == None):
		return render_template('addCid.html')

	if (request.form['fn'] == "" or request.form['fn'] == None):
		return render_template('addFirstName.html')

	if (request.form['ln'] == "" or request.form['ln'] == None):
		return render_template('addLastName.html')

	if (request.form['email'] == "" or request.form['email'] == None):
		return render_template('addEmail.html')

#	if (request.form['sex'] == "" or request.form['sex'] == None):
#		return render_template('addSex.html')
	
	cursor.execute(insert_stmt, data)
	
#"""
	cnx.commit()
	cnx.close()
	return render_template('addedCustomer.html', cid=request.form['cid'])
		
@customer_api.route('/deletecustomer')
def oldCustomer(customer=None):
        return render_template('formcustomerdelete.html', customer=customer)

@customer_api.route('/customerdelete', methods = ["POST"])
def deleteCustomer():
	cnx = mysql.connector.connect(user='root', database = 'MovieTheatre', buffered=True)
	cursor = cnx.cursor()
	del_stmt = (
		"DELETE FROM Customer "
		"where idCustomer = %s"
		)
	data = (request.form['cid'],)
	
	if (request.form['cid'] == "" or request.form['cid'] == None):
		cnx.close()
		return render_template('addCid.html')
	
	sel_stmt = (
		"SELECT * from Customer "
		"where idCustomer = %s"
		)

	cursor.execute(sel_stmt, data)
	
	if not cursor.fetchone():
		cnx.close()
		return render_template('noSuchCustomer.html')
	
	sel_stmt2 = (
		"SELECT Customer.idCustomer from Customer right join Attend "
		"on Attend.Customer_idCustomer=Customer.idCustomer "
		"where Customer.idCustomer = %s"
		)

	cursor.execute(sel_stmt2, data)
	if cursor.fetchone():
		cnx.close()
		return render_template('customerBookedShow.html')

	cursor.execute(del_stmt, data)
	cnx.commit()
	cnx.close()
	return render_template('successfulCustomerDelete.html', cid = request.form['cid'])

@customer_api.route('/modifycustomer')
def changeCustomer(customer=None):
        return render_template('formcustomerchange.html',customer=customer)

@customer_api.route('/customermodified', methods = ["POST"])
def modifyShowing():

	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	modify_stmt = (
			"UPDATE Customer set FirstName=%s, LastName =%s, EmailAddress =%s, Sex = %s "
			"WHERE idCustomer = %s"
			)
	data = (request.form['fn'], request.form['ln'], request.form['email'], request.form['sex'], request.form['cid'])

	sel_stmt = (
			"SELECT * from Customer where EmailAddress = %s" )
	data2 = (request.form['email'],)
	cursor.execute(sel_stmt, data2)
	
	if cursor.fetchone():
		return render_template('needUniqueEmail.html')

	if (request.form['fn'] == None or request.form['fn'] == ""):
		return render_template('addFirstName.html')
	if (request.form['ln'] == None or request.form['ln'] == ""):
		return render_template('addLastName.html')
	if (request.form['email'] == None or request.form['email'] == ""):
		return render_template('addEmail.html')
#	if (request.form['sex'] == None or request.form['sex'] == ""):
#		return render_template('addSex.html')
	if (request.form['cid'] == None or request.form['cid'] == ""):
		return render_template('addCid.html')
	cursor.execute(modify_stmt, data)
	cnx.commit()	
	cnx.close()
	return render_template('successfulCustomerModified.html', cid=request.form['cid'])


@customer_api.route('/listcustomers')
def listAllCustomers():
	cnx = mysql.connector.connect(user='root', database = 'MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from Customer order by LastName")
	cursor.execute(query)
	customers=cursor.fetchall()
	cnx.close()
	return render_template('listofcustomers.html', customers=customers)

