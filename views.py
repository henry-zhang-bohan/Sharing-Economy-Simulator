from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as logout_django
from django.views.decorators.csrf import csrf_protect
from .models import Profile, MarketItem, Item, Comment
from django.utils import timezone
from django.shortcuts import get_object_or_404
from decimal import *

# Create your views here.
@csrf_protect
def login_simulator(request):
	username = request.POST["username"]
	password = request.POST["password"]
	user = authenticate(username = username, password = password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect(reverse('simulator:interface'))
		else:
			return HttpResponse('This user is disabled.<br /><a href = "../">Go Back</a>')
	else:
		return HttpResponse('Invalid Login. Please check your password.<br /><a href = "../">Try Again</a>')


@csrf_protect
def login_sharing_simulator(request):
	username = request.POST["username"]
	password = request.POST["password"]
	user = authenticate(username = username, password = password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect(reverse('simulator:sharing_interface'))
		else:
			return HttpResponse('This user is disabled.<br /><a href = "../">Go Back</a>')
	else:
		return HttpResponse('Invalid Login. Please check your password.<br /><a href = "../">Try Again</a>')

	
@csrf_protect
def logout_simulator(request):
	logout_django(request)
	return HttpResponseRedirect(reverse('login:index'))


def index(request):
	return render(request, 'simulator/index.html')

def interface(request):
	user = request.user
	to_sell_list = Item.objects.filter(owner = user, on_market = False, sharing = False)
	on_sale_list = Item.objects.filter(owner = user, on_market = True, sharing = False)
	to_buy_list = Item.objects.filter(on_market = True, sharing = False)
	reference_price_list = MarketItem.objects.all()
	capital = user.profile.capital
	comment_list = Comment.objects.order_by('-time')[:5]
	new_comment_list = []
	for i in range(len(comment_list)):
		new_comment_list.append(comment_list[len(comment_list) - 1 - i])
	price_list = range(101)
	
	# personal asset
	personal_asset = 0
	for my_item in Item.objects.filter(owner = user, sharing = False):
		personal_asset += my_item.value.current_value
	net_worth = personal_asset + capital
	
	# market value
	market_value = 0
	for market_item in Item.objects.filter(on_market = True, sharing = False):
		market_value += market_item.value.current_value

	context = {'to_sell_list': to_sell_list,
	           'on_sale_list': on_sale_list,
	           'to_buy_list': to_buy_list,
	           'reference_price_list': reference_price_list,
	           'user': user,
	           'capital': capital,
	           'comment_list': new_comment_list,
	           'price_list':price_list,
	           'personal_asset': personal_asset,
	           'market_value': market_value,
	           'net_worth': net_worth}
	return render(request, 'simulator/interface.html', context)


def sharing_interface(request):
	user = request.user
	to_sell_list = Item.objects.filter(owner = user, on_market = False, sharing = True)
	on_sale_list = Item.objects.filter(owner = user, on_market = True, sharing = True)
	to_buy_list = Item.objects.filter(on_market = True, sharing = True)
	reference_price_list = MarketItem.objects.all()
	capital = user.sharing.capital
	comment_list = Comment.objects.order_by('-time')[:5]
	new_comment_list = []
	for i in range(len(comment_list)):
		new_comment_list.append(comment_list[len(comment_list) - 1 - i])
	price_list = range(101)
	
	# personal asset
	personal_asset = 0
	for my_item in Item.objects.filter(owner = user, sharing = True):
		personal_asset += my_item.value.current_value
	net_worth = personal_asset + capital
	
	# market value
	market_value = 0
	for market_item in Item.objects.filter(on_market = True, sharing = True):
		market_value += market_item.value.current_value

	context = {'to_sell_list': to_sell_list,
	           'on_sale_list': on_sale_list,
	           'to_buy_list': to_buy_list,
	           'reference_price_list': reference_price_list,
	           'user': user,
	           'capital': capital,
	           'comment_list': new_comment_list,
	           'price_list':price_list,
	           'personal_asset': personal_asset,
	           'market_value': market_value,
	           'net_worth': net_worth}
	return render(request, 'simulator/sharing_interface.html', context)

@csrf_protect
def sell(request):
	item_id = int(request.POST.get("id", -1))
	if item_id == -1:
		return HttpResponseRedirect(reverse('simulator:interface'))
	item = get_object_or_404(Item, pk = item_id)
	item.on_market = True
	item.time = timezone.now()
	item.selling_price = int(request.POST["selling_price"])
	item.save()
	return HttpResponseRedirect(reverse('simulator:interface'))

@csrf_protect
def sharing_sell(request):
	item_id = int(request.POST.get("id", -1))
	if item_id == -1:
		return HttpResponseRedirect(reverse('simulator:sharing_interface'))
	item = get_object_or_404(Item, pk = item_id)
	item.on_market = True
	item.time = timezone.now()
	item.save()
	return HttpResponseRedirect(reverse('simulator:sharing_interface'))

@csrf_protect
def comment(request):
	new_comment = Comment(time = timezone.now())
	new_comment.comment_text = request.POST["comment_text"]
	new_comment.author = request.user
	if new_comment.comment_text != '':
		new_comment.save()
	return HttpResponseRedirect(reverse('simulator:interface'))

@csrf_protect
def sharing_comment(request):
	new_comment = Comment(time = timezone.now())
	new_comment.comment_text = request.POST["comment_text"]
	new_comment.author = request.user
	if new_comment.comment_text != '':
		new_comment.save()
	return HttpResponseRedirect(reverse('simulator:sharing_interface'))

@csrf_protect
def buy(request):
	item_id = int(request.POST.get("item_id", -1))
	if item_id == -1:
		return HttpResponseRedirect(reverse('simulator:interface'))
	item = get_object_or_404(Item, pk = item_id)
	previous_owner = item.owner
	previous_owner.profile.capital += item.selling_price - 1
	previous_owner.profile.save()
	new_owner = request.user
	item.owner = new_owner
	new_owner.profile.capital -= item.selling_price + 1
	item.on_market = False
	item.time = timezone.now()
	item.save()
	new_owner.profile.save()
	return HttpResponseRedirect(reverse('simulator:interface'))

@csrf_protect
def combine(request):
	first_item_id = int(request.POST.get("first_item_id", -1))
	second_item_id = int(request.POST.get("second_item_id", -1))
	if first_item_id == second_item_id or first_item_id == -1 or \
	   second_item_id == -1:
		return HttpResponseRedirect(reverse('simulator:interface'))
	first_item = get_object_or_404(Item, pk = first_item_id)
	second_item = get_object_or_404(Item, pk = second_item_id)
	first_value = first_item.value.current_value
	second_value = second_item.value.current_value
	total_value = (first_value + second_value) * Decimal(1.3)
	profile = request.user.profile
	profile.capital += total_value
	profile.save()
	first_item.delete()
	second_item.delete()
	return HttpResponseRedirect(reverse('simulator:interface'))

@csrf_protect
def sharing_combine(request):
	first_item_id = int(request.POST.get("first_item_id", -1))
	second_item_id = int(request.POST.get("second_item_id", -1))
	if first_item_id == second_item_id or first_item_id == -1 or \
	   second_item_id == -1:
		return HttpResponseRedirect(reverse('simulator:sharing_interface'))
	first_item = get_object_or_404(Item, pk = first_item_id)
	second_item = get_object_or_404(Item, pk = second_item_id)
	first_value = first_item.value.current_value
	second_value = second_item.value.current_value
	total_value = (first_value + second_value) * Decimal(1.5)
	second_item.owner.sharing.capital += total_value / Decimal(2)
	second_item.owner.sharing.save()
	sharing = request.user.sharing
	sharing.capital += total_value / Decimal(2)
	sharing.save()
	first_item.delete()
	second_item.delete()
	return HttpResponseRedirect(reverse('simulator:sharing_interface'))

def googlecharts(request):
	username = Profile.objects.all()
	value = []
	for capital in Profile.objects.all():
		value.append(capital.capital)
	return render(request, 'simulator:googlecharts', {'username': username, 'value':value})
