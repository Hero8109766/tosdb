import csv
import os
import re
import codecs
from lupa import LuaRuntime, LuaError
import logging
import constants
from utils import iesutil


# HotFix: don't throw errors when LUA is getting an unknown key
def attr_getter(obj, name):
    if name in obj:
        if name in ['Blockable', 'HPCount', 'ReinforceArmor', 'TranscendArmor', 'ReinforceWeapon', 'TranscendWeapon']:
            return int(obj[name])
        else:
            return obj[name]
    return 0


def attr_setter(obj, name, value):
    obj[name] = value


lua = LuaRuntime(attribute_handlers=(attr_getter, attr_setter), unpack_returned_tuples=True)

LUA_OVERRIDE = [
    'function GET_ITEM_LEVEL(item) return 0 end',  # We cant emulate this function as geItemTable is undefined
    'function IsBuffApplied(pc, buff) return "NO" end',
    'function GetAbilityAddSpendValue(pc,classname,column) return 0 end',
    'function GetSkillOwner(skill) return {} end',
    'function IsServerSection(pc) return 0 end',
    'function GetExProp(entity, name) return entity[name] end',
    'function GetExProp_Str(entity, name) return tostring(entity[name]) end',
    'function GetIESID(item) end',
    'function GetItemOwner(item) return {} end',
    'function GetOwner(monster) end',
    'function GetServerNation() end',
    'function GetServerGroupID() end',
    'function IsPVPServer(itemOwner) end',
    'function IMCRandom(min, max) return 0 end',
    'function ScpArgMsg(a, b, c) return "" end',
    'function SCR_MON_OWNERITEM_ARMOR_CALC(self, defType) return 0 end',
    'function SetExProp(entity, name, value) entity[name] = value end',
    'function math.pow(value,power) return value ^ power end',
    'function GetZoneName() return "" end',
    "function Weeklyboss_GetNowWeekNum() return nil end",
    "function GetBuffByProp(self,mode,value) return nil end",
    "function IsRaidField(self)return 0 end",
    "function IsJoinColonyWarMap(self)return 0 end",
    "function IsPvPMineMap(self)return 0 end",
    "function SCR_MON_OWNERITEM_ARMOR_CALC(self) return 0 end",


]

LUA_RUNTIME = None
LUA_SOURCE = None


def init():
    init_global_constants('sharedconst.ies')
    init_global_constants('sharedconst_system.ies')
    init_global_data()
    init_global_functions()
    init_runtime()
    init_global_functions()

    pass

def init_global_constants(ies_file_name):
    execute = ''
    ies_path = os.path.join(constants.PATH_INPUT_DATA, 'ies.ipf', ies_file_name)

    with codecs.open(ies_path, 'r','utf-8',errors="replace") as ies_file:
        for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
            if row['UseInScript'] == 'NO':
                continue

            execute += row['ClassName'] + ' = ' + row['Value'] + '\n'

    lua.execute(execute)


