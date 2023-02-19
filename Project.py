from audioop import reverse
from genericpath import exists
from queue import Empty
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from pymongo import *
import matplotlib.pyplot as plt
import requests
import re

# When click on add button (Main Screen)
def f1():
	mw.withdraw()
	aw.deiconify()

# When click on update button (Main Screen)
def f3():
	mw.withdraw()
	uw.deiconify()

# When click on delete button (Main Screen)
def f4():
	mw.withdraw()
	dw.deiconify()

# When click on back button (Add Screen)
def f6():
	aw.withdraw()
	mw.deiconify()

# When click on back button (View Screen)
def f7():
	vw.withdraw()
	mw.deiconify()

# When click on back button (Upadte Screen)
def f8():
	uw.withdraw()
	mw.deiconify()

# When click on back button (Delete Screen)
def f9():
	dw.withdraw()
	mw.deiconify()

# Add Information
def save():
	con = None
	try:
		con = MongoClient("mongodb://localhost:27017")
		db = con["ems"]
		coll = db["employee"]
		# Validation in ID
		id = aw_ent_id.get()
		if(len(id) == 0):
			showerror("Error","ID should not be empty")
			return
		elif not id.isdigit():
			showerror("Error","ID should contain only positive numbers, not allowed spaces and special characters")
			return
		elif int(id) < 1:
			showerror("Error","ID should not be 0")
			return
		# Validation in Name
		name = aw_ent_name.get()
		if(len(name) == 0):
			showerror("Error","Name should not be empty")
			return
		elif not name.isalpha():
			showerror("Error","Name should contain only alphabets, not allowed spaces and special characters")
			return
		elif(len(name) < 2):
			showerror("Error","Name should be minimum length of 2")
			return
		# Validation in Salary
		sal = aw_ent_sal.get()
		if(len(sal) == 0):
			showerror("Error","Salary should not be empty")
			return
		elif not sal.isdigit():
			showerror("Error","Salary should contain only positive numbers, not allowed spaces and special characters")
			return
		elif int(sal) < 8000:
			showerror("Error","Salary should be minimum of 8000")
			return

		info = {"_id":id, "name":name, "sal":sal}
		coll.insert_one(info)
		showinfo("Success", "record added")

	except Exception as e:
		showerror("Error", "ID alredy exists")
	finally:
		if con is not None:
			con.close()
			aw_ent_id.delete(0, END)
			aw_ent_name.delete(0, END)
			aw_ent_sal.delete(0, END)
			aw_ent_id.focus()

# View Info
def f2():
	mw.withdraw()
	vw.deiconify()
	vw_st_data.delete(1.0, END)
	con = None
	try:
		con = MongoClient("mongodb://localhost:27017")
		db = con["ems"]
		coll = db["employee"]

		data = coll.find()
		info = ""
		for d in data:
			info += "ID:" + str(d.get("_id")) + " Name:" + str(d.get("name")) + " Salary:" + str(d.get("sal")) + "\n"
		vw_st_data.insert(INSERT, info)

	except Exception as e:
		showerror("Issue ", e)
	finally:
		if con is not None:
			con.close()

# Update Info
def update():
	con = None
	try:
		con = MongoClient("mongodb://localhost:27017")
		db = con["ems"]
		coll = db["employee"]
		# Validation in ID
		id = uw_ent_id.get()
		count = coll.count_documents({"_id":id})

		if count == 0:
			showerror("Error","ID does't exists")
			return
		elif(len(id) == 0):
			showerror("Error","ID should not be empty")
			return
		elif not id.isdigit():
			showerror("Error","ID should contain only positive numbers, not allowed spaces and special characters")
			return
		elif int(id) < 1:
			showerror("Error","ID should not be 0")
			return

		# Validation in Name
		name = uw_ent_name.get()
		if(len(name) == 0):
			showerror("Error","Name should not be empty")
			return
		elif not name.isalpha():
			showerror("Error","Name should contain only alphabets, not allowed spaces and special characters")
			return
		elif(len(name) < 2):
			showerror("Error","Name should be minimum length of 2")
			return

		# Validation in Salary
		sal = uw_ent_sal.get()
		if(len(sal) == 0):
			showerror("Error","Salary should not be empty")
			return
		elif not sal.isdigit():
			showerror("Error","Salary should contain only numbers, not allowed spaces and special characters")
			return
		elif int(sal) < 8000:
			showerror("Error","Salary should be minimum of 8000")
			return

		coll.update_one({"_id":id}, {"$set": {"name":name}})
		coll.update_one({"_id":id}, {"$set": {"sal":sal}})
		showinfo("Success", "record updated")

	except Exception as e:
		showerror("issue", e)
	finally:
		if con is not None:
			con.close()
			uw_ent_id.delete(0, END)
			uw_ent_name.delete(0, END)
			uw_ent_sal.delete(0, END)
			uw_ent_id.focus()

