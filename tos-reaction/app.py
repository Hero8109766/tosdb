import logging

import flask
from flask import Flask
from parserlib.utils.luautilmod import luaclass
from parserlib.parserr.parser_enums import *
from parserlib.constantsmod import constclass
from flask import Request
import json
app = Flask(__name__)

luas={}
consts={}
regions=[
    TOSRegion.iTOS,
    TOSRegion.jTOS,
    TOSRegion.kTOS,
    TOSRegion.twTOS,
    TOSRegion.kTEST
]

@app.route('/reaction/lua',methods=['GET','POST'])
def invokelua():
    acceptablemode=[
        'SkillFactor',
        'SpendSP',
        'CoolDown'
    ]
    context=json.loads(Request.form['context'])
    mode=Request.form['mode']
    region=TOSRegion.value_of(Request.form['region'])
    classid=Request.form['classid']
    stats=json.loads(Request.form['stats'])
    if region is None:
        logging.error("Region is not selected.")
        return 'fail'
    if mode not in acceptablemode:
        logging.error("Invalid Mode"+mode)
        return 'fail'

    # search function
    lua=luas[region]
    ies=lua.lua.eval("return GetClassByID('Skill',"+classid+")")
    if ies is None:
        logging.error("IES not found :"+classid)
        return 'fail'

    func=ies[mode]

    if func is None:
        logging.error("Func not found :" + classid)
        return 'fail'


    # call lua
    result,retval=luas[region].exec_lua_encapsulated(
        lua.exec_lua_encapsulated(context,func,"GetSkill("+ies.ClassName+")")
    )
    if result==False:
        # fail
        logging.error("Lua Failed :" + retval)
        return 'fail'

    obj={
        "result":retval
    }

    return json.dumps(obj)
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    for region in regions:
        const=constclass(region)
        lua=luaclass(const)
        lua.init()
        luas[region]=lua
        consts=[]
    app.run()

