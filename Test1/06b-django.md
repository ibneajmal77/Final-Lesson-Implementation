# 06b — DJANGO, FROM ZERO

> **Read `06-python.md` first.** This file assumes classes, decorators and inheritance.
>
> Same format: **What** → **Code** → **Why** → **Say** → **Hook** → ⚠️ **Trap**
>
> **Your angle:** Django is **ASP.NET MVC + Entity Framework + Identity + a free admin site**,
> all in one box. Say that early.

**30 minutes?** Part 0 → Part 4 → Part 12.

---

# 📑 MAP

| Part | Topic |
|---|---|
| 0 | The 12 answers that win |
| 1 | What Django is |
| 2 | The request lifecycle |
| 3 | Project layout and apps |
| 4 | **Models and the ORM** ⭐ |
| 5 | Migrations |
| 6 | Views |
| 7 | URLs |
| 8 | Templates |
| 9 | Forms |
| 10 | Admin |
| 11 | Auth and permissions |
| 12 | **Django REST Framework** ⭐ |
| 13 | Middleware |
| 14 | Settings and deployment |
| 15 | Caching and Celery |
| 16 | Async Django |
| 17 | Security |
| 18 | **Performance — the N+1 answer** ⭐ |
| 19 | Testing |
| 20 | Django vs FastAPI vs ASP.NET |
| 21 | 80 rapid-fire questions |

---

# EASY MEMORY NOTES

Read this first. Start with the short phrase. Say the simple line. Add the last column only if they
ask for more.

| Remember | Say it simply | If they ask more |
|---|---|---|
| **Full web box** | Django gives most web features out of the box. | ORM, admin, login, forms, templates, security. |
| **MVT = MVC names** | Django View is like a controller. | Template is the HTML view. |
| **Model saves itself** | A Django model knows how to save and query itself. | That is Active Record, unlike EF Core's `DbContext`. |
| **Query later** | A QuerySet does not hit the database until used. | You can chain filters and still get one query. |
| **N+1 loop** | Do not load related data one row at a time. | Use `select_related` or `prefetch_related`. |
| **Migrations are files** | Schema changes become code files. | Review them before running them in production. |
| **Admin is quick back office** | Django admin gives CRUD screens fast. | Useful for internal tools and support teams. |
| **Middleware wraps request** | Request goes through middleware in order, then response comes back. | Order matters, especially session before auth. |
| **Async is limited** | Django has async support, but much is still sync. | Use FastAPI for heavily async services. |

---

# PART 0 — THE 12 ANSWERS THAT WIN

| # | Question | Say this |
|---|---|---|
| 1 | **What is Django?** | "Django is a Python web framework with ORM, admin, login, forms, templates, and security built in." |
| 2 | **MVC or MVT?** | "Django says MVT. Its View is like a controller, and Template is the HTML view." |
| 3 | **The ORM in one line?** | "The model maps to a table and knows how to query and save itself." |
| 4 | **The N+1 problem?** | "A loop can run one query per row. Fix it with `select_related` or `prefetch_related`." |
| 5 | **Are QuerySets lazy?** | "Yes. A QuerySet does not hit the database until you use it." |
| 6 | **Migrations?** | "Migrations are code files for database changes. `makemigrations` creates them; `migrate` runs them." |
| 7 | **The admin?** | "Django admin gives quick CRUD screens from your models." |
| 8 | **What is DRF?** | "Django REST Framework helps build APIs with serializers, views, auth, and permissions." |
| 9 | **Fat models?** | "Keep HTTP work in views. Put business rules in models or services." |
| 10 | **Is Django async?** | "Partly. It supports async, but much of the ecosystem is still sync." |
| 11 | **Security out of the box?** | "Django gives CSRF protection, safe ORM queries, template escaping, and password hashing." |
| 12 | **When would you not use it?** | "For a small async API or WebSocket-heavy service, I would usually pick FastAPI." |

---

# PART 1 — WHAT DJANGO IS

## 1.1 Batteries included — what's in the box

| You get | ASP.NET equivalent |
|---|---|
| ORM | Entity Framework Core |
| Migrations | EF Migrations |
| **Admin site** | *nothing — you'd build it* ⭐ |
| Auth, users, groups, permissions | ASP.NET Identity |
| Forms and validation | model binding + DataAnnotations |
| Template engine | Razor |
| Routing | attribute routing |
| Middleware | middleware |
| Sessions, CSRF, security headers | built in |
| Management commands | dotnet CLI tools |
| Caching framework | `IMemoryCache` / Redis |
| i18n, timezones, email | built in |

**Say:** *"Django's proposition is that everything a web product needs is already there and already integrated. You trade flexibility for months of time. FastAPI is the opposite trade."*

**Hook:** **Django = a whole product. FastAPI = one service.**

---

## 1.2 MVT

```
Request → URL router → View → Model (ORM → DB)
                        ↓
                     Template → HTML → Response
```

| Django name | Actually is |
|---|---|
| **Model** | the data + the business rules |
| **View** | the **controller** — a function or class handling a request |
| **Template** | the **view** — the HTML |

