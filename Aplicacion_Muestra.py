import streamlit as st
from Database_SQL import Database

# function to sum
def my_sum(x, y):
    return x+y

# function to rest

def my_rest(x=4,y=5):

    return x-y

# start Connection
database = Database()

st.header(" Hielo Gran Pacífico")
st.sidebar.write("# Panel de usuario")
st.write("Aplicación para acceder y actualizar la base de datos")

# Table(
table = st.sidebar.selectbox("Tabla", ("Productos", "Clientes", "Empleados"))

# Select the product with the ID = id and the TABLE = table
col1, col2 = st.columns(2)

with col1:
    st.subheader("{}".format(table))
    st.write(database.select(table, attribute=None, column=None, value=None))

with col2:
    if table == "Productos":
        st.subheader("Clientes")
        st.write(database.select(table="Clientes",
                 attribute=None, column=None, value=None))
    else:
        pass

# Panel de Ventas
st.subheader("Panel de ventas")
col_1, col_2 = st.columns(2)

submitted2 = False
submitted3 = False

with col_1:

    with st.form(key='Producto'):

        Productos = database.select(
            table='Productos', attribute=None, column=None, value=None)
        ids = [i+1 for i in range(len(Productos))]
        ID = st.selectbox("Producto ID", ids, index=1, key=1)
        submitted1 = st.form_submit_button('Seleccionar')

    with st.form(key='Panel de ventas'):

        Producto = database.select(table='Productos',
                                   attribute='id',
                                   column=None,
                                   value=ID)
        Nombre = Producto.at[ID, 'producto']
        st.write(f'Producto seleccionado: {Nombre}')
        Precio = Producto.at[ID, 'precio']
        Cantidad = Producto.at[ID, 'cantidad']
        Unidades = st.number_input(f'Seleccione el número de unidades que desea retirar (Cantidad disponible: {Cantidad})',
                                   value=0)

        submitted2 = st.form_submit_button('OK')

    if submitted2:
        if Unidades > Cantidad:
            st.error('No existen suficientes unidades en el Inventario.')

with col_2:

    with st.form(key='Empleado'):

        id_e = [i for i in range(1, 5)]
        ID_E = st.selectbox(
            'Selecciona el ID del empleado que realizara la venta', id_e, index=1, key=2)
        submitted3 = st.form_submit_button('OK')
        Empleado = database.select(table='Empleados',
                                   attribute='id',
                                   column=None,
                                   value=ID_E)

        Nombre_empleado = Empleado.at[ID_E, 'nombre']
        Ventas = Empleado.at[ID_E, 'ventas']

    with st.form(key='Realizar Compra'):
        if Unidades <= Cantidad:

            Precio_total = Unidades*Precio
            Cantidad_final = Cantidad - Unidades
            Ventas_f = Ventas + Precio_total

            st.write(f'Empleado que realizará la venta: {Nombre_empleado}')
            st.write(f'Producto: {Nombre}')
            st.write(f'Unidades: {Unidades}')
            st.write(f'Precio Unitario: {Precio}')
            st.write(f'Precio total: ${Precio_total}')

            submitted4 = st.form_submit_button('Realizar venta')

            if submitted4:
                database.update(table='productos',
                                column='cantidad',
                                attribute='id',
                                id=ID,
                                value=Cantidad_final)
                database.update(table='empleados',
                                column='ventas_totales',
                                attribute='id',
                                id=ID_E,
                                value=Ventas_f)
                database.close()
                st.success('La venta se ha realizado exitosamente')
