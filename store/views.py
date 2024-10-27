from django.shortcuts import render
from django.views.generic import View
from store.forms import VehicleForm
from store.models import Vehicle  

# Create your views here.

class VehicleView(View):

    template_name = "vehicle.html"

    form_class = VehicleForm

    def get(self, request, *args, **kwargs):

        form_instance = self.form_class()

        return render(request, self.template_name, {'form': form_instance})

    def post(self, request, *args, **kwargs):

        form_instance = self.form_class(request.POST)

        if form_instance.is_valid():

            Vehicle.objects.create(**form_instance.cleaned_data)

            print("Form submitted and saved.")

            return render(request, self.template_name, {"form": form_instance})

        
        print("Form is invalid.")

        return render(request, self.template_name, {"form": form_instance})



class VehicleListView(View):

    template_name = "vehicle_list.html"

    def get(self, request, *args, **kwargs):
        
        qs = Vehicle.objects.all()

        return render(request, self.template_name, {"data": qs})