⚠️ **Trap: "Is Django MVC?"** → *"Functionally yes. Django calls it MVT because what it names 'view' is what MVC calls the controller, and the template is the view. The framework itself plays the controller role."*

---

# PART 2 — THE REQUEST LIFECYCLE

**Know this order. It's a common whiteboard question.**

```
1. Browser sends HTTP
2. WSGI/ASGI server (Gunicorn / Uvicorn) hands it to Django
3. Middleware — request phase, top to bottom
4. URL resolver matches urls.py → picks a view
5. View runs: queries the ORM, applies business rules
6. Template renders (or DRF serializes)
7. Middleware — response phase, bottom to top ⚠️ reverse order
8. Response returned
```

**Say:** *"Middleware wraps the view like an onion — request phase downward, response phase back up in reverse. Ordering in `MIDDLEWARE` matters, which is why `AuthenticationMiddleware` must come after `SessionMiddleware`: authentication reads the session."*

**Hook:** **Down the list on the way in, up on the way out.**

---

# PART 3 — LAYOUT AND APPS

```bash
django-admin startproject config .
python manage.py startapp orders
```

```
config/
  settings.py      # ⭐ everything is configured here
  urls.py          # root URL routing
  wsgi.py / asgi.py
orders/            # an "app" = a reusable feature module
  models.py
  views.py
  urls.py
  admin.py
  serializers.py   # if using DRF
  services.py      # ⭐ your business logic. Not a Django convention — do it anyway
  tests.py
  migrations/
manage.py
```

**Say:** *"A project is the deployment unit; an app is a feature module and it's meant to be reusable. I add a `services.py` per app for business logic, because views drift into fat controllers otherwise and models become god objects."*

**Hook:** **Project = deployment. App = feature.**

**`manage.py` commands worth naming:**
```bash
python manage.py runserver          # dev only
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell_plus         # django-extensions. Models pre-imported
python manage.py test
python manage.py collectstatic      # for production
python manage.py check --deploy     # ⭐ production security checklist
```

---

# PART 4 — MODELS AND THE ORM ⭐⭐

**This is where the interview goes deep. Most of Django is the ORM.**

## 4.1 A model

```python
from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    class Side(models.TextChoices):
        BUY = "BUY", "Buy"
        SELL = "SELL", "Sell"

    account  = models.ForeignKey(Account, on_delete=models.CASCADE,
                                 related_name="orders")
    symbol   = models.CharField(max_length=10, db_index=True)
    side     = models.CharField(max_length=4, choices=Side.choices)
    qty      = models.PositiveIntegerField()
    price    = models.DecimalField(max_digits=18, decimal_places=4)   # ⭐ money
    filled   = models.BooleanField(default=False)
    created  = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["symbol", "created"])]
        constraints = [
            models.CheckConstraint(check=models.Q(qty__gt=0), name="qty_positive"),
            models.UniqueConstraint(fields=["account", "symbol", "created"],
                                    name="uniq_order"),
        ]

    def __str__(self):
        return f"{self.side} {self.qty} {self.symbol}"

    @property
    def notional(self):
        return self.qty * self.price
```

**Points to make:**
- Django adds an auto `id` primary key unless you declare one.
- `DecimalField` for money. **Never `FloatField`.**
- `related_name="orders"` gives `account.orders.all()` for the reverse lookup.
- `Meta.constraints` puts the rule in the **database**, so it holds even for a bulk import.

**Say:** *"I push invariants into database constraints, not just model validation. `full_clean` isn't called by `save()`, so model-level validation is easy to bypass — a check constraint isn't."*

**Hook:** **Validation can be skipped. Constraints can't.**

---

## 4.2 `on_delete` — they will ask

| Value | Effect |
|---|---|
| `CASCADE` | delete the children too |
| `PROTECT` | ⭐ refuse the delete. Safest for financial records |
| `RESTRICT` | like PROTECT, but allows it if another cascade covers it |
| `SET_NULL` | null the FK (needs `null=True`) |
| `SET_DEFAULT` | use the default |
| `DO_NOTHING` | leave it to the database |

**Say:** *"There's no default — you must choose, which is deliberate. In a financial system I default to `PROTECT`, because silently cascading away trade history is unrecoverable."*

---

## 4.3 Field types

| Field | Notes |
|---|---|
| `CharField(max_length=)` | max_length required |
| `TextField` | unbounded |
| `IntegerField` / `BigIntegerField` / `PositiveIntegerField` | |
| `DecimalField(max_digits, decimal_places)` | ⭐ money |
| `FloatField` | ⚠️ never for money |
| `BooleanField` | |
| `DateField` / `DateTimeField` | `auto_now_add` = on create, `auto_now` = on every save |
| `ForeignKey` | many-to-one |
| `ManyToManyField` | creates a join table |
| `OneToOneField` | |
| `JSONField` | native JSON on Postgres |
| `UUIDField` | |
| `FileField` / `ImageField` | |
| `EmailField` / `URLField` / `SlugField` | CharField + validator |

