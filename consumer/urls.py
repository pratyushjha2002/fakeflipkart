from django.urls import path
from . import views


urlpatterns = [
    
    path('main/',views.main,name='main'),
    path('',views.main,name='main'), #extra
    path('index/',views.index,name='index'), #no - use
    path('add_seller_record/', views.add_seller_record,name="add_seller_record"),
    path('form/', views.form,name="seller_form"),
    path('search/', views.search,name="studentdata"),
    path('item_detailed/', views.item_detailed),
    path('c_login_form/', views.c_login_form,name="c_loginform"),
    path('s_login_form/', views.s_login_form),
    path('c_signup_form/', views.c_signup_form),
    path('s_signup_form/', views.s_signup_form),
    path('c_signup/', views.c_signup),
    path('s_signup/', views.s_signup),
    path('c_login/', views.c_login),
    path('c_logout/',views.c_logout),
    path('comment/',views.add_comment),
    path('buy_form/',views.buy_form),
    path('buy/',views.buy),
    path('cart/',views.add_cart),
    path('showcart/',views.showcart),
    path('remove_cart/',views.remove_cart),
    path('category_data/',views.category_data),
    path('thankyou_c/',views.thankyou_c),
    path('thankyou_s/',views.thankyou_s),
    path('forgot_password_form/',views.forgot_password_form),
    path('forgot_password/',views.forgot_password),
    path('password_reset/',views.password_reset),
    path('new_password/',views.new_password),
    path('set_new_password/',views.set_new_password),
    path('update_new_password/',views.update_new_password),
    path('search_result/',views.search_result),
]
#show username at top left to manage id, 