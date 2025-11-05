# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__all__ = [
    'TTkTimeProperties',
    'TTkDateProperties',
    'TTkDateTimeProperties',
    'TTkDateFormProperties'
    ]

import datetime

from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.menu import TTkMenuButton
from TermTk.TTkWidgets.datetime_time import TTkTime
from TermTk.TTkWidgets.datetime_date import TTkDate
from TermTk.TTkWidgets.datetime_datetime import TTkDateTime
from TermTk.TTkWidgets.datetime_date_form import TTkDateForm

TTkTimeProperties = {
    'properties'  : {
        'Time' : {
                'init': {'name':'time',        'type':datetime.time } ,
                'get':  { 'cb':TTkTime.time,   'type':datetime.time } ,
                'set':  { 'cb':TTkTime.setTime,'type':datetime.time } },
    },'signals' : {
        'timeChanged(datetime.time)' : {'name':'timeChanged',  'type':datetime.time},
    },'slots' : {
        'setTime(datetime.time)'     : {'name':'setTime',      'type':datetime.time},
    }
}

TTkDateProperties = {
    'properties'  : {
        'Date' : {
                'init': {'name':'date',        'type':datetime.date } ,
                'get':  { 'cb':TTkDate.date,   'type':datetime.date } ,
                'set':  { 'cb':TTkDate.setDate,'type':datetime.date } },
    },'signals' : {
        'dateChanged(datetime.date)' : {'name':'dateChanged',  'type':datetime.date},
    },'slots' : {
        'setDate(datetime.date)'     : {'name':'setDate',      'type':datetime.date},
    }
}

TTkDateFormProperties = {
    'properties'  : {
        'Date' : {
                'init': {'name':'date',        'type':datetime.date } ,
                'get':  { 'cb':TTkDateForm.date,   'type':datetime.date } ,
                'set':  { 'cb':TTkDateForm.setDate,'type':datetime.date } },
    },'signals' : {
        'dateChanged(datetime.date)' : {'name':'dateChanged',  'type':datetime.date},
    },'slots' : {
        'setDate(datetime.date)'     : {'name':'setDate',      'type':datetime.date},
    }
}

TTkDateTimeProperties = {
    'properties'  : {
        'DateTime' : {
                'init': {'name':'datetime',        'type':datetime.datetime } ,
                'get':  { 'cb':TTkDateTime.datetime,   'type':datetime.datetime } ,
                'set':  { 'cb':TTkDateTime.setDatetime,'type':datetime.datetime } },
    },'signals' : {
        'datetimeChanged(datetime.datetime)' : {'name':'datetimeChanged',  'type':datetime.datetime},
    },'slots' : {
        'setDatetime(datetime.datetime)'     : {'name':'setDatetime',      'type':datetime.datetime},
    }
}