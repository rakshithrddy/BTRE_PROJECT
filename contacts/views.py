from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from .models import Contact


def contact(request):
    if request.method == 'POST':
        listing = request.POST['listing']
        listing_id = request.POST['listing_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request=request, message='You have already made the inquiry for this listing')
                return redirect(f'/listings/{listing_id}')

        contact_ = Contact(listing=listing, listing_id=listing_id, name=name, email=email,
                           phone=phone, message=message, user_id=user_id)
        contact_.save()
        send_mail(
            'Property Listings Inquiry',
            f'There has been an inquiry for {listing}. Sign into admin panel for more info.',
            f'rakshith.yn@gmail.com',
            [realtor_email, 'rakshith.yn@gmail.com'],
            fail_silently=False
        )
        messages.success(request=request, message='You have successfully submitted the inquiry')
        return redirect(f'/listings/{listing_id}')
    return redirect('listings')
