from rest_framework.permissions import BasePermission 
from rest_framework.permissions import SAFE_METHODS

class IsManager(BasePermission):
    
    '''
    Allows access only Manager  
        '''
    def has_permission(self, request, view):
       
         if request.user.role == 'M':
        
             return True
         
class IsManagerOrSafeMethod(BasePermission):
    def has_permission(self, request, view):
       
        if request.user.role == 'M' or request.meethod in SAFE_METHODS:
            return True
        else:
            return False
    
         
class IsCustomer(BasePermission):
    
    '''
    Allows access only Customer  
        '''
    def has_permission(self, request, view):
       
         if request.user.role == 'C':
        
             return True