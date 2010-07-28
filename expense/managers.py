# -*- coding: utf-8 -*-
from django.db import models

class SubExpendTypeManager(models.Manager):
    
    def of(self, parent):
        """
        Get all expend types with parent passed by parameter 
        @param parent: ExpendType object
        @return: list(ExpendType objects) 
        """
        return super(SubExpendTypeManager, self).get_query_set().filter(parent=parent)
        
