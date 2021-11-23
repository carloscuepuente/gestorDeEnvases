from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import messagebox
from tkinter import filedialog

import database as db

#conect_to = "pruebaconfecha.db"
conect_to = "TecnoquimEnvasesDatabase.db"


#funciones de los botones
def show_cliente_click():
    
    if rif_search_entry.get() == "":
        messagebox.showerror("Error", "El campo del Rif no puede estar vacío")
        return
    else:
        rif = rif_search_entry.get()
        populate_list(rif=rif)

#hay que acomodar esta funcion para que de algun indicio
#si algo va mal, como por ejemplo si el cliente no se encuentra
def populate_list(rif = ""):
    for i in cliente_tree_view.get_children():
        cliente_tree_view.delete(i)
    cliente_tree_view.insert(parent="",
                            index="end",
                            values = db.Database(conect_to).show_client(rif=rif),
                            )

def empty_entry_fields_check_all():
    #chequea que los campos no esten vacios
    if (rif_search_entry.get() == "") or (cliente_search_entry.get() == "") or (galones_entry.get() == "")  or (cunete_entry.get() == "" ) or (carbolla_entry.get() == "") or (tambor_entry.get() == ""):
        return True
    else:
        return False

def empty_entry_fields_check_all_but_name():
    #chequea que los todos los camposn menos el del nombre no esten vacios
    if (rif_search_entry.get() == "") or (galones_entry.get() == "")  or (cunete_entry.get() == "" ) or (carbolla_entry.get() == "") or (tambor_entry.get() == ""):
        return True
    else:
        return False


def sum_container_click():
    if not empty_entry_fields_check_all():
        cliente = [(rif_search_entry.get(),
                    cliente_search_entry.get(),
                    galones_entry.get(),
                    cunete_entry.get(),
                    carbolla_entry.get(),
                    tambor_entry.get())]
        db.Database(conect_to).sum_envases(clientes=cliente)
        populate_list(rif=rif_search_entry.get())
        #para que si hay un doble clic erroneo no sume
        galones_text.set("0")
        cunete_text.set("0")
        carbolla_text.set("0")
        tambor_text.set("0")

    else:
        messagebox.showerror("Error", "Por favor llene los todos los campos")


def subtract_container_click():
    if not empty_entry_fields_check_all():
        cliente = [(rif_search_entry.get(),
                    cliente_search_entry.get(),
                    abs(int(galones_entry.get())),
                    abs(int(cunete_entry.get())),
                    abs(int(carbolla_entry.get())),
                    abs(int(tambor_entry.get())))]
        if db.Database(conect_to).substract_envases(clientes=cliente) == "ErrorOperacional":
            messagebox.showerror("Error", "No pueden haber envases negativos")
        populate_list(rif=rif_search_entry.get())
        #para que si hay doble clic erroneo, no reste
        galones_text.set("0")
        cunete_text.set("0")
        carbolla_text.set("0")
        tambor_text.set("0")

    else:
        messagebox.showerror("Error", "Por favor llene los todos los campos")


def show_cliente_byname_click():
    if cliente_search_entry.get() == "":
        messagebox.showerror("Error", "El campo nombre de cliente no puede estar vacio")
    else:
        name_cliente_find = cliente_search_entry.get()
        db_ansewer = db.Database(conect_to).show_cliente_by_name(name=name_cliente_find)
        for i in cliente_tree_view.get_children():
            cliente_tree_view.delete(i)
        for row in db_ansewer:
            cliente_tree_view.insert(parent="",
                                index="end",
                                values = row)


def create_cliente_click():
    if (rif_search_entry.get() == "") or (cliente_search_entry.get() == "") or (galones_entry.get() == "")  or (cunete_entry.get() == "" ) or (carbolla_entry.get() == "") or (tambor_entry.get() == ""):
        messagebox.showerror("Error", "No se puede crear cliente con campos vacios")
    else:
        cliente = [(rif_search_entry.get(),
                    cliente_search_entry.get(),
                    galones_entry.get(),
                    cunete_entry.get(),
                    carbolla_entry.get(),
                    tambor_entry.get())]
        if db.Database(conect_to).crear_cliente(cliente=cliente) == "ErrorOperacional":
            messagebox.showerror("Error", "No se puede crear cliente con envases negativos")
        else: 
            rif = rif_search_entry.get()
            populate_list(rif=rif)

