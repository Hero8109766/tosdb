import logging

import flask
from flask import Flask, request
from parserlib.utils.luautilmod import luaclass
from parserlib.parserr.parser_enums import *
from parserlib.constantsmod import constclass
from flask import Request
import json

app = Flask(__name__)

luas = {}
consts = {}
DEBUG_MODE = False
if not DEBUG_MODE:
    regions = [
        TOSRegion.iTOS,
        TOSRegion.jTOS,
        TOSRegion.kTOS,
        TOSRegion.twTOS,
        TOSRegion.kTEST
    ]
else:
    regions = [
        TOSRegion.kTEST,
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
        raise e


@app.route('/reaction/lua', methods=['GET', 'POST'])
def invokelua():
    acceptablemode = {
        'SkillFactor': 'SkillFactor',
        'SpendSP': "SpendSP",
        'SP': 'SpendSP',
        'CoolDown': "CoolDown",
        "SkillSR": "SkillSR",
        "CaptionRatio": "CaptionRatio",
        "CaptionRatio2": "CaptionRatio2",
        "CaptionRatio3": "CaptionRatio3",
        "CaptionTime": "CaptionTime",
        "SpendItemCount": "SpendItemCount",
        "Unlock": "Unlock",
        "!RelicReleaseOptions": "!RelicReleaseOptions",
        "!RelicByLevel": "!RelicByLevel",

    }

    data = request.get_data().decode('utf-8')
    data = json.loads(data)

    context = data['context']
    mode = data['mode']
    region = TOSRegion.value_of(data['region'])
    classid = str(int(data['classid']))
    iestype = data['type'].lower()
    arg = data['arg'] if "arg" in data else None
    arg2 = data['arg2'] if "arg2" in data else None

    if region is None:
        logging.error("Region is not selected.")
        return 'fail'
    if mode not in acceptablemode:
        logging.error("Invalid Mode" + mode)
        return 'fail'
    mode = acceptablemode[mode]
    # search function
    lua = luas[region]
    preverb = ''
    if iestype == 'skill':
        ies = lua.lua.execute("return GetClassByType('Skill'," + (classid) + ")")
        preverb = "GetSkill"
        logging.debug("Skill" + str(classid))
    elif iestype == 'ability':
        ies = lua.lua.execute("return GetClassByType('Ability'," + (classid) + ")")
        preverb = "GetAbility"
        logging.debug("Ability" + str(classid))
    elif iestype == 'item':
        ies = lua.lua.execute("return GetClassByType('Item'," + (classid) + ")")
        preverb = ""
        logging.debug("Ability" + str(classid))
    if ies is None:
        logging.error("IES not found :" + classid)
        return 'fail'
    func = None
    if mode == '!RelicReleaseOptions':
        fn_str = \
            '''
            return function(obj,arg)
                local msgstr = string.format('RelicGem_%s_DescText', arg)
                local strInfo = ClMsg(msgstr)
                return strInfo
            end
            '''
    elif mode == '!RelicByLevel':
        fn_str = \
            '''
            return function(obj,arg,arg2)
                local s=""
                local option_text_format = 'RelicOptionLongText%s'
                for i=1 , max_relic_option_count do
                    local func_str = string.format('get_tooltip_%s_arg%d', arg, i) 
                    local tooltip_func = _G[func_str]
                    if tooltip_func ~= nil then
                        local value, name, interval, type = tooltip_func()
                        local total = value * math.floor(arg2 / interval)
                        local msg = string.format(option_text_format, type)
                        local strInfo = ScpArgMsg(msg, 'name', ClMsg(name), 'total', total, 'interval', interval, 'value', value)

                        s=s .. strInfo ..'{nl}'
                    end

                end
                return s
            end
            '''
    else:
        func = ies[mode]

        if func is None:
            logging.error("Func not found :" + classid)
            return 'fail'
        fn_str = "return function(obj) \n" \
                 "  return " + func + "(obj" + "" + ")\n" \
                                                    "end"
    if (preverb):
        arg_fn = "return " + preverb + "(context,'" + ies["ClassName"] + "')"
        result, retval, r2, r3, r4 = lua.exec_lua_encapsulated(ies, context, fn_str, arg_fn, None)
    else:
        result, retval, r2, r3, r4 = lua.exec_lua_encapsulated(ies, context, fn_str, None, arg,arg2)
    if result == False:
        # fail
        logging.error("Lua Failed :" + str(retval))
        return 'fail'

    obj = {
        "result": retval,
        "r2": r2,
        "r3": r3,
        "r4": r4
    }

    return obj


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
