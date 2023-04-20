from rest_framework.permissions import BasePermission 


class IsManager(BasePermission):
    
    '''
    Allows access only Manager  
        '''
    def has_permission(self, request, view):
       
         if request.user.role == 'M':
        
             return True
         
class IsCustomer(BasePermission):
    
    '''
    Allows access only Customer  
        '''
    def has_permission(self, request, view):
       
         if request.user.role == 'C':
        
             return True