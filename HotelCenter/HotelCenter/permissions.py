from rest_framework.permissions import BasePermission 


class IsManager(BasePermission):
    
    '''
    Allows access only Manager  
        '''
    def has_permission(self, request, view):
       
         if request.user.role == 'M':
        
             return True