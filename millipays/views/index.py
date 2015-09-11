import sys

from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.core.urlresolvers import reverse

from millipays.models import Product, Member, CashLog


def index(request, error=''):
    # buy or reset the cart
    try:
        func = request.POST['function']
    except KeyError:
        pass
    else:
        if func == 'rst':
            # resets the order
            request.session.clear()

        elif func == 'buy':
            # confirms the order
            member = Member.objects.get(nick=request.session['cart'])
            is_member = request.session.get('isMember', True)

            total = 0
            # work through the cart and buy all products
            for item in Product.objects.values_list('barcode', flat=True).distinct():
                if item in request.session:
                    product = Product.objects.get(barcode=item)
                    count = request.session[item]

                    # determine price
                    if is_member:
                        product.price -= product.member_discount
                    product_total = count * product.price
                    total += product_total

                    # update members balance
                    member.balance -= product_total
                    member.consume += count

                    # add log entry
                    cs = CashLog(member=member, purchase_date=timezone.now(),
                                 product=product, count=count, price=product_total)
                    cs.save()

            member.save()
            request.session.clear()

            # response
            if is_member:
                error += "Du hast für {total} EUR eingekauft.\n" \
                         "Der neue Kontostand ist nun {balance}.\n" \
                         "Danke für deinen Einkauf!".format(total=total, balance=member.balance)
            else:
                error += "Bitte nun {total} EUR in die Kasse legen.\n" \
                         "Danke für deinen Einkauf!".format(total=total)

    # add or delete a product from cart
    try:
        ean = request.POST['barcode']
        func = request.POST['function']
    except KeyError:
        pass
    else:
        if func == 'add':
            # add product to cart
            if Member.objects.filter(number=ean).exists():
                # TODO: describe what happens here
                member = Member.objects.get(number=ean)
                request.session['cart'] = member.nick
                request.session['isMember'] = True
                if member.balance <= 0:
                    error += "Achtung: Bitte lade dein Prepaidkonto auf! " \
                             "Aktueller Kontostand: {balance} EUR.".format(balance=member.balance)

            elif ean in Product.objects.values_list('barcode', flat=True).distinct():
                # TODO: describe what happens here
                if ean in request.session:
                    request.session[ean] += 1
                else:
                    request.session[ean] = 1
            else:
                error += 'Produkt konte nicht hinzugefügt werden: EAN ist nicht bekannt!\n'

        elif func == 'del':
            # remove product from cart
            if ean in request.session:
                if request.session[ean] > 1:
                    request.session[ean] -= 1
                else:
                    del request.session[ean]
            else:
                error += 'Produkt konnte nicht entfernt werden: EAN ist nicht bekannt!\n'

        else:
            error += 'Unknown function call\n'

    # handle user selection
    try:
        request.session['cart'] = request.POST['selected_member']
    except KeyError:
        pass
    else:
        if not request.session['cart'] == 'Anonymous':
            request.session['isMember'] = True
            balance = Member.objects.get(nick=request.session['cart']).balance
            if balance <= 0:
                error += "Achtung: Bitte lade dein Prepaidkonto auf! "\
                         "Aktueller Kontostand: {balance} EUR\n".format(balance=balance)
        else:
            request.session['isMember'] = False

    # first run
    if 'cart' not in request.session:
        # create cart with Anonymous as default cart owner
        request.session['cart'] = 'Anonymous'
        request.session['isMember'] = False
        request.session.set_expiry(600)

    # create template product variables
    product_list = []
    cart_list = []
    member_list = []
    total_price = 0
    for product in Product.objects.order_by('-name'):
        if not product.stock <= 0:
            if product.name == 'UeberweisungsPrepaid':
                continue
            elif request.session.get('isMember', True):
                product.price -= product.member_discount
            # if not a member dont add Product Prepaid from product list
            elif product.name == 'Prepaid':
                continue
            product_list.append(product)

    # create template product variables in cart
    for item in Product.objects.values_list('barcode', flat=True).distinct():
        if item in request.session:
            product = Product.objects.get(barcode=item)
            product.count = request.session[item]
            if request.session.get('isMember', True):
                product.price -= product.member_discount
            product.total_price = product.count * product.price
            total_price += product.total_price
            cart_list.append(product)

    # create member list variables
    for member in Member.objects.order_by('-consume'):
        member_list.append(member.nick)

    # call render with context
    context = {'product_list': product_list, 'cart_list': cart_list, 'total_price': total_price,
               'member_list': member_list, 'error': error}
    return render(request, 'millipays/index.html', context)
