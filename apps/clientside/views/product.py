from azbankgateways import bankfactories
from azbankgateways.models import PaymentStatus, Bank
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic import TemplateView

from apps.account.models import Address
from apps.order.models import Payment, Transaction
from apps.product.models import Product


class ProductListView(ListView):
    template_name = 'front/pages/products.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    template_name = 'front/pages/single-product.html'
    slug_field = 'slug'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return Product.objects.filter(slug=self.kwargs['slug']).first()


class ProductPaymentForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea(), required=False)
    postal_code = forms.CharField(required=False)

    class Meta:
        model = Address
        exclude = ('user',)


class ProductPaymentView(ProductDetailView, CreateView):
    template_name = 'front/pages/checkout.html'
    form_class = ProductPaymentForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.path)

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        from apps.clientside.urls import calc_post_price

        obj: Address = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        product = Product.objects.get(slug=self.kwargs['slug'])
        payment = Payment.objects.create(
            user=obj.user,
            address=obj,
            note=form.cleaned_data['note'],
            object_id=product.id,
            content_type=ContentType.objects.get_for_model(Product),
        )

        amount = payment.calculate_price()
        post_price = calc_post_price(product.weight, obj.state, obj.city)
        if post_price:
            amount += post_price
        else:
            return redirect(self.request.META['HTTP_REFERER'])

        if amount <= 0:
            return render(self.request, "front/pages/payment_success.html")
        amount = amount * 10
        factory = bankfactories.BankFactory()
        bank = factory.auto_create()
        bank.set_request(self.request)
        bank.set_amount(amount)
        bank.set_client_callback_url(reverse('callback-gateway'))
        bank.set_mobile_number(self.request.user.phone_number)
        bank_obj = bank.ready()

        # assign bank to payment model
        payment.bank = bank_obj
        payment.save()
        return bank.redirect_gateway()

    def form_invalid(self, form):
        print(form.errors)
        return super().get(self.request)


class PaymentCallbackView(TemplateView):
    template_name = 'front/pages/payment_success.html'

    def get(self, request, *args, **kwargs):
        if tracking_code := request.GET.get('tc'):
            transaction = get_object_or_404(Bank, tracking_code=tracking_code)

            if transaction.status == PaymentStatus.COMPLETE:
                return self.success_payment(transaction.payment)

            else:
                return self.failed_payment(transaction)

        else:
            return render(self.request, "front/pages/payment_failed.html", {
                "message": "لینک معتبر نیست",
            })

    def success_payment(self, payment: Payment):
        # add student to course
        payment.course.students.add(payment.user)

        # set payment status to paid
        payment.set_paid()

        return render(self.request, "front/pages/payment_success.html", {
            "phone": payment.user.phone_number,
        })

    def failed_payment(self, transaction: Transaction):
        if discount := transaction.payment.discount_code:
            # decrease discount used count bcz of failed payment
            discount.decrease_used_count()

        if transaction.status == PaymentStatus.CANCEL_BY_USER:
            message = "پرداخت توسط شما کنسل شد."
        elif transaction.status == PaymentStatus.EXPIRE_VERIFY_PAYMENT:
            message = "پرداخت به دلیل انقضا مدت زمان کنسل شد."
        elif transaction.status == PaymentStatus.EXPIRE_GATEWAY_TOKEN:
            message = "توکن پرداخت نامعتبر می باشد."
        else:
            message = ""

        return render(self.request, "front/pages/payment_failed.html", {
            "message": message,
            "status": transaction.status,
        })
