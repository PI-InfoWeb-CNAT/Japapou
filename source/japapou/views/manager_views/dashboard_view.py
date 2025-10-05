from django.shortcuts import render  # type: ignore
from django.http import HttpRequest, HttpResponse  # type: ignore
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required, permission_required


class Sale:
    def __init__(self, date_str: str, plates: list[dict[str, int]]):
        self.date: datetime = datetime.strptime(date_str, "%d/%m/%Y")
        self.plates: list[dict[str, int]] = plates
        self.total: int = sum([plate["subtotal"] for plate in plates])


@login_required
@permission_required('japapou.change_plate', login_url='home')
def manager_dashboard_view(request: HttpRequest) -> HttpResponse:
    sales_data: list[dict] = [
        {
            "id": 1,
            "date": "20/06/2025",
            "plates": [
                {
                    "amount": 2,
                    "subtotal": 30,
                    "name": "Salmon Nigiri",
                    "price": 15,
                },
                {
                    "amount": 1,
                    "subtotal": 12,
                    "name": "Miso Soup",
                    "price": 12,
                },
            ],
        },
        {
            "id": 2,
            "date": "24/06/2025",
            "plates": [
                {
                    "amount": 1,
                    "subtotal": 18,
                    "name": "Chicken Teriyaki",
                    "price": 18,
                },
                {
                    "amount": 1,
                    "subtotal": 8,
                    "name": "Edamame",
                    "price": 8,
                },
            ],
        },
        {
            "id": 3,
            "date": "29/06/2025",
            "plates": [
                {
                    "amount": 3,
                    "subtotal": 45,
                    "name": "Tuna Roll",
                    "price": 15,
                }
            ],
        },
        {
            "id": 4,
            "date": "29/06/2025",
            "plates": [
                {
                    "amount": 1,
                    "subtotal": 20,
                    "name": "Tempura Udon",
                    "price": 20,
                },
                {
                    "amount": 2,
                    "subtotal": 10,
                    "name": "Green Tea Ice Cream",
                    "price": 5,
                },
            ],
        },
        {
            "id": 5,
            "date": "30/06/2025",
            "plates": [
                {
                    "amount": 2,
                    "subtotal": 26,
                    "name": "Shrimp Tempura",
                    "price": 13,
                },
                {
                    "amount": 1,
                    "subtotal": 14,
                    "name": "Spicy Tuna Roll",
                    "price": 14,
                },
            ],
        },
        {
            "id": 6,
            "date": "01/07/2025",
            "plates": [
                {
                    "amount": 1,
                    "subtotal": 22,
                    "name": "Beef Donburi",
                    "price": 22,
                },
                {
                    "amount": 1,
                    "subtotal": 6,
                    "name": "Pickled Vegetables",
                    "price": 6,
                },
            ],
        },
        {
            "id": 7,
            "date": "01/07/2025",
            "plates": [
                {
                    "amount": 1,
                    "subtotal": 25,
                    "name": "Sashimi Deluxe",
                    "price": 25,
                },
                {
                    "amount": 2,
                    "subtotal": 16,
                    "name": "Gyoza",
                    "price": 8,
                },
            ],
        },
        {
            "id": 8,
            "date": "02/07/2025",
            "plates": [
                {
                    "amount": 4,
                    "subtotal": 60,
                    "name": "Salmon Nigiri",
                    "price": 15,
                },
                {
                    "amount": 2,
                    "subtotal": 24,
                    "name": "Miso Soup",
                    "price": 12,
                },
                {
                    "amount": 1,
                    "subtotal": 18,
                    "name": "Chicken Teriyaki",
                    "price": 18,
                },
            ],
        },
        {
            "id": 9,
            "date": "02/07/2025",
            "plates": [
                {
                    "amount": 2,
                    "subtotal": 30,
                    "name": "Tuna Roll",
                    "price": 15,
                },
                {
                    "amount": 1,
                    "subtotal": 20,
                    "name": "Tempura Udon",
                    "price": 20,
                },
            ],
        },
        {
            "id": 10,
            "date": "03/07/2025",
            "plates": [
                {
                    "amount": 3,
                    "subtotal": 66,
                    "name": "Beef Donburi",
                    "price": 22,
                },
                {
                    "amount": 2,
                    "subtotal": 16,
                    "name": "Gyoza",
                    "price": 8,
                },
            ],
        },
        {
            "id": 11,
            "date": "03/07/2025",
            "plates": [
                {
                    "amount": 1,
                    "subtotal": 25,
                    "name": "Sashimi Deluxe",
                    "price": 25,
                },
                {
                    "amount": 3,
                    "subtotal": 39,
                    "name": "Shrimp Tempura",
                    "price": 13,
                },
            ],
        },
        {
            "id": 12,
            "date": "04/07/2025",
            "plates": [
                {
                    "amount": 2,
                    "subtotal": 36,
                    "name": "Chicken Teriyaki",
                    "price": 18,
                },
                {
                    "amount": 4,
                    "subtotal": 20,
                    "name": "Green Tea Ice Cream",
                    "price": 5,
                },
            ],
        },
        {
            "id": 13,
            "date": "05/07/2025",
            "plates": [
                {
                    "amount": 5,
                    "subtotal": 75,
                    "name": "Tuna Roll",
                    "price": 15,
                },
                {
                    "amount": 2,
                    "subtotal": 12,
                    "name": "Pickled Vegetables",
                    "price": 6,
                },
            ],
        },
        {
            "id": 14,
            "date": "06/07/2025",
            "plates": [
                {
                    "amount": 1,
                    "subtotal": 22,
                    "name": "Beef Donburi",
                    "price": 22,
                },
                {
                    "amount": 1,
                    "subtotal": 14,
                    "name": "Spicy Tuna Roll",
                    "price": 14,
                },
                {
                    "amount": 2,
                    "subtotal": 16,
                    "name": "Gyoza",
                    "price": 8,
                },
            ],
        },
        {
            "id": 15,
            "date": "07/07/2025",
            "plates": [
                {
                    "amount": 3,
                    "subtotal": 60,
                    "name": "Tempura Udon",
                    "price": 20,
                },
                {
                    "amount": 2,
                    "subtotal": 26,
                    "name": "Shrimp Tempura",
                    "price": 13,
                },
            ],
        },
    ]

    sales: list[Sale] = []
    for sale_data in sales_data:
        sales.append(Sale(sale_data["date"], sale_data["plates"]))

    month_labels: list[str] = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    week_labels: list[str] = [
        "Domingo",
        "Segunda",
        "Terça",
        "Quarta",
        "Quinta",
        "Sexta",
        "Sábado",
    ]
    sales_per_month: list[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sales_per_week: list[int] = [0, 0, 0, 0, 0, 0, 0]

    sales_this_year: list[Sale] = []
    for sale in sales:
        if sale.date.year == datetime.now().year:
            sales_this_year.append(sale)

    for sale in sales_this_year:
        sales_per_month[sale.date.month - 1] += sale.total

    sales_this_week: list[Sale] = []
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    for sale in sales:
        if sale.date >= week_start:
            sales_this_week.append(sale)

    for sale in sales_this_week:
        sales_per_week[sale.date.weekday()] += sale.total

    # context = {
    #     "labels": month_labels,
    #     "sales": sales_per_month,
    # }
    context = {
        "labels": week_labels,
        "sales": sales_per_week,
    }

    print(context)

    return render(
        request, template_name="manager/dashboard.html", context=context, status=200
    )
