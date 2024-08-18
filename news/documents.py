# # news/documents.py
# # from django_elasticsearch_dsl import Document, Index
# # from django_elasticsearch_dsl.registries import registry
# from .models import CrawlHackerNews

# @registry.register_document
# class CrawlHackerNewsDocument(Document):
#     class Index:
#         name = 'news'
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0,
#         }

#     class Django:
#         model = CrawlHackerNews
#         fields = [
#             'title',
#             'link',
#             'points',
#             'date',
#         ]
