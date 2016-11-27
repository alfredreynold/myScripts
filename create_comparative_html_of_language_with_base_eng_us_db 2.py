# -*- coding: utf-8 -*-
import re,time
import codecs
import zpicmodedict_to_uwd


def read_uwdict(filepath):
    f = codecs.open(filepath,'r', encoding='utf-8')
    n = f.readlines()
    uwdict = [re.match('\[(.*)\].*\(LEX=(.*), ABT=.*POS=(.*), LST=.*MOR=(.*), NUM=(.*), PAR=, IMG=(.*), AUDIO=(.*),.*CID=(.*), PARENT=(.*), AS', l).groups() for l in n]
    # print len(uwdict)
    return uwdict

def getTagName(uwdict, cId):
    z = [m[0] for m in uwdict if m[-2] == cId]
    #print z
    if(len(z) >= 1):
        z = z[0]
    else:
        print "no record found? ", cId
        z = ""
    return z

def getPicture(uwdict, cid):
    for u in uwdict:
        if u[-2] == cid:
            return u[5]
    return ''

def getAudioData(uwdict, cid):
    for u in uwdict:
        if u[-2] == cid:
            #print 'POS Empty =', u
            return u[6] 
    return ''

def getPOSValue(uwdict, cid):
    for u in uwdict:
        if u[-2] == cid:
            #print 'POS Empty =', u
            return u[3]  
    return ''
def getParentId(uwdict, cid):
    for u in uwdict:
        if u[-2] == cid:
            return u[-1]
    print 'Error getting parent id for ', cid

def identifierExists(uwdict, cid):
    for u in uwdict:
        if u[-2] == cid:
            return True
    return False

def getBreadcrumb(uwdict, identifier):
    if (identifier == str(0)):
        return ''
    else:
        parentId = getParentId(uwdict,identifier)
        if parentId == None:
            print identifier
            return getTagName(uwdict, identifier)

        return (getBreadcrumb(uwdict, parentId) + ' -> ' + getTagName(uwdict, identifier))