def init_global_data():

    ies_ADD = lua.execute('''
        ies_by_ClassID = {}
        ies_by_ClassName = {}
        ies_by_ClassIDCount = {}
        ies_by_ClassNameCount = {}
        
        function ies_ADD(key, data)
            _by_ClassID = {}
            _by_ClassName = {}
            _by_ClassIDCount=0
            _by_ClassNameCount=0
            key=string.lower(key)
            if ies_by_ClassID[key] ~= nil then
                _by_ClassID = ies_by_ClassID[key]
            end
            if ies_by_ClassName[key] ~= nil then
                _by_ClassName = ies_by_ClassName[key]
            end
            if ies_by_ClassID[key] ~= nil then
                _by_ClassIDCount = ies_by_ClassIDCount[key]
            end
            if ies_by_ClassName[key] ~= nil then
                _by_ClassNameCount = ies_by_ClassNameCount[key]
            end
            for i, row in python.enumerate(data) do
                _by_ClassID[math.floor(row["ClassID"])] = row
                _by_ClassName[row["ClassName"]] = row
                _by_ClassIDCount=_by_ClassIDCount+1
                _by_ClassNameCount=_by_ClassNameCount+1
            end
            
            ies_by_ClassID[key] = _by_ClassID
            ies_by_ClassName[key] = _by_ClassName
            ies_by_ClassIDCount[key] = _by_ClassIDCount
            ies_by_ClassNameCount[key] = _by_ClassNameCount
        end
        
        return ies_ADD
    ''')

    ies_ADD('ancient', iesutil.load('ancient_info.ies'))
    ies_ADD('ancient_info', iesutil.load('ancient_info.ies'))
    ies_ADD('clientmessage', iesutil.load('clientmessage.ies'))
    ies_ADD('item', iesutil.load('item_equip.ies'))
    ies_ADD('itemtranscend', iesutil.load('item_transcend.ies'))
    ies_ADD('item', iesutil.load('item_equip_ep12.ies'))
    ies_ADD('item', iesutil.load('item_ep12.ies'))
    ies_ADD('item', iesutil.load('item_HiddenAbility.ies'))
    ies_ADD('item', iesutil.load('item_GuildHousing.ies'))
    ies_ADD('item', iesutil.load('item_ep12.ies'))
    ies_ADD('item', iesutil.load('item_gem.ies'))
    ies_ADD('item', iesutil.load('item_event.ies'))
    ies_ADD('item', iesutil.load('item_event_equip.ies'))
    ies_ADD('item', iesutil.load('item_ep12.ies'))
    ies_ADD('item', iesutil.load('item_premium.ies'))
    ies_ADD('item', iesutil.load('item_quest.ies'))
    ies_ADD('item_grade', iesutil.load('item_grade.ies'))
    ies_ADD('item_growth', iesutil.load('item_growth.ies'))

    ies_ADD('item_goddess_reinforce', iesutil.load('item_goddess_reinforce.ies'))
    ies_ADD('HiddenAbility_Reinforce', iesutil.load('HiddenAbility_Reinforce.ies'))

    ies_ADD('job', iesutil.load('job.ies'))
    ies_ADD('buff', iesutil.load('buff.ies'))
    ies_ADD('monster', iesutil.load('monster.ies'))
    ies_ADD('monster', iesutil.load('monster_guild.ies'))
    ies_ADD('monster', iesutil.load('monster_item_summon.ies'))
    ies_ADD('monster', iesutil.load('monster_item.ies'))
    ies_ADD('monster', iesutil.load('monster_event.ies'))
    ies_ADD('monster', iesutil.load('Monster_solo_dungeon.ies'))
    ies_ADD('monster', iesutil.load('monster_Ancient.ies'))
    ies_ADD('monster', iesutil.load('monster_mgame.ies'))
    ies_ADD('monster', iesutil.load('monster_npc.ies'))


    ies_ADD('stat_monster', iesutil.load('statbase_monster.ies'))
    ies_ADD('stat_monster_race', iesutil.load('statbase_monster_race.ies'))
    ies_ADD('stat_monster_type', iesutil.load('statbase_monster_type.ies'))


