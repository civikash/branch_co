from django.test import TestCase, Client
from django.urls import reverse
from account.models import User
from reports.models import InfEconOp, ManagerInfEconOp
from django.contrib.auth.models import User


class InfEconOpCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="secret"
        )

    def test_dispatch_GET(self):
        # Test GET request to InfEconOpCreateView should return status 200 and use correct template
        self.client.login(username = 'testuser', password = 'secret')
        response = self.client.get(reverse("inf_econ_op_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reports/reports/economica.html")
        self.client.logout()

    def test_dispatch_POST(self):
        # Test POST request to InfEconOpCreateView should create a new InfEconOp and ManagerInfEconOp object and redirect to reports:reports-vision
        self.client.login(username = 'testuser', password = 'secret')
        response = self.client.post(reverse("inf_econ_op_create"))
        self.assertEqual(response.status_code, 302)

        new_inf_econ_op = InfEconOp.objects.get(company__users__username="testuser")
        self.assertIsNotNone(new_inf_econ_op)

        new_manager_inf_econ_op = ManagerInfEconOp.objects.get(reports__pk=new_inf_econ_op.pk)
        self.assertIsNotNone(new_manager_inf_econ_op)

        self.assertRedirects(response, reverse('reports:reports-vision', args=[new_manager_inf_econ_op.uid]))

        self.client.logout()