def make_list(parent, indent=0):
    global uwd_lang, uwd_english, pos, linenum, destfile



    z = [m for m in uwd_lang if m[-1] == parent]

    for k in z:
        print "alfee  ",k
        margin = indent*INDENT_WIDTH
        linenum = linenum+1
        # to do breadcrumbs
        
        tagname = k[0]
        parent_id = k[-1]
        parent_category = getBreadcrumb(uwd_lang,k[-1])[4:] #getTagName(uwd, k[-1])
        picture = k[5]
        audio_data = k[6]
        pos_value = k[3]
        pos_class = pos[pos_value.strip()]
        identifier = k[-2]


        data_label_changed = ''
        data_picture_changed = ''
        data_pos_changed = ''
        data_audio_changed = ''
        data_parent_changed = ''
        changed_flag = False
        changed_class = ''
        added_class = ''
        is_deleted_class = ''

        if identifierExists(uwd_english,identifier) == False:
            added_class = 'added'

        tagname = tagname.replace("'",'&#39;')

        if pos_value == '':
            pos_class = pos[getPOSValue(uwd_english,k[-2])]
        #indent, posclass, picture path, posvalue
        # *******************************************************************************************************

        if "ci_" in picture:
            picture = "spanish_custom_images/" + picture

        # *******************************************************************************************************

        htmlStr = "<div class='element' style='margin-left:%spx'><img class='lazy symbol %s' xxsrc='loading.gif' data-original='png/%s'/>" %(margin, pos_class, picture)
        #linenum tagname parent/breadcrumb, pos_value
        htmlStr = htmlStr + "<div class='content %s %s %s' data-identifier='%s' data-label-changed='%s' data-picture-changed='%s' data-pos-changed='%s' data-audio-changed='%s' data-parent-changed='%s'><span class='sequence'>%s. </span><span class='tagname'>%s</span><span class='breadcrumbs'> (under <b>%s</b> category)</span><span class='partofspeech'> POS = %s</span>" %(pos_class, changed_class,added_class,identifier, data_label_changed,data_picture_changed,data_pos_changed,data_audio_changed,data_parent_changed, str(linenum), tagname, parent_category,pos_value)

        english_tagname = getTagName(uwd_english, k[-2])
        english_parent_category = getBreadcrumb(uwd_english, k[-1])[4:]
        english_pos_value = getPOSValue(uwd_english,k[-2])
        english_picture = getPicture(uwd_english,k[-2])


        #linenum eng_tagname eng_parent/breadcrumb, pos_value
        
        htmlStr = htmlStr + "<div class='translated-content'><span class='sequence'>%s. </span><span class='tagname'>%s</span><span class='breadcrumbs'> (under %s category)</span><span class='partofspeech'> POS = %s</span></div>" %(str(linenum), english_tagname, english_parent_category,english_pos_value)
        
        if len(added_class) != 0:
            htmlStr = htmlStr + "</div><div class='added-tag'>Added<div class='edit-blog' ><button class = 'edit_button btn btn-default' data-toggle='popover' title='Edit' data-content='' edit-data-identifier='%s'>Edit</button></div></div></div>\n"%(identifier)
            # htmlStr = htmlStr + "<div class='edit-blog' ><button class = 'edit_button btn btn-default' data-toggle='popover' title='Edit' data-content='' edit-data-identifier='%s'>Edit</button></div>\n"%(identifier)
        elif len(changed_class) != 0:
            htmlStr = htmlStr + "</div><div class='modified-tag'>Modified<div class='edit-blog' ><button class = 'edit_button btn btn-default' data-toggle='popover' title='Edit' data-content='' edit-data-identifier='%s'>Edit</button></div></div></div>\n"%(identifier)
            # htmlStr = htmlStr + "<div class='edit-blog' ><button class = 'edit_button btn btn-default' data-toggle='popover' title='Edit' data-content='' edit-data-identifier='%s'>Edit</button></div>\n"%(identifier)
        else:
            htmlStr = htmlStr + "</div><div class='edit-blog' ><button class = 'edit_button btn btn-default' data-toggle='popover' title='Edit' data-content='' edit-data-identifier='%s'>Edit</button></div></div>\n"%(identifier)

        destfile.write(htmlStr+'\n')
        
        make_list(k[-2], indent+1)

# def deleted_items():
#     global uwd_v1, uwd_v2, uwd_english, pos, destfile
#     ctr = 0
#     for k in uwd_v1:
#         if identifierExists(uwd_v2, k[-2]) is False:
#             deleted_class = 'deleted'
#             tagname = k[0]
#             parent_id = k[-1]
#             parent_category = getBreadcrumb(uwd_v2,k[-1])[4:]
#             picture = k[4]
#             audio_data = k[5]
#             pos_value = getPOSValue(uwd_v2,k[-2])
#             pos_class = pos[pos_value.strip()]
#             identifier = k[-2]

#             data_label_changed = ''
#             data_picture_changed = ''
#             data_pos_changed = ''
#             data_audio_changed = ''
#             data_parent_changed = ''
#             deleted_class = 'deleted'
#             added_class = ''
#             ctr = ctr + 1
#             margin = '0'

#             #indent, posclass, picture path, posvalue
#             htmlStr = "<div class='element' style='margin-left:%spx clear:both'><img class='lazy symbol %s' xxsrc='loading.gif' data-original='png/%s'/>" %(margin, pos_class, picture)
#             #linenum tagname parent/breadcrumb, pos_value
#             htmlStr = htmlStr + "<div class='content %s %s' data-identifier='%s' data-label-changed='%s' data-picture-changed='%s' data-pos-changed='%s' data-audio-changed='%s' data-parent-changed='%s'><span class='sequence'>%s. </span><span class='tagname'>%s</span><span class='breadcrumbs'> (under <b>%s</b> category)</span><span class='partofspeech'> POS = %s</span>" %(deleted_class,added_class,identifier, data_label_changed,data_picture_changed,data_pos_changed,data_audio_changed,data_parent_changed, str(ctr), tagname, parent_category,pos_value)

