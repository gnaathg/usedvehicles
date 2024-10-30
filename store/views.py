from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import View
from store.forms import VehicleForm
from store.models import Vehicle  
from django.db.models import Q

# Create your views here.

class VehicleView(View):
    template_name = "vehicle.html"
    form_class = VehicleForm

    def get(self, request, *args, **kwargs):
        form_instance = self.form_class()
        return render(request, self.template_name, {'form': form_instance})

    def post(self, request, *args, **kwargs):
        form_data = request.POST
        form_instance = self.form_class(form_data,files=request.FILES)

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
                owner_type=data.get("owner_type"),  
                picture=data.get("picture")
            )
            
            # Redirect to the vehicle list view after successful form submission
            return redirect("vehicle_list")

        # Render the form again with errors if form is not valid
        return render(request, self.template_name, {"form": form_instance})

class VehicleListView(View):


    template_name = "vehicle_list.html"

    def get(self, request, *args, **kwargs):

        search_text = request.GET.get("filter")

        qs = Vehicle.objects.all()

        all_names = Vehicle.objects.values_list("name",flat=True).distinct()

        all_fuel_types = Vehicle.objects.values_list("fuel_type",flat=True).distinct()
        
        all_owner_types = Vehicle.objects.values_list("owner_type",flat=True).distinct()

        all_brands = Vehicle.objects.values_list("brand",flat=True).distinct() 

        all_records = []

        all_records.extend(all_names)
        all_records.extend(all_fuel_types)
        all_records.extend(all_owner_types)
        all_records.extend(all_brands)


        if search_text:

            qs = qs.filter(
                            Q(name__contains=search_text)|
                            Q(owner_type__contains=search_text)|
                            Q(fuel_type__contains=search_text)|
                            Q(brand__contains=search_text)
                            )

        return render(request, self.template_name, {"data": qs, "records":all_records})

class VehicleDetailView(View):

    template_name = "vehicle_detail.html"

    def get(self,request,*args,**kwargs):

        id =kwargs.get("id")

        qs =Vehicle.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})

class VehicleDeleteView(View):

    def get(self, request, *args, **kwargs):

        id = kwargs.get("id")

        vehicle = get_object_or_404(Vehicle, id=id)

        vehicle.delete()

        return redirect("vehicle_list")


class VehicleUpdateView(View):

    template_name = "vehicle_edit.html"

    form_class = VehicleForm

    def get(self,request,*args,**kwargs):

        id = kwargs.get('id')

        vehicle_object = get_object_or_404(Vehicle,id=id)

        data = {

            'name' : vehicle_object.name,
            'varient'  :vehicle_object.varient,
            'description' :vehicle_object.description,
            'fuel_type' :vehicle_object.fuel_type,
            'running_km' :vehicle_object.running_km,
            'color' :vehicle_object.color,
            'price' :vehicle_object.price,
            'brand' :vehicle_object.brand,
            'owner_type' :vehicle_object.owner_type
        }

        form_instance = self.form_class(initial=data)

        return render(request,self.template_name,{'form':form_instance})

    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data,files=request.FILES)

        if form_instance.is_valid():

            data = form_instance.cleaned_data

            Vehicle.objects.filter(id=kwargs.get('id')).update(**data)
        
            return redirect("vehicle_list")

        return render(request,self.template_name,{"form":form_instance})    