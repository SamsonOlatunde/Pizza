from django.http import request
from django.shortcuts import render
from .forms import Pizzaform, MultiplePizzaForms
from django.forms import formset_factory
from .models import Pizza


def home(request):
    return render(request, 'pizza/home.html', {})


def order(request):
    multiple_form = MultiplePizzaForms()
    if request.method == 'POST':
        filled_form = Pizzaform(request.POST)
        if filled_form.is_valid():
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            note = 'Thanks for ordering, your %s %s and %s pizza is on its way!' % (
                filled_form.cleaned_data['size'], filled_form.cleaned_data['topping1'],
                filled_form.cleaned_data['topping2'],)
            filled_form = Pizzaform()
        else:
            created_pizza_pk = None
            note = 'Pizza order failed, please try again'
        return render(request, 'pizza/order.html', {'created_pizza_pk': created_pizza_pk, 'pizzaform': filled_form, 'note': note, 'multiple_form': multiple_form})
    else:
        form = Pizzaform()
        return render(request, 'pizza/order.html', {'pizzaform': form, 'multiple_form': multiple_form})

def edit_order(request, pk):
    pizza = Pizza.objects.get(pk=pk)
    form = Pizzaform(instance=pizza)
    if request.method == 'POST':
        filled_form = Pizzaform(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = "Order has been updated"
            return render(request, 'pizza/edit_order.html', {'note': note, 'pizzaform': form, 'pizza': pizza})
    return render(request, 'pizza/edit_order.html', {'pizzaform': form, 'pizza': pizza})


def pizzas(request):
    global filled_formset
    number_of_pizzas = 2
    filled_multiple_pizza_form = MultiplePizzaForms(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['numbers']
    PizzaFormset = formset_factory(Pizzaform, extra=number_of_pizzas)
    formset = PizzaFormset()
    if request.method == "POST":
        filled_formset = PizzaFormset(request.POST)
        if filled_formset.is_valid():
            filled_formset.save()
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
            note = 'Pizza have been ordered!'
        else:
            note = 'Order was not created, please try again'

        return render(request, 'pizza/pizzas.html', {'note': note, 'formset': formset})
    else:
        return render(request, 'pizza/pizzas.html', {'formset': formset})