def update_cliente():
    if not empty_entry_fields_check_all():
        cliente = [(rif_search_entry.get(),
                    cliente_search_entry.get(),
                    galones_entry.get(),
                    cunete_entry.get(),
                    carbolla_entry.get(),
                    tambor_entry.get())]
        db.Database(conect_to).update_cliente(clientes=cliente)
        rif = rif_search_entry.get()
        populate_list(rif=rif)
    else:
        pass


def delete_cliente():
    if not empty_entry_fields_check_all():
        #deleted = [rif_search_entry.get(),cliente_search_entry.get()]
        db.Database(conect_to).remove_cliente(rif=rif_search_entry.get())
        show_database()
        
        #rif = rif_search_entry.get()
        #populate_list(rif=rif)
        



def submit_click():
    if clicked_option.get() == 1 and not empty_entry_fields_check_all():
        #messagebox.showinfo("op1","clicaste sobrescribir")
        if messagebox.askokcancel("Actualizar Cliente","¿Seguro que quiere actualizar el cliente?"):
            update_cliente()
            messagebox.showinfo("Actualizacion","Cliente Actualizado")
            
            clicked_option.set(None)
        else:
            clicked_option.set(None) #para reestablecer el radiobuton
            return
    
    elif clicked_option.get() == 2 and not empty_entry_fields_check_all():
        deleted = [rif_search_entry.get(),cliente_search_entry.get()]
        if messagebox.askokcancel("Borrar Cliente","¿Seguro que quiere borrar el cliente?"):
            delete_cliente()
            messagebox.showinfo("Cliente Borrado", "Cliente {}, {} borrado".format(deleted[0],deleted[1]))
            clicked_option.set(None)
        else:
            clicked_option.set(None)
            return
    else:
        clicked_option.set(None)
        return


def select_cliente(event):
    try:
        global selected_item
        index = cliente_tree_view.selection()[0]
        selected_item = cliente_tree_view.item(index)["values"]
        rif_search_entry.delete(0,END)
        rif_search_entry.insert(END,selected_item[0])
        cliente_search_entry.delete(0,END)
        cliente_search_entry.insert(END,selected_item[1])
        galones_entry.delete(0,END)
        galones_entry.insert(END,selected_item[2])
        cunete_entry.delete(0,END)
        cunete_entry.insert(END, selected_item[3])
        carbolla_entry.delete(0,END)
        carbolla_entry.insert(END,selected_item[4])
        tambor_entry.delete(0,END)
        tambor_entry.insert(END,selected_item[5])
    except IndexError:
        pass

root = Tk()
root.resizable(1,1)
root.title("Modulo de Gestion de Envases")
root.iconbitmap("construction_barrel_oil_petroleum_tank_icon_153209.ico")


#marco para el campo de busqueda por cliente
frame_search = Frame(root)
frame_search.grid(row=0,column=0)

#etiqueta de texto para buscar por cliente
label_search = Label(frame_search, 
text="Rif del Cliente",
font=("bold",12),
padx=10,
pady=10)
#posicionamiento de la etiqueta
label_search.grid(row=0,column=0,sticky=W)

#campo para escribir el Rif
rif_search = StringVar()
rif_search_entry = Entry(frame_search,
                        textvariable=rif_search)
rif_search_entry.grid(row=0,column=1,padx=10)

#boton para crear cliente
create_cliente = Button(frame_search,
                        text="Crear cliente",
                        height=1,
                        width=12,
                        command=create_cliente_click)
create_cliente.grid(row=0,column=2,padx=5,pady=5)


#label para el nombre del cliente
label_client_name = Label(frame_search,
                        text="Nombre del Cliente",
                        font=("bold",12),
                        padx=10,
                        pady=10,
                        )
label_client_name.grid(row=1,column=0,sticky=W)

