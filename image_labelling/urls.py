from django.urls import path

from image_labelling.views import ImageView, ImageListView, LabelView, ImageLabelsView, ImageLabelsSearchView, ImageMetadataView

urlpatterns = [
    path("image", ImageView.as_view(), name='image'),
    path("image/list", ImageListView.as_view(), name='list_images'),
    path("label", LabelView.as_view(), name='label'),
    path("list", ImageLabelsView.as_view(), name='image_labels_list'),
    path("search", ImageLabelsSearchView.as_view(), name='image_labels_search'),
    path("image/metadata", ImageMetadataView.as_view(), name='image_metadata'),
]