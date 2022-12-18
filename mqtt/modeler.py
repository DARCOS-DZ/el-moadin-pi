

def get_model(model, **kwargs):
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get(model=model)
        model_class = ct.model_class()
        object_init = model_class(**kwargs)
        object_init.save()
        return object_init
