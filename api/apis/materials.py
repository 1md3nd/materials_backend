from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bson.json_util import dumps
from .mongo_client_local import MongoConnection
from pymongo.errors import PyMongoError
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import json

def stream_data(collection):
    try:
        findAll = collection.find()
        df = pd.DataFrame(list(findAll))
        df['_id'] = df['_id'].astype(str)
        df= df.fillna('')
        df = df.T
        return Response(df.to_dict())
    except PyMongoError as e:
        return Response({'error': f'Error retrieving data: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def add_data(collection, data):
    try:
        # Insert the data into the MongoDB collection
        result = collection.insert_one(data)
        if result.inserted_id:
            return Response({'message': 'Data inserted successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to insert data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except PyMongoError as e:
        return Response({'error': f'Error inserting data: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET', 'POST'])
def all_materials(request):
    collection = MongoConnection.get_connection().get_database('materials').get_collection('all_materials')
    if request.method == 'GET':
        return stream_data(collection)
    elif request.method == 'POST':
        try:
            data = request.data
            print(data)
            # Call the add_data function to insert the data
            
        except PyMongoError as e:
            return Response({'error': f'Error retrieving data: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
def search_materials_by_formula(request):
    collection = MongoConnection.get_connection().get_database('materials').get_collection('all_materials')
    try:
        element = request.GET.get('element')
        elements = request.GET.get('elements')
        contain_only_element = request.GET.get('containsonly')
        sort_fields = request.GET.get('sort_field')
        sort_bys = request.GET.get('sort_order')

        # projection = {'__search_score': { '$meta': "textScore" } }
        condition = {}
        sort_cond = {}

        if element:
            condition['$text'] = {'$search':element,'$caseSensitive': True}

        elif elements:
            search_query = ''
            for element in elements.split(','):
                search_query += '\\"' + element + '\"'
            condition['$text'] = {'$search':search_query, '$caseSensitive':True}
        
        elif contain_only_element:
            search_query = ''
            for element in contain_only_element.split(','):
                search_query += '\\"' + element + '\"'
                condition['$text'] = {'$search':search_query, '$caseSensitive':True}
                condition['compounds_contain_count'] = len(contain_only_element.split(','))
        
        if sort_fields and sort_bys:
            sort_fields = list(sort_fields.split(','))
            sort_bys = list(sort_bys.split(','))
            for sort_field, sort_by in zip(sort_fields,sort_bys):
                sort_cond[sort_field] = 1 if sort_by == 'asc' else -1

        if len(condition) == 0:
            if sort_fields:
                materials = collection.find().sort(sort_cond)
            else:
                materials = collection.find()
        else:
            sort_cond['__search_score'] = {'$meta': "textScore"} 
            materials = collection.find(condition).sort(sort_cond)

        df = pd.DataFrame(list(materials))
        count = df.shape[0]
        if  count == 0:
            return Response({'status':'No data found.','data': list(df.columns)},status=status.HTTP_204_NO_CONTENT)
        print(df)
        df['_id'] = df['_id'].astype(str)
        df = df.fillna('')
        df = df.T

        return Response({'status':f'{count} data found.','data': df.to_dict()}, status=status.HTTP_200_OK)
    
    except PyMongoError as e:
        return Response({'error': f'Error retrieving data: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def compare_fields_by(request,):
    try:
        collection = MongoConnection.get_connection().get_database('materials').get_collection('all_materials')
    
        select_field = request.GET.get('field')
        comp = request.GET.get('comp')
        field_value = request.GET.get('value')
        
        if select_field and field_value:
            query = {}
            if comp == '=':
                search_comp = '$eq'
            elif comp == '>':
                search_comp = '$gt'
            elif comp == '>=':
                search_comp = '$gte'
            elif comp == '<':
                search_comp = '$lt'
            elif comp == '<=':
                search_comp = '$lte'
            elif comp == '!=':
                search_comp = '$ne'
            else:
                return Response({'error':' Someting Missing please check  comp ( = , < , <= , > , >= , != )'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':' Someting Missing please check field, comp, value'},status=status.HTTP_400_BAD_REQUEST)
        
    
        search_query = {search_comp:int(field_value)}
        query[select_field] = search_query
        print(query)
        materials = collection.find(query)
        df = pd.DataFrame(list(materials))

        count = df.shape[0]
        if  count == 0:
            return Response({'status':'No data found.','data': list(df.columns)},status=status.HTTP_204_NO_CONTENT)
        
        df['_id'] = df['_id'].astype(str)
        df = df.fillna('')
        df = df.T
        return Response({'status':f'{count} data found.','data': df.to_dict()}, status=status.HTTP_200_OK)
    
    except PyMongoError as e:
        return Response({'error': f'Error retrieving data: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def boolen_filter_(request,field,value):
    try:
        collection = MongoConnection.get_connection().get_database('materials').get_collection('all_materials')
        print(field,value)
        value = value.lower()
        if value in ('true',1):
            query_com = '$exists'
        else:
            query_com ='$ne'
        query = {field:{query_com:True}}
        materials =collection.find(query)
        df = pd.DataFrame(list(materials))
        count = df.shape[0]
        if  count == 0:
            return Response({'status':'No data found.','data': list(df.columns)},status=status.HTTP_204_NO_CONTENT)
        
        df['_id'] = df['_id'].astype(str)
        df = df.fillna('')
        df = df.T
        return Response({'status':f'{count} data found.','data': df.to_dict()}, status=status.HTTP_200_OK)
    
    except PyMongoError as e:
        return Response({'error': f'Error retrieving data: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def validate_field_(request,fields):
    try:
        collection = MongoConnection.get_connection().get_database('materials').get_collection('all_materials')
        if not fields:
            _dict = dict()
            material =collection.find_one()
            if material is None:
                return Response({'error': f'Error retrieving data: '}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            fields= list(material.keys())
            for field in fields:
                _dict[field] = str(type(material[field]))
            return Response({'status':'list of all column with datatypes','datatypes':_dict},status=status.HTTP_204_NO_CONTENT)
 
        material= collection.find_one()
        field_type =dict()
        for field in fields.split(','):
            field_type[field] = str(type(material[field]))
        return Response({'status':'Field of specific field.','datatype':field_type}, status=status.HTTP_200_OK)

    except PyMongoError as e:
        return Response({'error': f'Error retrieving data: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def search_text_(request):
    try:
        collection = MongoConnection.get_connection().get_database('materials').get_collection('all_materials')
        sub_string = request.GET.get('string')
        search_query = {'$text':{'$search':sub_string}}
        materials = collection.find(search_query)
        df = pd.DataFrame(list(materials))

        count = df.shape[0]
        if  count == 0:
            return Response({'status':'No data found.','data': list(df.columns)},status=status.HTTP_204_NO_CONTENT)
        
        df['_id'] = df['_id'].astype(str)
        df = df.fillna('')
        df = df.T
        return Response({'status':f'{count} data found.','data': df.to_dict()}, status=status.HTTP_200_OK)

    except PyMongoError as e:
        return Response({'error': f'Error retrieving data: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