def init_global_functions():
    global lua_clmsg
    lua.execute("".join((s+"\n" for s in LUA_OVERRIDE))+'\n\n'+'''
    
        app = {
            IsBarrackMode = function() return false end
        }
        
        exchange = {
            GetExchangeItemInfoByGuid = function(guid) end
        }
      
        geItemTable={
            GetProp=function(item)
                return {
                    GetMaterialExp=function(itemexp)
                        return 0
                    end
                    ,
                    GetLevel=function(itemexp)
                        return 1
                    end,
                    
                }
            end,
        }
        geTime = {
            GetServerSystemTime = function()
                local date = os.date("*t")
                
                return {
                    wDay = date.day,
                    wMonth = date.month,
                    wYear = date.year
                }
            end
        }
        
        session = {
            GetEquipItemByGuid = function(guid) end,
            GetEtcItemByGuid = function(guid) end,
            GetInvItemByGuid = function(guid) end,
            
            link = {
                GetGCLinkObject = function(guid) end
            },
            
            market = {
                GetCabinetItemByItemObjID = function(itemID) end,
                GetItemByItemID = function(itemID) end
            },
            
            otherPC = {
                GetItemByGuid = function(guid) end
            },
            
            pet = {
                GetPetEquipObjByGuid = function(guid) end
            }
        }
        
        
        
        
        
        function GetClassByNumProp(ies_key, column, value)
        
            local data = ies_by_ClassID[string.lower(ies_key)]
            if data==nil then
                return nil
            end
            for id, row in pairs(data) do
                if TryGetProp(row, column) == value then
                    return row
                end
            end
        end
        function string.starts(String,Start)
           return string.sub(String,1,string.len(Start))==Start
        end
        function GetClass(ies_key, name)
            local data = ies_by_ClassName[string.lower(ies_key)]
            return data[name]
        end
        function GetClassByType(ies_key, id)
            if string.starts(ies_key,"item_goddess_reinforce") then
                  local data = ies_by_ClassID[string.lower("item_goddess_reinforce")]
                return data[math.floor(id)]
            end
            local data = ies_by_ClassID[string.lower(ies_key)]
            return data[math.floor(id)]
        end
        
        function GetClassList(ies_key)
            
            local value=ies_by_ClassID[string.lower(ies_key)]
          
            return value,ies_by_ClassIDCount[string.lower(ies_key)]
           
        end
        
        function GetClassCount(ies_key)

            return ies_by_ClassIDCount[string.lower(ies_key)]

        end
        function GetClassByIndexFromList(list,idx)
            return list[idx]
        end
        function GetClassByNameFromList(data, key)
            for id, row in pairs(data) do
                if TryGetProp(row, "ClassName") == key then
                    return row
                end
            end
        end
        
        function MinMaxCorrection(value, min, max)
            if value < min then
                return min
            elseif value > max then
                return max
            else
                return value
            end
        end
        
        -- http://lua-users.org/wiki/SplitJoin @PeterPrade
        function StringSplit(text, delimiter)
           local list = {}
           local pos = 1
           if string.find("", delimiter, 1) then -- this would result in endless loops
              error("delimiter matches empty string!")
           end
           while 1 do
              local first, last = string.find(text, delimiter, pos)
              if first then -- found?
                 table.insert(list, string.sub(text, pos, first-1))
                 pos = last+1
              else
                 table.insert(list, string.sub(text, pos))
                 break
              end
           end
           return list
        end
        
        function SyncFloor(value)
            -- ROUND --
            if(type(value)=='number')then
                value = math.floor((value*1.0)+0.5) / 1.0;
                return(value);
            else
                
                for k,v in pairs(value) do
                    value[k]=SyncFloor(v)
                end
            end
            return value
        end
        
        -- https://stackoverflow.com/a/664557 some LUA table helper functions
        function table.set(t) -- set of list
          local u = { }
          for _, v in ipairs(t) do u[v] = true end
          return u
        end
        function table.find(t, value)
          for k, v in pairs(t) do
            if v == value then
              return k
            end
          end
          return nil
        end
        
        function TryGetProp(item, prop, default)
            if item == nil then
                return default
            end
            
            local value = item[prop]
            
            if tonumber(value) ~= nil then
                return tonumber(value)
            end
            
            if value ~= nil then
                return value
            else
                return default
            end
        end
        
        
    ''' + '\n')




