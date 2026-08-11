from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2                  # Количество элементов на странице по умолчанию
    page_size_query_param = 'page_size'  # Параметр в URL для переопределения размера (например, ?page_size=20)
    max_page_size = 50              # Максимально допустимое количество элементов на страницу