#             english_tagname = getTagName(uwd_english, k[-2])
#             english_parent_category = getBreadcrumb(uwd_english, k[-1])[4:]
#             english_pos_value = getPOSValue(uwd_english,k[-2])
#             english_picture = getPicture(uwd_english,k[-2])


#             #linenum eng_tagname eng_parent/breadcrumb, pos_value
            
#             htmlStr = htmlStr + "<div class='translated-content'><span class='sequence'>%s. </span><span class='tagname'>%s</span><span class='breadcrumbs'> (under %s category)</span><span class='partofspeech'> POS = %s</span></div>" %(str(linenum), english_tagname, english_parent_category,english_pos_value)
#             htmlStr = htmlStr + "</div><div class='deleted-tag'>DELETED</div></div>"
#             destfile.write(htmlStr+'\n')

def create_html(uwdict_filepath_eng, uwdict_filepath_lang, dest_htmlfile):
    ''' pass me a US uwdict file and diff lang one and I will generate a html file with comparative view
    '''

    global uwd_lang, uwd_english, linenum,INDENT_WIDTH, IMG_WIDTH,IMG_HEIGHT, destfile, pos

    linenum = 0
    #pos = {"verb":"green", "adjective":"blue", "phrases":"pink", "noun":"orange", "questions and time": "grey","short words":"brown", "people":"yellow", "place":"purple", "":"black", 'None':'black'}
    pos = {"verb":"green", "adjective":"blue","phrase":"pink", "noun":"orange","others":"black", "":"black", 'None':'black'}
    destfile = codecs.open(dest_htmlfile,'w', encoding='utf-8')

    destfile.write('<!DOCTYPE HTML> \n<html>\n<head><meta charset="UTF-8"><link rel="StyleSheet" href="css/bootstrap.min.css" type="text/css"><link rel="StyleSheet" href="css/stylesheet.css" type="text/css"></head><body><div id="submit2div" align = "left"><button class="btn btn-success" id="submit">Submit</button></div>\n')
    INDENT_WIDTH = 40
    IMG_WIDTH = '70px'
    IMG_HEIGHT = '60px'
    
    uwd_lang = read_uwdict(uwdict_filepath_lang)
    uwd_english = read_uwdict(uwdict_filepath_eng)
    make_list('0')
    # deleted_items()

    js_str = '<script src="js/jquery.js" type="text/javascript"></script>\n'
    js_str = js_str + '<script src="js/bootstrap.min.js" type="text/javascript"></script> \n'
    js_str = js_str + '<script src="js/tooltip.js" type="text/javascript"></script> \n'
    js_str = js_str + '<script src="js/jquery.scrollstop.js" type="text/javascript"></script> \n'
    js_str = js_str + '<script src="js/jquery.lazyload.js" type="text/javascript"></script> \n'
    js_str = js_str + '<script src="js/edit_script1.js" type="text/javascript"></script> \n'
    js_str = js_str + '<script src="js/bootbox.min.js" type="text/javascript"></script>\n'
    js_str = js_str + '<script src="js/index.js" type="text/javascript"></script>'

    destfile.write(js_str+'</body>\n</html>')
    destfile.close()

    #print getBreadcrumb(uwd, '100')

def run(sqlite_eng, sqlite_lang, dest_htmlfile):
    zpicmodedict_to_uwd.run(sqlite_lang,'lang_uwd.txt')
    zpicmodedict_to_uwd.run(sqlite_eng,'english_uwd.txt')
    create_html('english_uwd.txt','lang_uwd.txt',dest_htmlfile)

run('/Users/alfredreynold/Documents/forBuild/Proj/Lang/English/Database/User-Data.sqlite','/Users/alfredreynold/Documents/forBuild/Proj/Lang/English/Database/User-Data.sqlite','/Users/alfredreynold/Documents/Alfred/Dev/avaz_collaborate/Ter_DB_2015.html')