def init_runtime_walk(path):
    blacklist=['lib_math.lua']

    for root, dirs, file_list in os.walk(path):
        for file_name in sorted(file_list):
            if file_name.upper().endswith('.LUA') and file_name.lower() not in blacklist:
                file_path = os.path.join(root, file_name)
                lua_function = []

                with codecs.open(file_path, 'r',"utf-8",errors="replace") as file:
                    try:
                        #logging.debug(file_path)
                        # Remove multiline comments https://stackoverflow.com/a/40454391
                        file_content = file.readlines()

                        file_content = ''.join(file_content)
                        # ignore hangul
                        file_content = file_content.encode("ascii",errors="ignore").decode("ascii")
                        file_content = re.sub(r'--\[(=*)\[(.|\n)*?\]\1\]', '', file_content)

                        lua_function_load(file_content.split('\n'))

                        # Load LUA functions
                        for line in file_content.split('\n'):
                            line = line.strip()
                            line = line.replace('\xef\xbb\xbf', '')  # Remove UTF8-BOM
                            line = line.replace('\{', '\\\\{')  # Fix regex escaping
                            line = line.replace('\}', '\\\\}')  # Fix regex escaping
                            line = re.sub(r'\[\"(\w*?)\"\]', r"['\1']", line)  # Replace double quote with single quote
                            line = re.sub(r'local \w+ = require[ (]["\']\w+["\'][ )]*', '', line)  # Remove require statements
                            line = re.sub(r'function (\w+):(\w+)\((.*)\)', r'function \1.\2(\3)', line)  # Replace function a:b with function a.b

                            if len(line) == 0:
                                continue

                            if bool(re.match(r'(local\s+)?function\s+[\w.:]+\(.*?\)', line)):
                                #if file_name.upper().endswith("ABILITY_UNLOCK.LUA"):
                                #    print(line)

                                lua_function_load(lua_function)
                                lua_function = []

                            lua_function.append(line)

                        lua_function_load(lua_function)

                    except LuaError as error:
                        #if file_name.upper().endswith("CALC_PROPERTY_SKILL.LUA"):
                        #    print("fail")
                        logging.warning('Failed to load %s, error: %s...', file_path, error)
                        continue
def init_runtime():
    global LUA_RUNTIME, LUA_SOURCE

    LUA_RUNTIME = {}
    LUA_SOURCE = {}
    init_runtime_walk(constants.PATH_INPUT_DATA)
    #init_runtime_walk(os.join(constants.PATH_INPUT_DATA_KTOS):

def destroy():
    global lua, LUA_OVERRIDE, LUA_RUNTIME, LUA_SOURCE

    lua = None
    LUA_OVERRIDE = None
    LUA_RUNTIME = None
    LUA_SOURCE = None


def lua_function_load(function_source):
    if len(function_source) == 0:
        return

    function_execute = [line.strip() for line in function_source if not line.startswith('--')]
    function_execute = [re.sub(r'local \w+ = require[ (]["\']\w+["\'][ )]*', '', line) for line in function_execute]
    function_execute = [line.replace('\xef\xbb\xbf', '') for line in function_execute]
    function_execute = [line.replace('\{', '\\\\{')  for line in function_execute]
    function_execute = [line.replace('\}', '\\\\}') for line in function_execute]
    function_execute = '\n'.join(function_execute) + '\n'

    if function_source[0].startswith('function '):
        function_name = lua_function_name(function_source[0])
        #logging.debug(function_name)
        # Ignore any function that was overridden
        if not any(function_name in s for s in LUA_OVERRIDE):
            lua.execute(function_execute)
            #lua.execute(function_source)

            LUA_SOURCE[function_name] = '\n'.join(function_source)
            LUA_RUNTIME[function_name] = lua_function_reference(function_name)
    else:
        #lua.execute(function_execute)
        lua.execute(function_execute)


def lua_function_name(function):
    return function[function.index('function ') + len('function '):function.index('(')].strip()


def lua_function_reference(function_name):
    # In order to return a named LUA function, we need to add a return statement in the end
    # read more: https://github.com/scoder/lupa/issues/22
    return lua.execute('return ' + function_name)


