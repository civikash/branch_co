from django.urls import path
from account.views import signout, login, logout, company, users

app_name = 'account'

urlpatterns = [
    path('login/', login.LoginView.as_view(), name='login'),
    path('logout/', logout.LogoutView.as_view(), name='logout'),
    path('users/', users.UsersView.as_view(), name='users'),
    path('users/create/', users.AddUserView.as_view(), name='users-create'),
    path('signup/', signout.RegisterView.as_view(), name='signup'),
    path('company-data/', company.CompanyDataView.as_view(), name='company-data')
]