`null=True` = the **database** column allows NULL.
`blank=True` = **forms** allow empty.
⚠️ Never use `null=True` on a `CharField` — you'd get two kinds of empty. Use `blank=True` only.

---

## 4.4 QuerySets — lazy, chainable

```python
Order.objects.all()
Order.objects.filter(symbol="VOD", qty__gt=100)
Order.objects.exclude(filled=True)
Order.objects.get(pk=1)              # ⚠️ raises DoesNotExist or MultipleObjectsReturned
Order.objects.first() / .last()
Order.objects.order_by("-created")
Order.objects.values("symbol", "qty")        # dicts
Order.objects.values_list("symbol", flat=True)   # a flat list
Order.objects.distinct()
Order.objects.count() / .exists()
Order.objects.create(...)
Order.objects.bulk_create(objs, batch_size=1000)    # ⭐ one query
Order.objects.filter(...).update(filled=True)       # ⭐ one query, no signals
Order.objects.filter(...).delete()
Order.objects.get_or_create(symbol="VOD", defaults={...})
Order.objects.update_or_create(...)
```

**Field lookups:**
```python
__exact __iexact __contains __icontains __startswith __endswith
__gt __gte __lt __lte __range
__in __isnull
__date __year __month __day __week_day __hour
__regex
account__name__icontains="hsbc"        # ⭐ traverse relations with __
```

**Q objects — OR, AND, NOT:**
```python
from django.db.models import Q
Order.objects.filter(Q(symbol="VOD") | Q(symbol="BP"))
Order.objects.filter(~Q(filled=True))
```

**F objects — reference a column, avoid a race:**
```python
from django.db.models import F
Order.objects.filter(pk=1).update(qty=F("qty") + 1)     # ⭐ atomic in SQL
Order.objects.filter(qty__gt=F("filled_qty"))            # column vs column
```

**Say:** *"`F` makes the update happen in SQL rather than read-modify-write in Python, so two concurrent requests can't lose an increment. It's the same reason you'd write `UPDATE t SET qty = qty + 1` by hand."*

**Hook:** **`F` = do the maths in the database.**

**Aggregation and annotation:**
```python
from django.db.models import Sum, Count, Avg, Max, Min

Order.objects.aggregate(total=Sum("qty"))                    # one dict
Order.objects.values("symbol").annotate(total=Sum("qty"))    # ⭐ GROUP BY
Account.objects.annotate(n=Count("orders")).filter(n__gt=5)
```

**Say:** *"`aggregate` collapses the whole queryset to one row. `annotate` adds a computed column per group — that's `GROUP BY`. `values().annotate()` is the pattern."*

---

## 4.5 Laziness — say this properly

```python
qs = Order.objects.filter(symbol="VOD")     # NO query yet
qs = qs.exclude(filled=True)                # still no query
qs = qs.order_by("-created")[:10]           # still no query — slicing adds LIMIT
for o in qs:                                # ⭐ NOW one query runs
    ...
```

**Evaluation triggers:** iteration, slicing with a step, `len()`, `list()`, `bool()`,
`count()`, `exists()`, `repr()`.

⚠️ **QuerySets cache after evaluation**, but re-filtering makes a **new** queryset and a new
query. So `if qs.exists(): for o in qs:` is two queries. Use `qs = list(qs)` once instead.

**Say:** *"QuerySets are lazy and chainable, so filters compose into a single SQL statement. The trap is that a re-filter creates a new queryset — calling `count()` then iterating hits the database twice."*

**Hook:** **Lazy until you touch it. Re-filter = new query.**

---

## 4.6 Transactions

```python
from django.db import transaction

@transaction.atomic
def place_order(...): ...

with transaction.atomic():
    account.save()
    order.save()

with transaction.atomic():
    acct = Account.objects.select_for_update().get(pk=1)     # ⭐ row lock
    acct.balance -= amount
    acct.save()

transaction.on_commit(lambda: send_email.delay(order.id))    # ⭐ fire AFTER commit
```

**Say:** *"`atomic` gives a transaction or a savepoint if nested. `select_for_update` takes a row lock for read-modify-write — that's `SELECT ... FOR UPDATE`. And `on_commit` is important: if I queue a Celery job inside the transaction, the worker can pick it up before the commit lands and not find the row."*

**Hook:** **Queue jobs in `on_commit`, never inside the transaction.**

⚠️ Default is **autocommit**: every `save()` is its own transaction unless you wrap it.

---

## 4.7 Raw SQL — when the ORM isn't enough

```python
Order.objects.raw("SELECT * FROM orders WHERE symbol = %s", [symbol])   # ⭐ params

from django.db import connection
with connection.cursor() as c:
    c.execute("SELECT ... WHERE id = %s", [id])       # never f-string SQL
```

**Say:** *"For window functions, recursive CTEs or heavy reporting I'd drop to raw SQL rather than fight the ORM. Always parameterised — string interpolation into SQL is the injection hole."*

