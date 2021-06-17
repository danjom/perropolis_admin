from django.utils.translation import ugettext_lazy as _


# Message Types
VERIFICATION_CODE = 1
REMINDER = 2
NOTIFICATION = 3
MARKETING = 4

MESSAGE_TYPES = (
    (VERIFICATION_CODE, _("Verification Code")),
    (REMINDER, _("Reminder")),
    (NOTIFICATION, _("Notification")),
    (MARKETING, _("Marketing")),
)

####################################################

# Brand Types
FOOD_AND_SNACKS = 1
DRUGS = 2
ACCESSORIES = 3

BRAND_TYPES = (
    (FOOD_AND_SNACKS, _("Food/Snacks")),
    (DRUGS, _("Drugs")),
    (ACCESSORIES, _("Accesories/Toys")),
)

####################################################

# Animal sizes
TEA_CUP = 1
SMALL = 2
MEDIUM = 3
LARGE = 4
GIANT = 5

ANIMAL_SIZES = (
    (TEA_CUP, _("Tea cup")),
    (SMALL, _("Small")),
    (MEDIUM, _("Medium")),
    (LARGE, _("Large")),
    (GIANT, _("GIANT"))
)

# Drug Types
PILLS = 1
INYECTION = 2
SYRUP = 3
SUPPOSITORY = 4

DRUG_TYPES = (
    (PILLS, _('Pills')),
    (INYECTION, _('Inyection')),
    (SYRUP, _('Syrup')),
    (SUPPOSITORY, _('Suppository')),
)
