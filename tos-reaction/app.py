import logging

import flask
from flask import Flask,request
from parserlib.utils.luautilmod import luaclass
from parserlib.parserr.parser_enums import *
from parserlib.constantsmod import constclass
from flask import Request
import json
app = Flask(__name__)

luas={}
consts={}
DEBUG_MODE=True
if not DEBUG_MODE:
    regions=[
        TOSRegion.iTOS,
        TOSRegion.jTOS,
        TOSRegion.kTOS,
        TOSRegion.twTOS,
        TOSRegion.kTEST
    ]
else:
    regions = [
        TOSRegion.jTOS,
    ]

for region in regions:
    try:
        const = constclass(region)
        lua = luaclass(const)
        lua.init()
        luas[region] = lua
        consts = []
    except Exception as e:
        logging.error(str(e))

@app.route('/reaction/lua',methods=['GET','POST'])
def invokelua():
    acceptablemode={
        'SkillFactor':'SkillFactor',
        'SpendSP':"SpendSP",
        'SP':'SpendSP',
        'CoolDown':"CoolDown",
        "SkillSR":"SkillSR",
        "CaptionRatio":"CaptionRatio",
        "CaptionRatio2": "CaptionRatio2",
        "CaptionRatio3": "CaptionRatio3",
        "CaptionTime":"CaptionTime",
        "SpendItemCount":"SpendItemCount",
        "Unlock":"Unlock",
    }
    data = request.get_data().decode('utf-8')
    data = json.loads(data)


    context=data['context']
    mode=data['mode']
    region=TOSRegion.value_of(data['region'])
    classid=data['classid']
    luatype=data['type']
    if region is None:
        logging.error("Region is not selected.")
        return 'fail'
    if mode not in acceptablemode:
        logging.error("Invalid Mode"+mode)
        return 'fail'
    mode=acceptablemode[mode]
    # search function
    lua=luas[region]
    preverb=''
    if luatype=='skill':
        ies=lua.lua.execute("return GetClassByType('Skill',"+classid+")")
        preverb="GetSkill"
        logging.debug("Skill" + str(classid))
    elif luatype=='ability':
        ies = lua.lua.execute("return GetClassByType('Ability'," + classid + ")")
        preverb = "GetAbility"
        logging.debug("Ability"+str(classid))
    if ies is None:
        logging.error("IES not found :"+classid)
        return 'fail'

    func=ies[mode]

    if func is None:
        logging.error("Func not found :" + classid)
        return 'fail'
    fn_str="return function(obj) \n" \
           "  return "+func+"(obj"+""+")\n" \
           "end"

    # call lua
    # arg_fn="return function() \n" \
    #        "  return "+preverb+"(nil,'"+ies["ClassName"]+"') \n" \
    #        "end"
    arg_fn="  return "+preverb+"(context,'"+ies["ClassName"]+"')"

    result,retval=lua.exec_lua_encapsulated(ies,context,fn_str,arg_fn)
    if result==False:
        # fail
        logging.error("Lua Failed :" + retval)
        return 'fail'

    obj={
        "result":retval
    }

    return str(retval)
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':

    app.run()