---

# PART 5 — MIGRATIONS

```bash
python manage.py makemigrations orders
python manage.py migrate
python manage.py sqlmigrate orders 0002       # ⭐ show the SQL before running it
python manage.py migrate orders 0001          # roll back to a migration
python manage.py makemigrations --empty       # for a data migration
```

**Data migration:**
```python
def forwards(apps, schema_editor):
    Order = apps.get_model("orders", "Order")     # ⭐ historical model, not the import
    Order.objects.filter(side="").update(side="BUY")

class Migration(migrations.Migration):
    dependencies = [("orders", "0001_initial")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
```

⚠️ **Always use `apps.get_model`,** never the direct import. The imported model is today's
version; the migration must run against the model as it was.

**The production answer — say all of it:**
> *"Migrations are versioned Python files, so they're reviewed in the pull request like code. In production I run `migrate` as a separate job before the rollout, never at app startup — otherwise every worker races to migrate the same database. For a large table I make it a two-step deploy: add the nullable column and backfill in batches, deploy the code that writes both, then make it non-null and drop the old column. And I check `sqlmigrate` first, because Django will happily generate a migration that locks a hot table."*

**Hook:** **Expand, migrate, contract. Never at startup.**

---

# PART 6 — VIEWS

## 6.1 Function-based

```python
from django.shortcuts import render, get_object_or_404

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "orders/detail.html", {"order": order})
```

## 6.2 Class-based

```python
from django.views.generic import ListView, DetailView, CreateView

class OrderList(ListView):
    model = Order
    paginate_by = 50
    def get_queryset(self):
        return Order.objects.select_related("account").filter(
            account__owner=self.request.user)
```

| Generic view | Does |
|---|---|
| `ListView` | list + pagination |
| `DetailView` | one object |
| `CreateView` / `UpdateView` / `DeleteView` | form CRUD |
| `TemplateView` | static template |
| `RedirectView` | redirect |

**Say:** *"Function views for anything with unusual logic — they're explicit and easy to read. Class-based generics for standard CRUD, because they remove real boilerplate. The cost of CBVs is that the mixin chain makes control flow hard to follow, so I don't use them for complex flows."*

**Hook:** **CBV for CRUD. FBV for logic.**

---

# PART 7 — URLS

```python
# config/urls.py
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("orders.urls")),
]

# orders/urls.py
urlpatterns = [
    path("orders/", views.OrderList.as_view(), name="order-list"),
    path("orders/<int:pk>/", views.OrderDetail.as_view(), name="order-detail"),
    path("orders/<slug:symbol>/", views.by_symbol),
    re_path(r"^legacy/(?P<id>\d+)/$", views.legacy),
]
```

Converters: `int`, `str`, `slug`, `uuid`, `path`.

**Named URLs — never hardcode a path:**
```python
reverse("order-detail", kwargs={"pk": 1})       # in Python
{% url 'order-detail' order.pk %}               # in a template
```

**Say:** *"Named URLs mean the path exists in one place. Change the route and every link and redirect follows — you never grep for hardcoded strings."*

---

# PART 8 — TEMPLATES

```django
{% extends "base.html" %}
{% block content %}
  {% for order in orders %}
    <p>{{ order.symbol }} — {{ order.price|floatformat:2 }}</p>
  {% empty %}
    <p>No orders</p>
  {% endfor %}
  {% if user.is_authenticated %}...{% endif %}
  {% url 'order-detail' order.pk %}
  {% csrf_token %}
{% endblock %}
```

**Key facts:**
- **Auto-escaping is on.** `{{ x }}` is XSS-safe. `{{ x|safe }}` turns it off — that's the risk.
- Deliberately limited: no arbitrary Python. Logic belongs in the view.
- `{% extends %}` + `{% block %}` = Razor layouts and sections.

**Say:** *"Templates auto-escape by default, which kills most XSS. The language is intentionally weak so business logic can't leak into the presentation layer."*

---

# PART 9 — FORMS

```python
from django import forms

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["symbol", "side", "qty", "price"]

    def clean_qty(self):                      # one field
        qty = self.cleaned_data["qty"]
        if qty > 1_000_000:
            raise forms.ValidationError("Too large")
        return qty

    def clean(self):                          # across fields
        data = super().clean()
        ...
        return data
```

```python
form = OrderForm(request.POST)
if form.is_valid():
    order = form.save()
```

**Say:** *"A `ModelForm` derives fields, validation and saving from the model, so the rules live in one place. `clean_<field>` validates one field, `clean` validates across fields. It's model binding plus validation plus HTML rendering in one object."*

---

# PART 10 — THE ADMIN ⭐

```python
from django.contrib import admin

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ("symbol", "side", "qty", "price", "created")
    list_filter   = ("side", "filled", "created")
    search_fields = ("symbol", "account__name")
    date_hierarchy = "created"
    readonly_fields = ("created", "updated")
    list_select_related = ("account",)         # ⭐ avoids N+1 in the list
    actions = ["mark_filled"]

    @admin.action(description="Mark as filled")
    def mark_filled(self, request, queryset):
        queryset.update(filled=True)
```

