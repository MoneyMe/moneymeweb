from django.shortcuts import render_to_response, HttpResponseRedirect
from django.core.urlresolvers import reverse
from moneymeweb.expense.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    print("Main... redirectings...")
    groups = request.user.get_profile().get_groups_name()
    if u'Client' in groups and u'Supplier' not in groups: # simple user
        return HttpResponseRedirect(reverse("user_home"))
    elif u'Supplier' in groups and u'Client' not in groups:
        return HttpResponseRedirect(reverse("supplier_home"))

@login_required
def user_home(request):
    return render_to_response('user_home.html')

@login_required
def supplier_home(request):
    return render_to_response('supplier_home.html')
