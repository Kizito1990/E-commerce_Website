from .models import Contact

def contact_details(request):
    contacts = Contact.objects.all()
    return {'contacts': contacts}