**Say:** *"The admin is a fully permissioned CRUD back office generated from the models. For internal tooling — ops, support, reference data — it's weeks of work for a few lines. It's the single biggest reason teams pick Django."*

⚠️ **Say the limits too, it shows judgement:** *"It's for trusted internal staff, not a customer-facing UI. It's not a substitute for a real workflow tool, and it's easy to expose too much — so I restrict by permission, lock down `readonly_fields`, and never put it on a public URL without extra protection."*

---

# PART 11 — AUTH AND PERMISSIONS

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

@login_required
def dashboard(request): ...

@permission_required("orders.add_order")
def create(request): ...

class OrderList(LoginRequiredMixin, ListView): ...
```

**What ships:** `User` model, groups, per-model add/change/delete/view permissions, password
hashing (PBKDF2 by default, argon2 available), password reset flow, session management.

**Custom user — say this:**
> *"I always start a project with a custom user model, even if it's empty — `AUTH_USER_MODEL` pointing at my own class inheriting `AbstractUser`. Swapping it later is genuinely painful, so it's the cheapest insurance in the framework."*

**Hook:** **Custom user on day one. Always.**

**Object-level permissions** aren't built in — name `django-guardian`, or a `has_permission`
check in the service layer.

---

# PART 12 — DJANGO REST FRAMEWORK ⭐⭐

**If the role involves APIs, this is where the questions go.**

## 12.1 Serializers

```python
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source="account.name", read_only=True)
    notional = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "symbol", "side", "qty", "price",
                  "account_name", "notional"]
        read_only_fields = ["id"]

    def get_notional(self, obj):
        return obj.qty * obj.price

    def validate_qty(self, value):
        if value <= 0:
            raise serializers.ValidationError("must be positive")
        return value

    def validate(self, data):          # cross-field
        return data
```

**Say:** *"A serializer does three jobs: validate incoming data, convert models to JSON, and define the API contract. It's AutoMapper plus FluentValidation in one class. `ModelSerializer` derives fields from the model, which is convenient but I list `fields` explicitly — `__all__` means a new column silently becomes public."*

**Hook:** **Never `fields = "__all__"` on a public API.**

## 12.2 ViewSets and routers

```python
from rest_framework import viewsets, permissions, filters

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["symbol"]

    def get_queryset(self):
        return (Order.objects
                .select_related("account")            # ⭐ no N+1
                .filter(account__owner=self.request.user))

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# urls.py
router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")
urlpatterns = [path("api/v1/", include(router.urls))]
```

One `ModelViewSet` + router gives you list, create, retrieve, update, partial update, destroy —
with correct status codes and URLs.

## 12.3 The rest of DRF

| Feature | How |
|---|---|
| Auth | `TokenAuthentication`, `SessionAuthentication`, `SimpleJWT` |
| Permissions | `IsAuthenticated`, `DjangoModelPermissions`, custom `BasePermission` |
| Throttling | `AnonRateThrottle`, `UserRateThrottle`, `ScopedRateThrottle` |
| Pagination | `PageNumberPagination`, `LimitOffsetPagination`, **`CursorPagination`** ⭐ |
| Filtering | `django-filter` |
| Versioning | URL path, header, or query param |
| Schema/docs | `drf-spectacular` → OpenAPI |

⚠️ **Trap: "Which pagination for a large, live table?"** → *"Cursor pagination. Offset pagination gets slower as the offset grows, and rows shift between pages when data is being inserted. A cursor on an indexed, ordered column is stable and constant time."*

**Hook:** **Big or live data → cursor pagination.**

---

# PART 13 — MIDDLEWARE

```python
# settings.py — order matters
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",   # needs session first
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

```python
class CorrelationIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response          # runs ONCE at startup

    def __call__(self, request):
        request.correlation_id = request.headers.get("X-Request-ID", str(uuid4()))
        response = self.get_response(request)     # everything downstream
        response["X-Request-ID"] = request.correlation_id
        return response
```

**Say:** *"Middleware is the request pipeline, same shape as ASP.NET Core. `__init__` runs once at startup, `__call__` per request. Order matters — authentication needs the session, so it must come after session middleware."*

---

# PART 14 — SETTINGS AND DEPLOYMENT

## 14.1 Settings

```python
import os
DEBUG = os.environ["DJANGO_DEBUG"] == "1"        # ⚠️ NEVER True in production
SECRET_KEY = os.environ["SECRET_KEY"]            # never in git
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")
DATABASES = {"default": dj_database_url.config(conn_max_age=600)}
```

Split settings: `base.py` / `dev.py` / `prod.py`, or one file driven by environment variables.
`django-environ` or Pydantic Settings both work.

⚠️ **`DEBUG=True` in production leaks the full stack trace, settings and SQL to any visitor.**
It's the single most common Django breach. Say this if security comes up.

## 14.2 Deploy

