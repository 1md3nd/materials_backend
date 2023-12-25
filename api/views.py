from django.shortcuts import render
from datetime import datetime
from rest_framework.decorators import api_view

import sys
import path

directory = path.Path(__file__).abspath()
sys.path.append(directory.parent)

from apis.materials import all_materials, search_materials_by_formula,compare_fields_by,boolen_filter_,validate_field_,search_text_

# Create your views here.
@api_view(['GET'])
def home(request):
    return render(
        request,
        "home.html",
        {   "date":datetime.today()
         },
    )

def get_all_materials(request):
    response = all_materials(request=request)
    return response


def search_materials_formula(request):
    return search_materials_by_formula(request)

def compare_fields(request):
    return compare_fields_by(request)

def boolen_filter(request,field,value):
    return boolen_filter_(request,field,value)

def validate_field(request,field=None):
    return validate_field_(request,field)

def search_text(request):
    return search_text_(request)