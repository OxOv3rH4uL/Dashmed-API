from rest_framework.pagination import PageNumberPagination

class FixedPageSizePagination(PageNumberPagination):
    page_size = 10 #Increase the page size if you want
    max_page_size = 10 #Increase the max page size if you want :)