```bash
gunicorn config.wsgi:application --workers 4 --bind 0.0.0.0:8000
# or async:
uvicorn config.asgi:application --workers 4
```

| Item | Answer |
|---|---|
| Static files | `collectstatic` → WhiteNoise or a CDN |
| Media | S3 / Azure Blob, never the app disk |
| Migrations | a job before the rollout |
| Workers | ~`2 × cores + 1` |
| `CONN_MAX_AGE` | persistent DB connections; use PgBouncer at scale |
| Checklist | `manage.py check --deploy` ⭐ |
| Monitoring | Sentry, structured JSON logs, OpenTelemetry |

---

# PART 15 — CACHING AND CELERY

## 15.1 Cache layers

```python
from django.core.cache import cache
cache.set("prices:VOD", data, timeout=60)
cache.get("prices:VOD")
cache.get_or_set("k", expensive_fn, 300)

from django.views.decorators.cache import cache_page
@cache_page(60 * 15)
def report(request): ...
```

| Layer | Use |
|---|---|
| Per-site / per-view | whole pages |
| Template fragment | `{% cache 300 "sidebar" %}` |
| Low-level `cache.*` | ⭐ most control. What I'd use |
| Backend | Redis or Memcached. Not local memory across workers |

⚠️ **Locmem cache is per process.** With four workers you get four inconsistent caches. Say it.

## 15.2 Celery

```python
@shared_task(bind=True, max_retries=3, autoretry_for=(RequestException,),
             retry_backoff=True)
def reconcile(self, order_id): ...

transaction.on_commit(lambda: reconcile.delay(order.id))     # ⭐
```

**Say:** *"Celery with Redis or RabbitMQ for anything slow or unreliable — reconciliation, reports, emails, third-party calls. Tasks must be idempotent, because at-least-once delivery means they will be retried. And I queue them in `on_commit`, or the worker can start before the transaction commits and not find the row."*

**Hook:** **Idempotent tasks. Queue on commit.**

---

# PART 16 — ASYNC DJANGO

| Version | Added |
|---|---|
| 3.0 | ASGI support |
| 3.1 | async views, async middleware |
| 4.1 | **async ORM** (`afilter`, `aget`, `acreate`, `async for`) |
| 4.2+ | async class-based views, more coverage |

```python
async def prices(request):
    orders = [o async for o in Order.objects.filter(symbol="VOD")]
    return JsonResponse({"n": len(orders)})
```

⚠️ **The trap:** calling **sync ORM code inside an async view** raises
`SynchronousOnlyOperation`. Wrap it: `await sync_to_async(fn)(...)`.
The reverse is `async_to_sync`.

**Say:** *"Django's async support is real but partial — the ORM has async methods since 4.1, though many third-party packages are still sync-only, and Django wraps them with `sync_to_async` in a threadpool. If a service is genuinely async-heavy — WebSockets, thousands of concurrent connections — I'd use FastAPI. If it's a product that occasionally does async work, Django is fine."*

**Django Channels** = WebSockets and background consumers for Django, over ASGI with a Redis
channel layer.

---

# PART 17 — SECURITY

| Threat | Django's answer |
|---|---|
| SQL injection | ORM parameterises everything. Raw SQL must use `%s` params |
| XSS | template auto-escaping. ⚠️ `\|safe` opts out |
| CSRF | `CsrfViewMiddleware` + `{% csrf_token %}`. Cookie + hidden field must match |
| Clickjacking | `XFrameOptionsMiddleware` → `X-Frame-Options: DENY` |
| Passwords | PBKDF2 with salt by default. argon2 available |
| HTTPS | `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `SESSION_COOKIE_SECURE` |
| Host header attack | `ALLOWED_HOSTS` |
| Mass assignment | explicit `fields` on forms/serializers |
| Secrets | env vars. `SECRET_KEY` never in git |
| Info leak | ⚠️ `DEBUG = False` |
| Audit | `manage.py check --deploy` |

**Say:** *"Django's security defaults are strong — the common web vulnerabilities are handled unless you actively opt out with `|safe`, `csrf_exempt`, `fields = '__all__'` or `DEBUG=True`. So in review I look for the opt-outs, not the vulnerabilities."*

**Hook:** **Django is safe by default. Look for the opt-outs.**

---

# PART 18 — PERFORMANCE ⭐ (the N+1 answer)

## 18.1 The N+1 problem — the single most asked Django question

```python
# BAD — 1 query for orders + 1 per order for the account = 101 queries
for order in Order.objects.all()[:100]:
    print(order.account.name)

# GOOD — one query with a JOIN
for order in Order.objects.select_related("account")[:100]:
    print(order.account.name)

# For many-to-many / reverse FK — 2 queries total
for acct in Account.objects.prefetch_related("orders"):
    for o in acct.orders.all(): ...

