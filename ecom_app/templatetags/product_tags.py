from django import template
import math
register = template.Library()

@register.simple_tag
def calc_sell_price(Price,Discount):
    if Discount is None or Discount is 0:
        return Price
    sellprice = Price

    sellprice = Price - (Price*Discount/100)
    return math.floor(sellprice)

@register.simple_tag
def progress_bar(Total_qty,Availablity):
    progress_bar = Availablity
    progress_bar = Availablity * (100/Total_qty)
    return math.floor(progress_bar)