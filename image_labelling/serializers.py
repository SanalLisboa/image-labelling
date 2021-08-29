from rest_framework import serializers

from image_labelling.settings import STATUS_CHOICES


class MultiImageUploadSerializer(serializers.Serializer):

    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False)
    )


class ListRequestSerialzier(serializers.Serializer):

    start_idx = serializers.IntegerField(required=False)
    end_idx = serializers.IntegerField(required=False)
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)

    def validate(self, data):

        start_idx = data.get('start_idx')
        end_idx = data.get('end_idx')

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if (not start_idx and start_idx != 0) and end_idx:
            raise serializers.ValidationError("Start index cannot be null when end index is given")
        elif start_idx and (not end_idx and end_idx != 0):
            raise serializers.ValidationError("End index cannot be null when start index is given")
        elif start_idx and end_idx and start_idx >= end_idx:
            raise serializers.ValidationError("Start index should be less than end index")
        
        if not start_date and end_date:
            raise serializers.ValidationError("Start date cannot be null when end date is given")
        elif start_date and not end_date:
            raise serializers.ValidationError("End date cannot be null when start date is given")
        elif start_date and start_date and start_date >= end_date:
            raise serializers.ValidationError("Start date should be less than end date")
    
        return data


class ImageRenderRequestSerializer(serializers.Serializer):

    image_id = serializers.UUIDField()


class ImageListResponseSerialzier(serializers.Serializer):

    id = serializers.UUIDField()
    format = serializers.CharField()
    uploaded_on = serializers.DateTimeField()
    created_by = serializers.CharField()


class CoordinatesSerializer(serializers.Serializer):

    x1 = serializers.FloatField()
    y1 = serializers.FloatField()
    x2 = serializers.FloatField()
    y2 = serializers.FloatField()


class LabelImageRequestSerializer(serializers.Serializer):

    image_id = serializers.UUIDField()
    coordinates = CoordinatesSerializer()
    label = serializers.CharField(max_length=30)


class LabelProcessingRequestSerialzier(serializers.Serializer):

    label_id = serializers.UUIDField()
    image_id = serializers.UUIDField()


class LabelListRequestSerialzier(serializers.Serializer):

    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)

    def validate(self, data):

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if not start_date and end_date:
            raise serializers.ValidationError("Start date cannot be null when end date is given")
        elif start_date and not end_date:
            raise serializers.ValidationError("End date cannot be null when start date is given")
        elif start_date and start_date and start_date >= end_date:
            raise serializers.ValidationError("Start date should be less than end date")
    
        return data


class LabelsSerializer(serializers.Serializer):

    created_by = serializers.CharField()
    id = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    label = serializers.CharField()
    coordinates = CoordinatesSerializer()


class ImageLabelsListResponseSerialzier(serializers.Serializer):

    image_id = serializers.UUIDField()
    image_format = serializers.CharField()
    image_uploaded_on = serializers.DateTimeField()
    image_created_by = serializers.CharField()
    labels = LabelsSerializer(many=True)
    image_status = serializers.IntegerField()


class ImageSearchRequestSerialzier(serializers.Serializer):

    query = serializers.CharField()


class ImageSearchResponseSerializer(serializers.Serializer):

    image_id = serializers.UUIDField()
    image_format = serializers.CharField()
    image_uploaded_on = serializers.DateTimeField()
    image_uploaded_by = serializers.CharField()
    label_id = serializers.UUIDField()
    label_created_at = serializers.DateTimeField()
    label_updated_at = serializers.DateTimeField()
    labeled_by = serializers.CharField()
    label = serializers.CharField()
    coordinates = CoordinatesSerializer()
    similarity = serializers.FloatField()


class LabelByImageIDRequestSerializer(serializers.Serializer):

    image_id = serializers.UUIDField()


class ImageMetadataSerializer(serializers.Serializer):

    uploaded_by = serializers.CharField()
    uploaded_on = serializers.DateTimeField()
    sha = serializers.CharField()
    format = serializers.CharField()
