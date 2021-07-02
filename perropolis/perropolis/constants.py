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
    (GIANT, _("Giant"))
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


# Week Days
MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
SUNDAY = 7

WEEK_DAYS = (
    (MONDAY, _('Monday')),
    (TUESDAY, _('Tuesday')),
    (WEDNESDAY, _('Wednesday')),
    (THURSDAY, _('Thursday')),
    (FRIDAY, _('Friday')),
    (SATURDAY, _('Saturday')),
    (SUNDAY, _('Sunday')),
)


# Room Type

REGULAR_SIZE = 1
LARGE_SIZE = 2

ROOM_TYPES = (
    (REGULAR_SIZE, _('Regular Size')),
    (LARGE_SIZE, _('Large Size')),
)


# SERVING_TYPES

SERVING_TYPE_FOOD = 1
SERVING_TYPE_MEDICATION = 2

SERVING_TYPES = (
    (SERVING_TYPE_FOOD, _('Food')),
    (SERVING_TYPE_MEDICATION, _('Medication'))
)


# Genders

FEMALE = 1
MALE = 2

GENDERS = (
    (FEMALE, _('Female')),
    (MALE, _('Male')),
)
