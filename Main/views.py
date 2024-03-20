from django.shortcuts import render, redirect
from Main.models import Account

# Create your views here.
from django.views.generic.base import TemplateView
 
class HomePage(TemplateView):
    template_name = 'home.html'
    
    
    
def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email'
        account_name = request.POST.get('account_name')
        account_bio = request.POST.get('account_bio', '')

        account = Account.objects.create(username=username, email=email, account_name=account_name, account_bio=account_bio)
        return redirect('account_created')
    return render(request, 'create_account.html')

def search_account(request):
    query = request.GET.get('q')
    accounts = Account.objects.filter(account_name__icontains=query)
    return render(request, 'search_accounts.html', {'users': users, 'query': query})