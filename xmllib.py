

def xmlfind(keystr,rawdata, begin,stop):
    xmlkey_begin = begin
    xmlkey_end = begin
    xmlkey_begin = rawdata.find('<' + keystr + '>',begin,stop) + len('<' + keystr + '>')
    xmlkey_end = rawdata.find('</' + keystr +'>',begin,stop)
    if xmlkey_end < 20:
        metardata = 0
    else:
        metardata = rawdata[xmlkey_begin:xmlkey_end]
    return (metardata)
