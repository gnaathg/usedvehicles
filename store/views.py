from django.shortcuts import render, redirect
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
        form_data = request.POST
        form_instance = self.form_class(form_data)

        if form_instance.is_valid():
            data = form_instance.cleaned_data
            Vehicle.objects.create( #**data
                name=data.get("name"),
                varient=data.get("varient"),
                description=data.get("description"),
                fuel_type=data.get("fuel_type"),
                running_km=data.get("running_km"),
                color=data.get("color"),
                price=data.get("price"),
                brand=data.get("brand"),
                owner_type=data.get("owner_type")  
            )
            
            # Redirect to the vehicle list view after successful form submission
            return redirect("vehicle-list")

        # Render the form again with errors if form is not valid
        return render(request, self.template_name, {"form": form_instance})

class VehicleListView(View):
    template_name = "vehicle_list.html"

    def get(self, request, *args, **kwargs):
        qs = Vehicle.objects.all()
        return render(request, self.template_name, {"data": qs})

class VehicleDetailView(View):

    template_name = "vehicle_detail.html"

    def get(self,request,*args,**kwargs):

        id =kwargs.get("id")

        qs =Vehicle.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})

class VehicleDeleteView(View):


    def get(self,request,*args,**kwargs):

        id = kwargs.get("id")

        Vehicle.objects.get(id=id).delete()

        return redirect("vehicle-list")

class VehicleUpdateView(View):

    template_name = "vehicle_edit.html"

    form_class = VehicleForm

    def get(self,request,*args,**kwargs):

        form_instance = self.form_class()

        return render(request,self.template_name,{'form':form_instance})