# Delete Info
def delete():
	con = None
	try:

		con = MongoClient("mongodb://localhost:27017")
		db = con["ems"]
		coll = db["employee"]
		# Validation in ID
		id = dw_ent_id.get()
		count = coll.count_documents({"_id":id})

		if count == 0:
			showerror("Error","ID does't exists")
			return
		elif(len(id) == 0):
			showerror("Error","ID should not be empty")
			return
		elif not id.isdigit():
			showerror("Error","ID should contain only positive numbers, not allowed spaces and special characters")
			return
		coll.delete_one({"_id":id})
		showinfo("Success", "record deleted")
	except Exception as e:
		showerror("Error", e)
	finally:
		if con is not None:
			con.close()
			dw_ent_id.delete(0, END)
			dw_ent_id.focus()

# function call from close 
def chart_close(event):
	mw.deiconify()

# chart
def gen():
	mw.withdraw()
	
	sal_graph = []
	name_graph = []

	con = None
	try:
		con = MongoClient("mongodb://localhost:27017")
		db = con["ems"]
		coll = db["employee"]

		data = coll.find().sort("sal", DESCENDING).limit(5)
		for d in data:
			sal_graph.append(int(d.get("sal")))
			name_graph.append(str(d.get("name")))
	
			#salary = int(d.get("sal"))
			#print(salary)

	except Exception as e:
		showerror("issue", e)
	finally:
		if con is not None:
			con.close()	
			
	fig=plt.figure()
	plt.title("Chart")
	plt.xlabel("Top 5 highest Salary Employee Name")
	plt.ylabel("Salary")
	chart = plt.bar(name_graph,sal_graph,color=["green", "orange", "yellow", "pink", "red"],width = 0.4, label="Salary")
	fig.canvas.mpl_connect('close_event', chart_close)
	#plt.grid()
	#plt.legend(shadow=True)
	plt.show()

# Location
def f10():
	try:
		wa = "https://ipinfo.io/"
		response = requests.get(wa)
		data = response.json()
		cityname = data["city"]
		mw_ent_loc.config(text = f"Location : {cityname}")
	except Exception as e:
		print("issue ", e)

# Temp
def f11():
	try:
		a1 = "http://api.openweathermap.org/data/2.5/weather"
		a2 = "?q=" + "Thane"
		a3 = "&appid=" + "43c8c731750d27cd5915be407679e506"
		a4 = "&units=" + "metric"
		wa = a1 + a2+ a3 + a4
		res = requests.get(wa)
		data = res.json()
		temp = data['main']['temp']
		mw_ent_temp.config(text = f"Temp : {temp}")
	except Exception as e:
		print("issue ", e)

# Main Screen
mw = Tk()
mw.title("E.M.S")
mw.geometry("600x500+100+100")
mw['bg']='Light Blue'
y=10
f= ("Arial Rounded MT", 16, "bold")

mw_lab = Label(mw, text="Employee Management System by Rahul", bg='Light Blue', fg='Red', font=f)
mw_btn_add = Button(mw, text="Add", font=f, width=10, bg='Light Blue', fg='Blue', command=f1)
mw_btn_show = Button(mw, text="View", font=f, width=10, bg='Light Blue', fg='Blue', command=f2)
mw_btn_upd = Button(mw, text="Update", font=f, width=10, bg='Light Blue', fg='Blue', command=f3)
mw_btn_dlt = Button(mw, text="Delete", font=f, width=10, bg='Light Blue', fg='Blue', command=f4)
mw_btn_chart = Button(mw, text="Charts", font=f, width=10, bg='Light Blue', fg='Blue', command=gen)
mw_ent_loc = Label(mw, text="", bg='Light Blue', fg='Green', font=f)
f10()
mw_ent_temp = Label(mw, text="", bg='Light Blue', fg='Green', font=f)
f11()