def lua_function_source(function):
    result = []

    for line in function.splitlines():
        line = line.strip()

        # Remove empty lines
        if len(line) == 0:
            continue

        # Remove comment-only lines
        if line.startswith('--'):
            continue

        result.append(line)

    return result


def lua_function_source_format(function_source):
    level = 0
    result = []

    TOKEN_LEVEL_INCREASE = ['else', 'for', 'function', 'if']
    TOKEN_LEVEL_DECREASE = ['end', 'else']

    for line in function_source:

        # insert extra empty lines (to increase readability)
        if line.find('if') == 0:
            result.append('')

        # << indentation
        if any(line.find(s) == 0 for s in TOKEN_LEVEL_DECREASE):
            level = level - 1

        result.append((level * 4) * ' ' + line)

        # >> indentation
        if any(line.find(s) == 0 for s in TOKEN_LEVEL_INCREASE):
            level = level + 1

        # insert extra empty lines (to increase readability)
        if line.find('end') == 0:
            result.append('')

    return result


def lua_function_source_to_javascript(function_source):
    result = []

    for line in lua_function_source_format(function_source):
        if line.strip().startswith('--'):
            continue

        if '^' in line:
            parts = line.split('^')
            for i in range(len(parts)):
                if i == len(parts) - 1:
                    break

                part_left = lua_function_source_to_javascript_argument(parts[i], -1)
                part_right = lua_function_source_to_javascript_argument(parts[i + 1], 1)

                line = line.replace('^', '')
                line = line.replace(part_left, 'Math.pow(' + part_left)
                line = line.replace(part_right, ', ' + part_right + ')')

        line = line + ' {' if line.find('function ') == 0 else line
        line = line.replace('~=', '!=')
        line = line.replace('local ', 'var ')
        line = line.replace('math.', 'Math.')
        line = line.replace(':', '.')
        line = re.sub(r'--(.+)', '', line)
        line = re.sub(r'#(\w+)', r'\1.length', line)
        line = re.sub(r'\band\b', ' && ', line)
        line = re.sub(r'\bor\b', ' || ', line)
        line = re.sub(r'\bend\b', '}', line)
        line = re.sub(r'\belse\b', '} else {', line)
        line = re.sub(r'\belseif\b', '} else if', line)
        line = re.sub(r'\bnil\b', 'null', line)
        line = re.sub(r'{((?:"\w+"[,\s]*)+)}', r'[\1]', line) # arrays
        line = re.sub(r'^(\s*)([^\s]+?),\s*([^\s]+?)\s*=\s*([^\s]+?),\s*([^\s]+?)$', r'\1\2 = \4; \3 = \5;', line) # multiple variable association

        result.append(line)

    result = '\n'.join(result)

    result = re.sub(r'for ([^,]+?)=([^,]+?),([^,]+?),([^,]+?)do', r'for (var \1 = \2; \1 <= \3; \1 += \4) {', result, flags=re.DOTALL)
    result = re.sub(r'for ([^,]+?)=([^,]+?),([^,]+?)do', r'for (var \1 = \2; \1 <= \3; \1 ++) {', result, flags=re.DOTALL)
    result = re.sub(r'if (.+?) then', r'if (\1) {', result, flags=re.DOTALL)
    result = result.splitlines()

    return result


def lua_function_source_to_javascript_argument(text, direction):
    i = 0
    parenthesis = 0
    parenthesis_open = '(' if direction == 1 else ')'
    parenthesis_close = ')' if direction == 1 else '('

    text = text[::-1] if direction == -1 else text
    text = text + ' '  # hotfix: so i never stops at an interesting character

    for i in range(len(text)):
        char = text[i]

        if char in (' ', '\n', parenthesis_close) and i > 0 and parenthesis == 0:
            break

        if char == parenthesis_open:
            parenthesis = parenthesis + 1
        if char == parenthesis_close:
            parenthesis = parenthesis - 1

    return text[:i][::-1] if direction == -1 else text[:i]