# Control the prefetched queryset
Account.objects.prefetch_related(
    Prefetch("orders", queryset=Order.objects.filter(filled=False))
)
```

| | Use for | How |
|---|---|---|
| `select_related` | ForeignKey, OneToOne (**forward**) | SQL JOIN, one query |
| `prefetch_related` | ManyToMany, reverse FK | a second query, joined in Python |

**Say the whole thing:**
> *"N+1 is one query for the list and then one more per row when you touch a relation. `select_related` does a JOIN and is for forward foreign keys. `prefetch_related` runs a second query and joins in Python, which is what you need for many-to-many and reverse relations because a JOIN would multiply rows. I catch these with `django-debug-toolbar` in development and by asserting query counts in tests with `assertNumQueries`."*

**Hook:** **`select_related` = JOIN forward. `prefetch_related` = second query.**

## 18.2 The rest of the checklist

| Fix | Effect |
|---|---|
| `only()` / `defer()` | fetch fewer columns |
| `values()` / `values_list()` | skip model instantiation entirely |
| `bulk_create` / `bulk_update` | one query instead of N |
| `.update()` on a queryset | one UPDATE, no per-object save |
| `iterator(chunk_size=)` | stream a huge queryset without caching it |
| `exists()` not `count()` | when you only need a yes/no |
| `count()` not `len(qs)` | when you don't need the objects |
| Indexes | `db_index=True`, `Meta.indexes`, composite in query order |
| `select_for_update` | correctness under concurrency |
| Caching | Redis for hot reads |
| `CONN_MAX_AGE` / PgBouncer | connection reuse |
| `django-debug-toolbar` | ⭐ see every query per page |
| `assertNumQueries` | ⭐ stop regressions in CI |
| `.explain()` | read the query plan |

**Say:** *"I measure with debug-toolbar or `connection.queries`, then fix the N+1 first — it's almost always the biggest item. Then column selection, then indexes. And I lock the fix in with `assertNumQueries`, so the next person's innocent change doesn't reintroduce it."*

---

# PART 19 — TESTING

```python
from django.test import TestCase, Client
from django.urls import reverse

