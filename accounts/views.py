from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.forms import RegistrationForms, UserForm, UserProfileForm
from accounts.models import Account, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

from carts.models import Cart, CartItem
from carts.views import _cart_id
import requests

from orders.models import Order, OrderProduct

from django.utils.translation import gettext_lazy as _ 

# Create your views here.

def register(request):
    
    if request.method == "POST":
        form = RegistrationForms(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            
            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verication_email.html', {
                "user": user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            })
            print(message)
            
            to_email = email
            send_email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForms()
    context = {
        'form': form,
    }
    return render(request,'accounts/register.html', context)


def login(request):
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        # user = auth.authenticate(email=email, password=password)
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    # Getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                        
                    # Get the cart items fom the user to access his product variations    
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                        
                    
                    
                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, _('You are now logged in.'))
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, _('Invalid login credentials'))
            return redirect('login')
        
    return render(request,'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, _('You are logged out.'))
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, _('Congratulation Your account is activated.'))
        return redirect('login')
    else:
        messages.error(request, _('Invalid activation link.'))
        return redirect('register')
    
    
@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        # Créer un profil utilisateur pour l'utilisateur actuel
        userprofile = UserProfile.objects.create(user=request.user)
    
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password.'
            message = render_to_string('accounts/reset_password_email.html', {
                "user": user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            })
            print(message)
            
            to_email = email
            send_email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[to_email])
            send_email.send()
            
            messages.success(request, _('Password reset email has been sent to your email address.'))
            
            return redirect('login')
            
        else:
            messages.error(request, _('Account does not exist.'))
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, _('Please reset your password'))
        return redirect('resetPassword')
    else:
        messages.error(request, _('This link has been expired!'))
        return redirect('login')
        
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password'] 
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, _('Password reset successful'))
            return redirect('login')
        else:
            messages.error(request, _('Password do not match.'))
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user_id=request.user.id, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile has been updated.'))
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user = Account.objects.get(username__exact=request.user.username)
        
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, _('Password updated successfully.'))
                return redirect('change_password')
            else:
                messages.error(request, _('Please enter valid current password.'))
                return redirect('change_password')
        else:
            messages.error(request, _('Please does not match.'))
            return redirect('change_password')
        
    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    
    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)


###########################################

"""
import io
from django.http import FileResponse
from django.views import View
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle

class DownloadInvoiceView(View):
    def get(self, request, order_id):
        order_detail = OrderProduct.objects.filter(order__order_number=order_id)
        order = Order.objects.get(order_number=order_id)
        subtotal = 0
        for item in order_detail:
            subtotal += item.product_price * item.quantity

        # Create a file-like buffer to receive PDF data
        buffer = io.BytesIO()

        # Create the PDF object using the buffer as its "file"
        p = canvas.Canvas(buffer, pagesize=letter)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # You can use the ReportLab canvas methods to add text, images, tables, etc.
        # Refer to the ReportLab documentation for more details: https://www.reportlab.com/docs/reportlab-userguide.pdf

        # Set the font and size
        p.setFont("Helvetica", 12)

        # Draw the image
        logo_path = r"ecommerce\static\images\logo.png"  # Replace this with the actual path to your image
        p.drawImage(logo_path, 100, 750, width=1.5*inch, height=0.5*inch)

        # Write the invoice content
        p.drawString(100, 750, f"Invoice for Order {order.order_number}")
        p.drawString(100, 700, f"Customer: {order.full_name}")
        p.drawString(100, 680, f"Address: {order.full_address}, {order.city}, {order.state}, {order.country}")
        p.drawString(100, 660, f"Email: {order.email}")

        # Create the data for the table
        table_data = [['Product', 'Quantity', 'Price']]
        for item in order_detail:
            table_data.append([item.product.product_name, str(item.quantity), str(item.product.price)])

        # Define the table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'grey'),  # Background color for the header row
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),  # Text color for the header row
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font name for the header row
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # Font size for the header row
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Bottom padding for the header row
            ('BACKGROUND', (0, 1), (-1, -1), 'beige'),  # Background color for the data rows
            ('TEXTCOLOR', (0, 1), (-1, -1), 'black'),  # Text color for the data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Font name for the data rows
            ('FONTSIZE', (0, 1), (-1, -1), 10),  # Font size for the data rows
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alignment for all cells
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment for all cells
            ('LINEABOVE', (0, 0), (-1, -1), 1, 'black'),  # Line above for all cells
            ('LINEBELOW', (0, 0), (-1, -1), 1, 'black'),  # Line below for all cells
            ('BOX', (0, 0), (-1, -1), 1, 'black'),  # Box around the table
        ])

        # Create the table object
        table = Table(table_data)

        # Apply the table style
        table.setStyle(table_style)

        # Draw the table on the canvas
        table.wrapOn(p, 400, 200)  # Set the table width and height
        table.drawOn(p, 100, 550)  # Set the table position

        # Calculate the position for the total section
        y = 500 - (len(order_detail) * 20)  # Adjust the y-position based on the number of products

        p.drawString(100, y - 40, f"Sub Total: {subtotal} FCFA")
        p.drawString(100, y - 60, f"Tax: {order.tax} FCFA")
        p.drawString(100, y - 80, f"Grand Total: {order.order_total} FCFA")

        # Close the PDF object cleanly and we're done
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers present the option to save the file
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"{order_id}.pdf")

"""