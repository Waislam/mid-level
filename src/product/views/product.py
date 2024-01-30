from django.views import generic
from django.views.generic.list import ListView
from product.models import Product, Variant, ProductVariantPrice
from datetime import date
from django.db.models import Q



class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()

        title_query = self.request.GET.get('title')
        vari_title = self.request.GET.get('variant')
        created_at = self.request.GET.get('date')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')

        filter_conditions = {}

        if title_query:
            filter_conditions['title__icontains'] = title_query

        if created_at:
            filter_conditions['created_at__date'] = date(*map(int, created_at.split('-')))

        if price_from and price_to:
            filter_conditions['product_variant_prices__price__range'] = (price_from, price_to)

        if vari_title is not None:
            filter_conditions['product_variants__variant_title'] = vari_title

        if filter_conditions:
            return queryset.filter(**filter_conditions)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['variant_prices'] = ProductVariantPrice.objects.select_related('product')
        context['variants'] = Variant.objects.prefetch_related('product_productvariants')

        for var in context['variants']:
            var.variant_title_list = list(set(var.product_productvariants.values_list('variant_title', flat=True)))

        return context
