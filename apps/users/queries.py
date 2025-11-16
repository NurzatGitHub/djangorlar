from django.db.models import Q, Count, Avg, Max, Min, Sum, Case, When, Value, IntegerField, BooleanField, F, ExpressionWrapper
from django.db.models.functions import ExtractYear, Now
from apps.users.models import CustomUser
from datetime import datetime, timedelta

from django.db import models

def orm_queries():
    # 2.1
    q21 = CustomUser.objects.filter(is_active=True)

    # 2.2
    q22 = CustomUser.objects.filter(email__endswith="@gmail.com")

    # 2.3
    q23 = CustomUser.objects.filter(city="Almaty")

    # 2.4
    q24 = CustomUser.objects.exclude(city="Almaty")

    # 2.5
    q25 = CustomUser.objects.filter(salary__gt=500000)

    # 2.6
    q26 = CustomUser.objects.filter(department="IT", country="Kazakhstan")

    # 2.7
    q27 = CustomUser.objects.filter(birth_date__isnull=True)

    # 2.8
    q28 = CustomUser.objects.filter(first_name__istartswith="A")

    # 2.9
    q29 = CustomUser.objects.count()

    # 2.10
    q210 = CustomUser.objects.order_by("-date_joined")[:20]

    # 2.11
    q211 = CustomUser.objects.values_list("city", flat=True).distinct()

    # 2.12
    q212 = CustomUser.objects.filter(department="Sales").count()

    # 2.13
    week_ago = datetime.now() - timedelta(days=7)
    q213 = CustomUser.objects.filter(last_login__gte=week_ago)

    # 2.14
    q214 = CustomUser.objects.filter(Q(first_name__icontains="bek") | Q(last_name__icontains="bek"))

    # 2.15
    q215 = CustomUser.objects.filter(salary__gte=300000, salary__lte=700000)

    # 2.16
    q216 = CustomUser.objects.filter(department__in=["IT", "HR", "Finance"])

    # 2.17
    q217 = CustomUser.objects.values("department").annotate(count=Count("id"))

    # 2.18
    q218 = q217.order_by("-count")

    # 2.19
    q219 = CustomUser.objects.values("city").annotate(count=Count("id")).order_by("-count")[:5]

    # 2.20
    q220 = CustomUser.objects.filter(last_login__isnull=True)

    # 2.21
    q221 = CustomUser.objects.aggregate(avg_salary=Avg("salary"))

    # 2.22
    q222 = CustomUser.objects.aggregate(max_salary=Max("salary"), min_salary=Min("salary"))

    # 2.23
    q223 = CustomUser.objects.filter(phone__contains="+7")

    # 2.24
    q224 = CustomUser.objects.annotate(full_name=F("first_name") + Value(" ") + F("last_name"))

    # 2.25
    q225 = CustomUser.objects.annotate(
        birth_year=ExtractYear("birth_date")
    ).order_by("birth_year")

    # 2.26
    q226 = CustomUser.objects.filter(birth_date__month=5)

    # 2.27
    q227 = CustomUser.objects.filter(role="manager", salary__gt=400000)

    # 2.28
    q228 = CustomUser.objects.filter(Q(role="employee") | Q(department="HR"))

    # 2.29
    q229 = CustomUser.objects.filter(is_active=True).values("city").annotate(count=Count("id"))

    # 2.30
    q230 = CustomUser.objects.order_by("date_joined")[:10]

    # 2.31
    q231 = CustomUser.objects.filter(city__startswith="A", salary__gt=300000)

    # 2.32
    q232 = CustomUser.objects.filter(Q(department__isnull=True) | Q(department=""))

    # 2.33
    q233 = CustomUser.objects.values("country").annotate(
        count=Count("id"),
        avg_salary=Avg("salary")
    )

    # 2.34
    q234 = CustomUser.objects.filter(is_staff=True).order_by("-last_login")

    # 2.35
    q235 = CustomUser.objects.exclude(email__contains="example.com")

    # 2.36 (salary > average)
    avg_salary = CustomUser.objects.aggregate(a=Avg("salary"))["a"]
    q236 = CustomUser.objects.filter(salary__gt=avg_salary)

    # 2.37
    q237 = CustomUser.objects.values("email").annotate(c=Count("id")).filter(c__gt=1)

    # 2.38
    q238 = CustomUser.objects.annotate(
        salary_level=Case(
            When(salary__lt=300000, then=Value("low")),
            When(salary__lte=700000, then=Value("medium")),
            When(salary__gt=700000, then=Value("high")),
            output_field=models.CharField(),
        )
    ).order_by("salary_level")

    # 2.39
    current_year = datetime.now().year
    q239 = CustomUser.objects.filter(date_joined__year=current_year)

    # 2.40
    q240 = CustomUser.objects.values("department").annotate(total_salary=Sum("salary"))

    # 2.41
    q241 = CustomUser.objects.filter(department="IT", last_login__isnull=True)

    # 2.42
    q242 = CustomUser.objects.filter(country="Kazakhstan").filter(Q(city__isnull=True) | Q(city=""))

    # 2.43
    q243 = CustomUser.objects.filter(birth_date__lt="1990-01-01", salary__isnull=False)

    # 2.44
    q244 = CustomUser.objects.annotate(
        years_since_joined=ExpressionWrapper(
            Now() - F("date_joined"),
            output_field=IntegerField()
        )
    )

    # 2.45
    q245 = CustomUser.objects.filter(
        department="Sales",
        email__endswith="@gmail.com",
        salary__gt=350000
    )

    # 2.46
    q246 = CustomUser.objects.order_by("country", "-salary")

    # 2.47
    q247 = CustomUser.objects.values("role").annotate(count=Count("id")).filter(count__gt=100)

    # 2.48
    q248 = CustomUser.objects.filter(last_login__lt=F("date_joined"))

    # 2.49
    q249 = CustomUser.objects.annotate(
        is_senior=Case(
            When(birth_date__lt="1985-01-01", then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    )

    # 2.50
    q250 = CustomUser.objects.values("department").annotate(
        avg_salary=Avg("salary"),
        count=Count("id")
    ).filter(count__gte=20).order_by("-avg_salary")

    return "All queries loaded"
