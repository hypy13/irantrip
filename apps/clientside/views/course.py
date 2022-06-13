from azbankgateways import bankfactories
from azbankgateways.models import PaymentStatus, Bank
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic import TemplateView

from apps.account.models import Address
from apps.course.models import Course
from apps.order.models import Payment


class CourseListView(ListView):
    template_name = 'front/pages/course-list.html'
    context_object_name = 'courses'
    paginate_by = 6

    def get_queryset(self):
        return Course.objects.filter(status=True).all()


class CourseDetailView(DetailView):
    template_name = 'front/pages/single-course.html'
    slug_field = 'slug'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        return Course.objects.filter(slug=self.kwargs['slug']).first()


class CoursePaymentForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea(), required=False)
    postal_code = forms.CharField(required=False)

    class Meta:
        model = Address
        exclude = ('user',)


class CoursePaymentView(CourseDetailView, CreateView):
    template_name = 'front/pages/checkout.html'
    form_class = CoursePaymentForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.path)

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        product = Course.objects.get(slug=self.kwargs['slug'])
        payment = Payment.objects.create(
            user=obj.user,
            address=obj,
            note=form.cleaned_data['note'],
            object_id=product.id,
            content_type=ContentType.objects.get_for_model(Course)
        )
        amount = payment.calculate_price()
        if amount <= 0:
            return render(self.request, "front/pages/payment_success.html")

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
            "message": "success",
        })

    def failed_payment(self, transaction):
        if discount := transaction.payment.discount_code:
            # decrease discount used count bcz of failed payment
            discount.decrease_used_count()

        return render(self.request, "front/pages/payment_failed.html", {
            "message": transaction.status,
        })
