from django.shortcuts import get_object_or_404, render
from .models import Product, Member, CashLog
from django.utils import timezone
from django.core.urlresolvers import reverse
import sys

def index(request, error=""):




    #buy or reset the cart
    try:
        func = request.POST['function']
    except:
        pass
    else:
        if func == 'rst':
            request.session.clear()
        elif func == 'buy':
            m = Member.objects.get(nick=request.session["cart"])
            tp = 0
            isMember = request.session.get('isMember', True)
            for item in Product.objects.values_list('barcode', flat=True).distinct():
                if item in request.session:
                    p = Product.objects.get(barcode=item)
                    pcount = request.session[item]
                    if isMember:
                        p.price -= p.member_discount
                    total_price = pcount * p.price
                    tp += total_price
                    m.balance -= total_price
                    m.consume += pcount
                    cs = CashLog(member=m, product=p, count=pcount, price=total_price, purchase_date=timezone.now())
                    cs.save()
            m.save()
            request.session.clear()
            if isMember:
                error += "Du hast für " + str(tp) + "€ eingekauft.\n Der neue Kontostand ist " + str(m.balance) + "€\n Vielen Dank!"
            else:
                error += "Bitte lege jetzt " + str(tp) + "€ in die Matekasse. Vielen Dank!"

    # add or delete a product from cart
    try:
        bc = request.POST['barcode']
        func = request.POST['function']
    except:
        pass
    else:
        if func == 'add':
            if Member.objects.filter(number=bc).exists():
                member = Member.objects.get(number=bc)
                request.session['cart'] = member.nick
                request.session['isMember'] = True
                if member.balance <= 0:
                    error += "Achtung: Dein Prepaidkonto ist bei "+ str(member.balance) +"€\n"
            elif bc in Product.objects.values_list('barcode', flat=True).distinct():
                if bc in request.session:
                  request.session[bc] += 1
                else:
                    request.session[bc] = 1
            else:
                error = 'Cannot add item. Item is invalid'

        elif func == 'del':

            if bc in request.session:
                if request.session[bc] > 1:
                    request.session[bc] -= 1
                else:
                    del request.session[bc]
            else:
                error = 'Cannot delete item. Item is invalid'

        else:
            error += "Unknown function call\n"
    try:
        request.session['cart'] = request.POST['selected_member']
    except:
        pass
    else:
        if not request.session['cart'] == 'Anonymous':
            request.session['isMember'] = True
            balance = Member.objects.get(nick=request.session['cart']).balance
            if balance <= 0:
                error += "Achtung: Dein Prepaidkonto ist bei "+ str(balance) +"€\n"
        else:
            request.session['isMember'] = False

    # first run
    if 'cart' not in request.session:
        #create cart with Anonymous as default cart owner
        request.session['cart'] = 'Anonymous'
        request.session['isMember'] = False
        request.session.set_expiry(600)

    #create template product variables
    product_list = []
    cart_list = []
    member_list = []
    total_price = 0
    for product in  Product.objects.order_by('-name'):
        if not product.stock <= 0:
            if request.session.get('isMember', True):
                product.price -= product.member_discount
            # if not a member dont add Product Prepaid from product list
            elif product.name == 'Prepaid':
                continue
            product_list.append(product)

    #create template product variables in cart
    for item in Product.objects.values_list('barcode', flat=True).distinct():
        if item in request.session:
            p = Product.objects.get(barcode=item)
            p.count = request.session[item]
            if request.session.get('isMember', True):
                p.price -= p.member_discount
            p.total_price = p.count * p.price
            total_price += p.total_price
            cart_list.append(p)

    #create member list variables
    for member in Member.objects.order_by('-consume'):
        member_list.append(member.nick)

    #call render with context
    context = {'product_list': product_list, 'cart_list': cart_list, 'total_price': total_price, 'member_list': member_list, 'error': error}
    return render(request, 'millipays/index.html', context)