mw_lab.pack(pady=y)
mw_btn_add.pack(pady=y)
mw_btn_show.pack(pady=y)
mw_btn_upd.pack(pady=y)
mw_btn_dlt.pack(pady=y)
mw_btn_chart.pack(pady=y)
mw_ent_loc.place(x = 50, y = 400)
mw_ent_temp.place(x = 400, y = 400)

# Add Screen
aw = Toplevel(mw)
aw.title("Add Emp")
aw.geometry("600x500+100+100")
aw['bg']='Light Green'

aw_lab_id = Label(aw, text="Enter Id:", bg='Light Green', fg='Green', font=f)
aw_ent_id = Entry(aw, bg='Light Green', fg='Black', font=f)

aw_lab_name = Label(aw, text="Enter Name:", bg='Light Green', fg='Green', font=f)
aw_ent_name = Entry(aw, bg='Light Green', fg='Black', font=f)

aw_lab_sal = Label(aw, text="Enter Salary:", bg='Light Green', fg='Green', font=f)
aw_ent_sal = Entry(aw, bg='Light Green', fg='Black', font=f)

aw_btn_save = Button(aw, text="Save", font=f, bg='Light Green', fg='Green', command=save)
aw_btn_back = Button(aw, text="Back", font=f, bg='Light Green', fg='Green', command=f6)

aw_lab_id.pack(pady=y)
aw_ent_id.pack(pady=y)
aw_lab_name.pack(pady=y)
aw_ent_name.pack(pady=y)
aw_lab_sal.pack(pady=y)
aw_ent_sal.pack(pady=y)
aw_btn_save.pack(pady=y)
aw_btn_back.pack(pady=y)
aw.withdraw()

# View Screen
vw = Toplevel(mw)
vw.title("View Emp")
vw.geometry("600x500+100+100")
vw['bg']='Yellow'

vw_st_data = ScrolledText(vw, width=35, height=10, font=f)
vw_btn_back = Button(vw, text="Back", font=f, command=f7)
vw_st_data.pack(pady=y)
vw_btn_back.pack(pady=y)
vw.withdraw()

# Update Screen
uw = Toplevel(mw)
uw.title("Update Emp")
uw.geometry("600x500+100+100")
uw['bg']='Pink'

uw_lab_id = Label(uw, text="Enter Id:", bg='Pink', font=f)
uw_ent_id = Entry(uw, bg='Pink', font=f)

uw_lab_name = Label(uw, text="Enter Name:", bg='Pink', font=f)
uw_ent_name = Entry(uw, bg='Pink', font=f)

uw_lab_sal = Label(uw, text="Enter Salary:", bg='Pink', font=f)
uw_ent_sal = Entry(uw, bg='Pink', font=f)

uw_btn_save = Button(uw, text="Save", bg='Pink', font=f, command=update)
uw_btn_back = Button(uw, text="Back", bg='Pink', font=f, command=f8)

uw_lab_id.pack(pady=y)
uw_ent_id.pack(pady=y)
uw_lab_name.pack(pady=y)
uw_ent_name.pack(pady=y)
uw_lab_sal.pack(pady=y)
uw_ent_sal.pack(pady=y)
uw_btn_save.pack(pady=y)
uw_btn_back.pack(pady=y)
uw.withdraw()

# Delete Screen
dw = Toplevel(mw)
dw.title("Delete Emp")
dw.geometry("600x500+100+100")
dw['bg']='Red'

dw_lab_id = Label(dw, text="Enter Id:", bg='Red', font=f)
dw_ent_id = Entry(dw, bg='Red', font=f)

dw_btn_save = Button(dw, text="Save", font=f, bg='Red', command=delete)
dw_btn_back = Button(dw, text="Back", font=f, bg='Red', command=f9)

dw_lab_id.pack(pady=y)
dw_ent_id.pack(pady=y)
dw_btn_save.pack(pady=y)
dw_btn_back.pack(pady=y)
dw.withdraw()

mw.mainloop()