from django.forms import modelformset_factory

from feedback.models import OutputAlternativo


OutputAlternativoModelFormSet = modelformset_factory(
    OutputAlternativo,
    fields=('sugerencia',), extra=0
)