#campo para escribir el nombre del cliente
cliente_search = StringVar()
cliente_search_entry = Entry(frame_search,
                            textvariable=cliente_search)
cliente_search_entry.grid(row=1,column=1,padx=10)

create_cliente = Button(frame_search,
                        text="Buscar Nombre",
                        height=1,
                        width=12,
                        command=show_cliente_byname_click)
create_cliente.grid(row=1,column=2,padx=5,pady=5)


show_cliente = Button(frame_search,
                    text="Buscar Rif",
                    height=1,
                    width=12,
                    command=show_cliente_click,)
                    #command=show_cliente_click,)
show_cliente.grid(row=1,column=3,padx=5,pady=5)



#el frame para los campos escribibles
frame_fields = Frame(root)
frame_fields.grid(row=1,column=0,sticky=W,padx=70,pady=10)

#campos de los galones o cajas aun no se
galones_text = StringVar()
galones_text.set("0")
galones_label = Label(frame_fields, 
                        text= "Galones",
                        font=("bold", 12),
                        padx=0,
                        pady=5,)
galones_label.grid(row=0,column=0,sticky=W)
galones_entry = Entry(frame_fields,
                    textvariable=galones_text)
galones_entry.grid(row=0,column=1,sticky=W)

#campos de los cuñetes20L
cunete_text = StringVar()
cunete_text.set("0")
cunete_label = Label(frame_fields,
                    text="Cuñete20L",
                    font=("bold",12),
                    padx=0,
                    pady=5)
cunete_label.grid(row=1,column=0,sticky=W)
cunete_entry = Entry(frame_fields,
                    textvariable=cunete_text)
cunete_entry.grid(row=1, column=1,sticky=W)

#campos de las carbollas
carbolla_text = StringVar()
carbolla_text.set("0")
carbolla_label = Label(frame_fields,
                        text="Carbolla60L",
                        font=("bold",12),
                        padx=0,
                        pady=5)
carbolla_label.grid(row=2,column=0,sticky=W)
carbolla_entry = Entry(frame_fields, textvariable = carbolla_text)
carbolla_entry.grid(row=2,column=1,sticky=W)

#campo de los tambores
tambor_text = StringVar()
tambor_text.set("0")
tambor_label = Label(frame_fields,
                    text="Tambor210L",
                    font=("bold",12),
                    padx=0,
                    pady=5)
tambor_label.grid(row=3,column=0,sticky=W)
tambor_entry = Entry(frame_fields,textvariable = tambor_text)
tambor_entry.grid(row=3,column=1,sticky=W)


#boton sumar envases
sum_container = Button(frame_fields,
                        text="Sumar Envases",
                        height=1,
                        width=12,
                        command=sum_container_click,)
sum_container.grid(row=1,column=2,padx=20,pady=5)


#boton de restar envases
substract_container = Button(frame_fields,
                            text="Restar Envases",
                            height=1,
                            width=12,
                            command=subtract_container_click,)
substract_container.grid(row=2,column=2,padx=20,pady=5)




#todo este frame esta comentado porque le cambie la ubicacion a los unicos dos botones que tenia
"""
#frame de los botones
frame_buttons = Frame(root)
frame_buttons.grid(row=1,column=1,)



show_client = Button(frame_buttons,
                    text="Mostrar Cliente",
                    height=1,
                    width=12,
                    command=show_cliente_click,)
show_client.grid(row=0,column=0,padx=5,pady=5)


#boton sumar envases
sum_container = Button(frame_buttons,
                        text="Sumar Envases",
                        height=1,
                        width=12,
                        command=sum_container_click,)
sum_container.grid(row=1,column=0,padx=5,pady=5)

#boton de restar envases
substract_container = Button(frame_buttons,
                            text="Restar Envases",
                            height=1,
                            width=12,
                            command=subtract_container_click,)
substract_container.grid(row=2,column=0,padx=5,pady=5)
"""

#frame para las opciones de los radiobuton de actualizar y de borrar clientes
update_delete_frame = Frame(root)
update_delete_frame.grid(row=2,column=0,sticky=W,padx=10,pady=10)

clicked_option = IntVar()