class OrderTests(TestCase):
    @classmethod
    def setUpTestData(cls):                 # ⭐ once per class, not per test
        cls.account = Account.objects.create(name="Test")

    def test_create(self):
        r = self.client.post(reverse("order-list"),
                             {"symbol": "VOD", "qty": 10, "price": "1.5"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)

    def test_no_n_plus_one(self):
        with self.assertNumQueries(2):      # ⭐ locks in the fix
            list(Account.objects.prefetch_related("orders"))
```

| Tool | For |
|---|---|
| `TestCase` | wraps each test in a transaction and rolls back — fast |
| `TransactionTestCase` | when you need real commits |
| `setUpTestData` | class-level fixtures, much faster than `setUp` |
| `Client` | in-process HTTP |
| `assertNumQueries` | ⭐ query-count regression guard |
| `pytest-django` | pytest fixtures and style |
| `factory_boy` | test object factories instead of fixtures |
| `freezegun` | control time |

**Say:** *"`TestCase` rolls back per test, so tests are isolated and fast. I use `setUpTestData` for shared objects, `factory_boy` instead of JSON fixtures because fixtures rot, and `assertNumQueries` on list endpoints so an N+1 can't sneak back in."*

---

# PART 20 — DJANGO vs FASTAPI vs ASP.NET

| | **Django** | **FastAPI** | **ASP.NET Core** |
|---|---|---|---|
| Philosophy | batteries included | minimal, async-first | batteries included |
| ORM | built in (Active Record) | bring SQLAlchemy | EF Core (Data Mapper) |
| Migrations | built in | Alembic | EF Migrations |
| Admin | **yes** ⭐ | no | no |
| Auth | built in | build it | Identity |
| Validation | forms / DRF serializers | **Pydantic** ⭐ | DataAnnotations |
| API docs | DRF + spectacular | **automatic** ⭐ | Swashbuckle |
| Async | partial | **native** | native |
| Raw speed | moderate | fast | **fastest** |
| Learning curve | large but guided | small | large |
| Best for | products, back offices, CMS | microservices, ML, real-time | enterprise .NET |

**The answer to "which and why?":**
> *"It depends how much of the system isn't the API. A product with users, roles, an admin back office and reporting — Django, because that's months of work already built and integrated. A service that exposes an API, especially async or model-serving — FastAPI. And in a .NET shop I'd keep the transactional core in ASP.NET Core and use Python services for analytics and quant, behind a versioned contract so the boundary stays explicit."*

---

# PART 21 — RAPID-FIRE: 80 QUESTIONS

| # | Q | A |
|---|---|---|
| 1 | Django in one line? | Batteries-included Python web framework |
| 2 | MVT? | Model, View (controller), Template (view) |
| 3 | Project vs app? | Deployment unit vs feature module |
| 4 | ORM pattern? | Active Record |
| 5 | EF's pattern? | Data Mapper |
| 6 | Are QuerySets lazy? | Yes |
| 7 | What evaluates one? | Iterate, slice, `len`, `list`, `count`, `exists` |
| 8 | N+1 problem? | One query per row when touching a relation |
| 9 | Fix for forward FK? | `select_related` — a JOIN |
| 10 | Fix for M2M / reverse? | `prefetch_related` — second query |
| 11 | Why not JOIN for M2M? | It multiplies rows |
| 12 | Spot N+1? | `django-debug-toolbar`, `assertNumQueries` |
| 13 | `F()` object? | Reference a column. Atomic SQL update |
| 14 | `Q()` object? | Complex OR / NOT filters |
| 15 | `annotate` vs `aggregate`? | Per-group column vs one summary row |
| 16 | GROUP BY? | `values().annotate()` |
| 17 | `get()` risks? | `DoesNotExist`, `MultipleObjectsReturned` |
| 18 | `get_or_create`? | Fetch or insert |
| 19 | Insert many? | `bulk_create` |
| 20 | Update many? | `.update()` on the queryset |
| 21 | Traverse relations in a filter? | Double underscore `__` |
| 22 | Money field? | `DecimalField` |
| 23 | Never for money? | `FloatField` |
| 24 | `null` vs `blank`? | Database NULL vs form empty |
| 25 | `null=True` on CharField? | No — two kinds of empty |
| 26 | `on_delete` default? | None. You must choose |
| 27 | Safest `on_delete` for finance? | `PROTECT` |
| 28 | `related_name`? | Names the reverse accessor |
| 29 | DB-level rules? | `Meta.constraints` |
| 30 | Does `save()` validate? | No — `full_clean` isn't called |
| 31 | Add an index? | `db_index=True` or `Meta.indexes` |
| 32 | Transaction? | `@transaction.atomic` |
| 33 | Row lock? | `select_for_update` |
| 34 | Queue a job safely? | `transaction.on_commit` |
| 35 | Why? | Worker can beat the commit |
| 36 | Default transaction mode? | Autocommit |
| 37 | Raw SQL safely? | `%s` params, never f-strings |
| 38 | Create a migration? | `makemigrations` |
| 39 | Apply? | `migrate` |
| 40 | Preview the SQL? | `sqlmigrate` |
| 41 | Data migration model import? | `apps.get_model` |
| 42 | Run migrations when? | A job before rollout |
| 43 | Big-table schema change? | Expand, migrate, contract |
| 44 | FBV vs CBV? | Logic vs standard CRUD |
| 45 | Generic views? | List, Detail, Create, Update, Delete |
| 46 | Build a URL? | `reverse()` / `{% url %}` |
| 47 | URL converters? | int, str, slug, uuid, path |
| 48 | Template auto-escaping? | On by default |
| 49 | Turn it off? | `\|safe` ⚠️ |
| 50 | Template inheritance? | `extends` + `block` |
| 51 | ModelForm? | Form derived from a model |
| 52 | Validate one field? | `clean_<field>` |
| 53 | Validate across fields? | `clean` |
| 54 | The admin gives? | Generated CRUD back office |
| 55 | Admin N+1 fix? | `list_select_related` |
| 56 | Admin limits? | Internal staff only |
| 57 | Custom user model? | Day one. `AUTH_USER_MODEL` |
| 58 | Password hashing? | PBKDF2 default, argon2 available |
| 59 | Protect a view? | `@login_required` / `LoginRequiredMixin` |
| 60 | Object-level perms? | Not built in — `django-guardian` |
| 61 | DRF serializer does? | Validate + map + define the contract |
| 62 | Avoid in serializers? | `fields = "__all__"` |
| 63 | ModelViewSet gives? | Full CRUD + router URLs |
| 64 | DRF throttling? | Anon/User/Scoped rate throttles |
| 65 | Pagination for big data? | Cursor pagination |
| 66 | Why not offset? | Slow at depth, shifts on insert |
| 67 | DRF JWT? | `SimpleJWT` |
| 68 | OpenAPI docs? | `drf-spectacular` |
| 69 | Middleware order? | Down on request, up on response |
| 70 | Auth middleware needs? | Session middleware before it |
| 71 | `DEBUG=True` in prod? | Leaks settings and stack traces |
| 72 | Deploy check? | `manage.py check --deploy` |
| 73 | Static files? | `collectstatic` + WhiteNoise/CDN |
| 74 | Cache backend? | Redis or Memcached |
| 75 | Locmem cache issue? | Per process — inconsistent |
| 76 | Background jobs? | Celery |
| 77 | Celery task rule? | Must be idempotent |
| 78 | Async ORM since? | 4.1 |
| 79 | Sync ORM in async view? | `SynchronousOnlyOperation` — use `sync_to_async` |
| 80 | WebSockets in Django? | Channels |

---

## ✅ Before you close this file

- [ ] Say the **Part 0** table, all 12
- [ ] Say the **N+1 answer** (Part 18.1) word for word
- [ ] Explain **`select_related` vs `prefetch_related`** and *why* they differ
- [ ] Explain **lazy QuerySets** and what triggers evaluation
- [ ] Say the **migration deployment** answer (Part 5)
- [ ] Run the **Part 21** rapid-fire, target 65/80

**Then go to `06c-orm-databases.md`.**
