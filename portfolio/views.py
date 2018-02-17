from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import datetime

def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})

#################
### CUSTOMERS ###
#################
@login_required
def customer_list(request):
   customers = Customer.objects.filter(created_date__lte=timezone.now())
   return render(request, 'portfolio/customer_list.html',
                 {'customers': customers})

@login_required
def customer_new(request):
   if request.method == "POST":
       form = CustomerForm(request.POST)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.created_date = timezone.now()
           customer.save()
           customers = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customers})
   else:
       form = CustomerForm()
   return render(request, 'portfolio/customer_new.html', {'form': form})

@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customer})
   else:
       # edit
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('portfolio:customer_list')

##############
### STOCKS ###
##############
@login_required
def stock_list(request):
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})

@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})

@login_required
def stock_edit(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   if request.method == "POST":
       form = StockForm(request.POST, instance=stock)
       if form.is_valid():
           stock = form.save()
           # stock.customer = stock.id
           stock.updated_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
   else:
       form = StockForm(instance=stock)
   return render(request, 'portfolio/stock_edit.html', {'form': form})

@login_required
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    stock.delete()
    stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
    return render(request, 'portfolio/stock_list.html', {'stocks': stocks})

###################
### INVESTMENTS ###
###################
@login_required
def investment_list(request):
    investments = Investment.objects.filter(recent_date__lte=timezone.now())
    return render(request, 'portfolio/investment_list.html', {'investments': investments})

@login_required
def investment_new(request):
    if request.method == "POST":
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.created_date = timezone.now()
            investment.save()
            investments = Investment.objects.filter(recent_date__lte=timezone.now())
            return render(request, 'portfolio/investment_list.html', {'investments': investments})
    else:
        form = InvestmentForm
    return render(request, 'portfolio/investment_new.html', {'form': form})

@login_required
def investment_edit(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    if request.method == "POST":
        form = InvestmentForm(request.POST, instance=investment)
        if form.is_valid():
            investment = form.save()
            investment.updated_date = timezone.now()
            investment.save()
            investments = Investment.objects.filter(recent_date__lte=timezone.now())
            return render(request, 'portfolio/investment_list.html', {'investments': investments})
    else:
        form = InvestmentForm(instance=investment)
    return render(request, 'portfolio/investment_edit.html', {'form': form})

@login_required
def investment_delete(request, pk):
    investment = get_object_or_404(Investment, pk=pk)
    investment.delete()
    investments = Investment.objects.filter(recent_date__lte=timezone.now())
    return render(request, 'portfolio/investment_list.html', {'investments': investments})
'''
@login_required
def portfolio(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments =Investment.objects.filter(customer=pk)
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    print(sum_acquired_value)

    stocks = Stock.objects.filter(customer=pk)

    initial_stock_value_sum = Stock.objects.filter(customer=pk).aggregate(Sum('initial_stock_value'))
    current_stock_value = 10000
    dict = {'customers': customers,
            'investments': investments,
            'stocks': stocks,
            'sum_acquired_value': sum_acquired_value,
            'initial_stock_value_sum':'aaaaa',
            'current_stock_value':current_stock_value,}

    return render(request, 'portfolio/portfolio.html', {'dictionary':dict})
'''
@login_required
def profile_temp(request):
    return render(request, 'portfolio/profile_temp.html')
''' SAFETY
@login_required
def portfolio(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())

    # STOCKS
    stocks = Stock.objects.filter(customer=pk)
    # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stocks_value = 0
    # Loop through each stock and add the value to the total
    for stock in stocks:
        #sum_current_stocks_value += stock.current_stock_value()
        try:
            sum_current_stocks_value += stock.current_stock_price()[1]
        except TypeError:
            pass
        sum_of_initial_stocks_value += stock.initial_stock_value()
'''

@login_required
def portfolio(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())

    # STOCKS
    stocks = Stock.objects.filter(customer=pk)
    # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stocks_value = 0
    # Loop through each stock and add the value to the total
    for stock in stocks:
        #sum_current_stocks_value += stock.current_stock_value()
        try:
            sum_current_stocks_value += stock.current_stock_price()[1]
        except TypeError:
            pass
        sum_of_initial_stocks_value += stock.initial_stock_value()

    # INVESTMENTS
    investments = Investment.objects.filter(customer=pk)
    sum_current_investments_value = 0
    sum_of_initial_investments_value = 0
    for investment in investments:
        sum_current_investments_value += investment.recent_value
        sum_of_initial_investments_value += investment.acquired_value

    portfolio_initial_investments = sum_of_initial_stocks_value + sum_of_initial_investments_value
    portfolio_current_investments = sum_current_stocks_value + float(sum_current_investments_value)


    return render(request, 'portfolio/portfolio.html', {'customers': customers,
                                                        'investments': investments,
                                                        'stocks': stocks,
                                                        'customer' :customer,
                                                        'sum_current_stocks_value': sum_current_stocks_value,
                                                        'sum_of_initial_stocks_value': sum_of_initial_stocks_value,
                                                        'sum_current_investments_value':sum_current_investments_value,
                                                        'sum_of_initial_investments_value':sum_of_initial_investments_value,
                                                        'portfolio_initial_investments':portfolio_initial_investments,
                                                        'portfolio_current_investments':portfolio_current_investments,})
@login_required
def portfolio_pdf(request, pk):
    ####
    response = HttpResponse(content_type='application/pdf')

    customer = get_object_or_404(Customer, pk=pk)
    customerName = customer.name
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")
    filename = str(customerName) + '_Portfolio_' + now + '.pdf'
    response['Content-Disposition'] = 'attachment; filename=' + filename

    # STOCKS
    stocks = Stock.objects.filter(customer=pk)
    # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stocks_value = 0
    # Loop through each stock and add the value to the total
    for stock in stocks:
        #sum_current_stocks_value += stock.current_stock_value()
        try:
            sum_current_stocks_value += stock.current_stock_price()[1]
        except TypeError:
            pass
        sum_of_initial_stocks_value += stock.initial_stock_value()

    # INVESTMENTS
    investments = Investment.objects.filter(customer=pk)
    sum_current_investments_value = 0
    sum_of_initial_investments_value = 0
    for investment in investments:
        sum_current_investments_value += investment.recent_value
        sum_of_initial_investments_value += investment.acquired_value

    portfolio_initial_investments = sum_of_initial_stocks_value + sum_of_initial_investments_value
    portfolio_current_investments = sum_current_stocks_value + float(sum_current_investments_value)

    p = canvas.Canvas(response)
    p.drawString(100,100,"Hello world.")
    p.showPage()
    p.save()
    return response

class CustomerList(APIView):
    def get(self, request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)