update_cliente_radiobu = Radiobutton(update_delete_frame,
                                    text="Sobrescribir Cliente",
                                    variable=clicked_option,
                                    value=1)
update_cliente_radiobu.grid(row=0,column=0,sticky=W,pady=5)

delete_cliente_radiobu = Radiobutton(update_delete_frame, 
                                    text="Borrar Cliente", 
                                    variable=clicked_option,
                                    value=2)
delete_cliente_radiobu.grid(row=1,column=0,sticky=W,pady=5)

submit_button = Button(update_delete_frame,
                        text="Enviar",
                        command=submit_click)
submit_button.grid(row=2,column=0,sticky=W,padx=6,pady=5)



#frame de los resultados de los querys
result_frame = Frame(root)
result_frame.grid(row=0,
                column=2,
                columnspan=4,
                rowspan=6,
                padx=20,
                pady=20)

columns = ["Rif", 
            "Cliente",
            "Galones",
            "Cuñete20L",
            "Carbolla60L",
            "Tambor210L",
            "UltimaFacturacion",
            "UltimaDevolucion"]

#crear el treeview y ponerlo en su frame
cliente_tree_view = Treeview(result_frame,
                            columns=columns,
                            show="headings")

#estilo del treeview
style = ttk.Style()

#tema del treeview
style.theme_use("default")

#configuracion de los colores
style.configure("Treeview",
                background = "#D3D3D3",
                foreground = "black",
                rowheight = 25,
                fieldbackground = "D3D3D3")
                           
cliente_tree_view.column("Rif",width=80,minwidth=30)

#crear los encabezados para las columnas
for col in columns:
    if col == "UltimaFacturacion" or col == "UltimaDevolucion":
        cliente_tree_view.column(col,width = 115,anchor = W,stretch=True,minwidth=60)
        cliente_tree_view.heading(col,text = col, anchor = CENTER)
    else:
        cliente_tree_view.column(col,width = 80,anchor = W,stretch=True,minwidth=60)
        cliente_tree_view.heading(col,text = col, anchor = CENTER)

cliente_tree_view.bind("<<TreeviewSelect>>",select_cliente)
cliente_tree_view.pack(side="left",fill="y")
scrollbar = Scrollbar(result_frame,orient="vertical")
scrollbar.configure(command=cliente_tree_view.yview)
scrollbar.pack(side="right",fill="y")
cliente_tree_view.config(yscrollcommand=scrollbar.set)

#menu
menubar = Menu(root)
root.config(menu=menubar)

def quit_program():
    ansewer = messagebox.askquestion("Salir","¿Está seguro que desea salir?")
    if ansewer == "yes":
        return root.quit()
    else:
        return

def show_database():
    for i in cliente_tree_view.get_children():
        cliente_tree_view.delete(i)
    for row in db.Database(conect_to).show_data():
        cliente_tree_view.insert(parent="",
                                index="end",
                                values = row)

def export_database():
    file = filedialog.asksaveasfilename(title="Exportar como archivo Excel",defaultextension=".xlsx")
    if file != "":
        db.Database(conect_to).export_database(filename=file)
    else:
        pass
    

#filemenu
filemenu = Menu(menubar,tearoff = 0)
filemenu.add_command(label="Exportar Base de datos",command=export_database)
filemenu.add_separator()
filemenu.add_command(label="Salir",command=quit_program)


#editmenu
editmenu = Menu(menubar,tearoff = 0)
editmenu.add_command(label="Mostrar Base de datos",command=show_database)

"""
editmenu.add_separator()
editmenu.add_command(label="Sobrescribir Cliente",command=None)
editmenu.add_command(label="Borrar Cliente", command=None)
"""

#helpmenu
helpmenu = Menu(menubar,tearoff = 0)
helpmenu.add_command(label="Ver Documentacion")
helpmenu.add_command(label="Creditos")

#agregar a la barra de menus
menubar.add_cascade(label="Archvio", menu=filemenu)
menubar.add_cascade(label="Base de Datos", menu=editmenu)
#menubar.add_cascade(label="Ayuda", menu=helpmenu)

root.mainloop()