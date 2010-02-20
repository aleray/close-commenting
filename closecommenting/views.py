# *-* encoding: utf-8 *-*

## Copyright 2010 Stéphanie Vilayphiou, Alexandre Leray

## This file is part of Close Commenting.
## 
## Close Commenting is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
## 
## Close Commenting is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with Close Commenting.  If not, see <http://www.gnu.org/licenses/>.


from django.views.generic import list_detail
from models import Text

def text_detail(request, slug):
    """
    Returns a text
    """
    view = request.GET.get('view', 'unfold'), 
    # cp = int(request.GET['cp']) if 'cp' in request.GET else None
    # cc = int(request.GET['cc']) if 'cc' in request.GET else None
    
    # cp = comment of a paragraph
    cp = request.GET.get('cp', None)
    try: cp = int(cp)
    except: pass
    # cc = comment of a comment
    cc = request.GET.get('cc', None)
    try: cc = int(cc)
    except: pass
    # ct = comment of a text
    ct = request.GET.get('ct', None)
    try: ct = int(ct)
    except: pass
    
    return list_detail.object_detail(
        request, 
        queryset = Text.objects.all(),
        slug = slug,
        slug_field = 'dc_identifier',
        template_name = 'closecommenting/text.html',
        template_object_name = 'text',
        extra_context = {
            'view': view, 
            'cp': cp, 
            'cc': cc, 
            'ct': ct, 
        }
    )
