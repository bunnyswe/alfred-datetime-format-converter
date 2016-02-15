# -*- coding: utf-8 -*-

import alfred
import calendar
from delorean import utcnow, now, parse, epoch

def process(query_str):
    """ Entry point """
    value = parse_query_value(query_str)
    if value is not None:
        results = alfred_items_for_value(value)
        xml = alfred.xml(results,len(results)) # compiles the XML answer
        alfred.write(xml) # writes the XML back to Alfred

def parse_query_value(query_str):
    """ Return value for the query string """
    try:
        query_str = str(query_str).strip('"\' ')
        if query_str == 'now':
            d = now()
        else:
            # Parse datetime string or timestamp
            try:
                d = epoch(float(query_str))
            except ValueError:
                d = parse(str(query_str))
    except (TypeError, ValueError):
        d = None
    return d

def alfred_items_for_value(value):
    """
    Given a delorean datetime object, return a list of
    alfred items for each of the results
    """

    index = 0
    results = []
    value.shift('Asia/Chongqing')
    # First item as timestamp
    item_value = calendar.timegm(value.datetime.utctimetuple())
    results.append(alfred.Item(
        title=str(item_value),
        subtitle=u'UTC Timestamp',
        attributes={
            'uid': alfred.uid(index), 
            'arg': item_value,
        },
        icon='icon.png',
    ))
    index += 1

    item_value = calendar.timegm(value.datetime.timetuple())
    results.append(alfred.Item(
        title=str(item_value),
        subtitle=u'Local Timestamp',
        attributes={
            'uid': alfred.uid(index), 
            'arg': item_value,
        },
        icon='icon.png',
    ))
    index += 1

    # Various formats
    formats = [
        # 19370101
        ("%Y%m%d", "%Y%m%d"),
        # 120027
        ("%H%M%S", "%H%M%S"),
        # 19370101 120027
        ("%Y%m%d %H%M%S", "%Y%m%d %H%M%S"),
        # 19370101120027000000
        ("%Y%m%d%H%M%S%f", "%Y%m%d%H%M%S%f"),
        # 1937-01-01 12:00:27
        ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"),
        # Sun, May 19 2002 15:21:36
        ("%a, %b %d %Y %H:%M:%S", "%a, %d %b %Y %H:%M:%S"), 
        # 1996-12-19T16:39:57-0800
        ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S%z"),
        # local
        ("%x %X", "Local Time"),
    ]
    for format, description in formats:
        item_value = value.datetime.strftime(format)
        results.append(alfred.Item(
            title=str(item_value),
            subtitle=description,
            attributes={
                'uid': alfred.uid(index), 
                'arg': item_value,
            },
        icon='icon.png',
        ))
        index += 1

    return results

if __name__ == "__main__":
    try:
        query_str = alfred.args()[0]
    except IndexError:
        query_str = None
    process(query_str)
