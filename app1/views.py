from django.shortcuts import render, redirect, get_object_or_404
#importar un módulo
from django.http import HttpResponse
from . models import stores, products
from .forms import newstoreform, newproductform, newcontactform
from email.message import EmailMessage
import smtplib
from django.views.generic import (ListView)



 
def home(request):
    return render(request,'home.html')


#función info
def info(request):
    nombre=['DevHeidi']
    return render(request, 'info.html',{
        'name':nombre
    })


def stores_view(request):
    s=stores.objects.all()
    return render (request, 'stores.html',{
        'stores': s
    })

def products_view(request):
    p=products.objects.all()
    return render(request,'products.html',{
        'products':p
    })

def create_store(request):
    if request.method=='GET':
        return render(request, 'create_store.html',{
        'forms':newstoreform()
    })
    else:
        stores.objects.create(name=request.POST['name'],description=request.POST['description'])
        return redirect('stores')

def create_product(request):
    if request.method=='GET':
        return render(request, 'create_product.html',{
            'forms': newproductform(),
            'stores': stores.objects.all()
        })
    else:
        store_id = request.POST['store']
        store_obj = stores.objects.get(id=store_id)

        products.objects.create(
            title=request.POST['title'],
            price=request.POST['price'],
            store=store_obj
        )

        return redirect('products')


def details(request,id):
    s=stores.objects.get(id=id)
    p=products.objects.filter(store_id=id)
    return render(request,'details.html', {
        'store':s,
        'products':p
    })

    
def contact(request):
    if request.method == 'GET':
        return render(request, 'contact.html', {'form': newcontactform()})
    else:
        try:
            remitente = "programadores303@gmail.com"
            destinatario = request.POST['email']
            password_app = "vmtujjfepajxyrem"  # REEMPLAZA TU_CONTRASEÑA_AQUÍ
             
            # CONSTRUIR MENSAJE CON PRODUCTOS
            mensaje = """Saludos, gracias por contactarnos.Nuestros productos son los siguientes:
        """
            
            for i in products.objects.all():
                mensaje = mensaje + str(i) + ' - $' + str(i.price) + '\n'
            
            email = EmailMessage()
            email["From"] = remitente
            email["To"] = destinatario
            email["Subject"] = "Contacto tienda - Nuestros Productos DevLiz"
            email.set_content(mensaje)  # IMPORTANTE: asignar el mensaje
            
            # ENVIAR CORREO
            smtp = smtplib.SMTP("smtp.gmail.com", 587)
            smtp.starttls()
            smtp.login(remitente, password_app)
            smtp.sendmail(remitente, destinatario, email.as_string())
            smtp.quit()
            
            return redirect('home')
            
        except Exception as e:
            return render(request, 'contact.html', {
                'form': newcontactform(),
                'error': f'Error: {str(e)}'
            })


# función despedirse

def despedirse(request):
    return HttpResponse('<h1>¡Adiós!</h1>')

class ProductosListView(ListView):
    context_object_name='productos'
    template_name = "filtro.html"
   
    def get_queryset(self):
        print('*************************')
        palabra_clave=self.request.GET.get("kword",'')
        print('=================',palabra_clave)
        lista=products.objects.filter(title=palabra_clave)
        return lista

class StoreListView(ListView):
    context_object_name = 'stores'
    template_name = "filtro_tienda.html"
   
    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", "").strip()
        
        # Solo buscar si hay palabra clave
        if palabra_clave:
            return stores.objects.filter(name__icontains=palabra_clave)
        else:
            # Retornar lista vacía si no hay búsqueda
            return stores.objects.none()

# Actualizar un productos
def update_product(request):
    if request.method == "GET":

        # El usuario todavía no ha buscado nada
        if "kword" not in request.GET:
            return render(request, "update_product.html")

        # Buscar producto por nombre
        nombre = request.GET.get("kword", "")

        try:
            product = products.objects.get(title=nombre)
        except products.DoesNotExist:
            return render(request, "update_product.html", {
                "error": "No existe un producto con ese nombre."
            })

        # Si encuentra el producto, mostrar el form con datos
        form = newproductform(initial={
            "title": product.title,
            "price": product.price,
            "store": product.store.name
        })

        return render(request, "update_product.html", {
            "forms": form,
            "product": product
        })

    else:
        # Actualizar el producto
        nombre_original = request.POST.get("title_original")
        product = products.objects.get(title=nombre_original)

        form = newproductform(request.POST)
        if form.is_valid():
            store_obj = stores.objects.get(name=form.cleaned_data["store"])

            product.title = form.cleaned_data["title"]
            product.price = form.cleaned_data["price"]
            product.store = store_obj
            product.save()

            return redirect("products")

        return render(request, "update_product.html", {
            "forms": form,
            "error": "Datos inválidos"
        })


def update_stores(request):
    if request.method == "GET":
        # Si el usuario aún no ha buscado nada
        if "kword" not in request.GET:
            return render(request, "update_stores.html")

        # Buscar tienda por nombre
        nombre = request.GET.get("kword", "").strip()

        try:
            store = stores.objects.get(name__iexact=nombre)
        except stores.DoesNotExist:
            return render(request, "update_stores.html", {
                "error": f"No existe una tienda con el nombre '{nombre}'."
            })

        # Inicializar el form con los datos de la tienda
        form = newstoreform(initial={
            "name": store.name,
            "description": store.description
        })

        return render(request, "update_stores.html", {
            "form": form,
            "store": store
        })

    else:
        # Actualizar la tienda
        nombre_original = request.POST.get("name_original")
        store = get_object_or_404(stores, name=nombre_original)

        form = newstoreform(request.POST)
        if form.is_valid():
            store.name = form.cleaned_data["name"]
            store.description = form.cleaned_data["description"]
            store.save()
            return redirect("stores")  # Redirigir a la lista de tiendas

        return render(request, "update_stores.html", {
            "form": form,
            "error": "Datos inválidos"
        })


def delete_product(request):
    context = {}

    if request.method == 'POST':
        kword = request.POST.get('kword', '').strip()

        if kword != "":
            try:
                obj = products.objects.get(title__iexact=kword)
                obj.delete()
                context['mensaje'] = f"Producto '{kword}' eliminado correctamente."
            except products.DoesNotExist:
                context['error'] = f"No se encontró el producto '{kword}'."

    return render(request, 'delete_product.html', context)

def delete_stores(request):
    context = {}

    if request.method == 'POST':
        kword = request.POST.get('kword', '').strip()

        if kword != "":
            try:
                store = stores.objects.get(name__iexact=kword)
                store.delete()
                context['mensaje'] = f"Tienda '{kword}' eliminada correctamente."
            except stores.DoesNotExist:
                context['error'] = f"No se encontró la tienda '{kword}'."

    return render(request, 'delete_stores.html', context)

