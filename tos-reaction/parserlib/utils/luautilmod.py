import csv
import glob
import os
import re
import codecs
import multiprocessing
from lupa import LuaRuntime, LuaError
import logging
from parserlib.utils import iesutilmod

class luaclass:

    lock=multiprocessing.Lock()
    # HotFix: don't throw errors when LUA is getting an unknown key
    def attr_getter(self,obj, name):
        if name in obj:
            if name in ['Blockable', 'HPCount', 'ReinforceArmor', 'TranscendArmor', 'ReinforceWeapon', 'TranscendWeapon']:
                return int(obj[name])
            else:
                return obj[name]
        return 0


    def attr_setter(self,obj, name, value):
        obj[name] = value



    LUA_RUNTIME = None
    LUA_SOURCE = None

    def __init__(self,constants):
        self.constants=constants
        self.lua = LuaRuntime(attribute_handlers=(self.attr_getter, self.attr_setter),
                              unpack_returned_tuples=True)
        self.ies=iesutilmod.iesclass(constants)
        self.LUA_OVERRIDE = [
            'function GET_ITEM_LEVEL(item) return 0 end',  # We cant emulate this function as geItemTable is undefined
            'function IsBuffApplied(pc, buff) return "NO" end',
            'function GetAbilityAddSpendValue(pc,classname,column) return 0 end',
            #'function GetSkillOwner(skill) return {} end',
            'function IsServerSection(pc) return 0 end',
            'function IsServerObj(pc) return 0 end',
            'function GetExProp(entity, name) return entity[name] or 0 end',
            'function GetExProp_Str(entity, name) return tostring(entity[name]) or nil end',
            'function GetIESID(item) end',
            'function GetItemOwner(item) return {} end',
            'function GetOwner(monster) end',
            'function GetServerNation() end',
            'function GetServerGroupID() end',
            'function IsPVPServer(itemOwner) end',
            'function IsPVPField(pc) return 0 end',

            'function IMCRandom(min, max) return 0 end',
            'function ScpArgMsg(a, b, c) return "" end',
            'function SCR_MON_OWNERITEM_ARMOR_CALC(self, defType) return 0 end',
            'function SetExProp(entity, name, value) entity[name] = value end',
            'function math.pow(value,power) return value ^ power end',
            'function GetZoneName() return "" end',
            "function Weeklyboss_GetNowWeekNum() return nil end",
            "function GetBuffByProp(self,mode,value) return nil end",
            "function IsRaidField(self)return 0 end",
        ]
    def exec_lua_encapsulated(self,cls,context,lua_fn,arg_call):
        self.lock.acquire()
        try:
            func=self.lua.execute(
                "return function(cls,context,fn_str,arg_call) "
                "   LUA_CONTEXT=context\n"
                "   local fn=load(fn_str,fn_str,'t')\n"
                "   local arg_fn=load(arg_call,arg_call,'t') \n"
                "   local _,arg_fn2=assert(pcall(arg_fn))\n"
                "   local _,arg=assert(pcall(arg_fn))\n"
                "   local _,cls_fn=assert(pcall(fn))\n"
                "   local _,retval=assert(pcall(cls_fn,arg))\n"
                "   return result,retval\n"
                "end\n")
            return func(cls,context,lua_fn,arg_call)
        finally:
            pass
            self.lock.release()
    def init(self):
        self.init_global_constants('sharedconst.ies')
        self.init_global_constants('sharedconst_system.ies')
        self.init_global_data()
        self.init_global_functions()
        self.init_runtime()

        pass

    def init_global_constants(self,ies_file_name):
        execute = ''
        ies_path = os.path.join(self.constants.PATH_INPUT_DATA, 'ies.ipf', ies_file_name)

        with codecs.open(ies_path, 'r','utf-8',errors="replace") as ies_file:
            for row in csv.DictReader(ies_file, delimiter=',', quotechar='"'):
                if row['UseInScript'] == 'NO':
                    continue

                execute += row['ClassName'] + ' = ' + row['Value'] + '\n'

        self.lua.execute(execute)

    def ies_add_glob(self,key,pattern):
        for path in glob.glob(pattern,recursive=True):
            self.ies_ADD(key,  self.ies.load(path) )
    def init_global_data(self):
        self.ies_ADD = self.lua.execute('''
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

        self.ies_ADD('ancient', self.ies.load('ancient_info.ies'))
        self.ies_ADD('ancient_info', self.ies.load('ancient_info.ies'))
        self.ies_ADD('item', self.ies.load('item_equip.ies'))
        self.ies_ADD('item', self.ies.load('item_equip_ep12.ies'))
        self.ies_ADD('item', self.ies.load('item_ep12.ies'))
        self.ies_ADD('item', self.ies.load('item_HiddenAbility.ies'))
        self.ies_ADD('item', self.ies.load('item_GuildHousing.ies'))
        self.ies_ADD('item', self.ies.load('item_ep12.ies'))
        self.ies_ADD('item', self.ies.load('item_gem.ies'))
        self.ies_ADD('item', self.ies.load('item_event.ies'))
        self.ies_ADD('item', self.ies.load('item_event_equip.ies'))
        self.ies_ADD('item', self.ies.load('item_ep12.ies'))
        self.ies_ADD('item', self.ies.load('item_premium.ies'))
        self.ies_ADD('item', self.ies.load('item_quest.ies'))
        self.ies_ADD('item_grade', self.ies.load('item_grade.ies'))
        self.ies_ADD('item_growth', self.ies.load('item_growth.ies'))
        self.ies_ADD('HiddenAbility_Reinforce', self.ies.load('HiddenAbility_Reinforce.ies'))

        self.ies_ADD('job', self.ies.load('job.ies'))
        self.ies_ADD('buff', self.ies.load('buff.ies'))
        self.ies_ADD('monster', self.ies.load('monster.ies'))
        self.ies_ADD('monster', self.ies.load('monster_guild.ies'))
        self.ies_ADD('monster', self.ies.load('monster_item_summon.ies'))
        self.ies_ADD('monster', self.ies.load('monster_item.ies'))
        self.ies_ADD('monster', self.ies.load('monster_event.ies'))
        self.ies_ADD('monster', self.ies.load('Monster_solo_dungeon.ies'))
        self.ies_ADD('monster', self.ies.load('monster_Ancient.ies'))
        self.ies_ADD('monster', self.ies.load('monster_mgame.ies'))
        self.ies_ADD('monster', self.ies.load('monster_npc.ies'))
        self.ies_ADD('skill', self.ies.load('skill.ies'))
        self.ies_ADD('SkillRestrict', self.ies.load('SkillRestrict.ies'))
        self.ies_ADD('ability', self.ies.load('ability.ies'))
        self.ies_add_glob("ability",'../ies_ability.ipf/ability_*.ies')
        self.ies_ADD('monster_skill', self.ies.load('monster_skill.ies'))

        self.ies_ADD('stat_monster', self.ies.load('statbase_monster.ies'))
        self.ies_ADD('stat_monster_race', self.ies.load('statbase_monster_race.ies'))
        self.ies_ADD('stat_monster_type', self.ies.load('statbase_monster_type.ies'))


    def init_global_functions(self):

        self.lua.execute("".join((s+"\n" for s in self.LUA_OVERRIDE)))
        self.lua.execute('''
            function setfenv(fn, env)
              local i = 1
              while true do
                local name = debug.getupvalue(fn, i)
                if name == "_ENV" then
                  debug.upvaluejoin(fn, i, (function()
                    return env
                  end), 1)
                  break
                elseif not name then
                  break
                end
            
                i = i + 1
              end
            
              return fn
            end
            app = {
                IsBarrackMode = function() return false end
            }
            
            exchange = {
                GetExchangeItemInfoByGuid = function(guid) end
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
            
            function GetClass(ies_key, name)
                local data = ies_by_ClassName[string.lower(ies_key)]
                return data[name]
            end
            function GetClassByType(ies_key, id)
            print(ies_key)
                local data = ies_by_ClassID[string.lower(ies_key)]
                return data[math.floor(id)]
            end
            
            function GetClassList(ies_key)
                
                local value=ies_by_ClassID[string.lower(ies_key)]
              
                return value,ies_by_ClassIDCount[string.lower(ies_key)]
               
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
            function GetMyJobHistoryString(pc)
                local jobs=LUA_CONTEXT.jobs;
                local jobstr=''
                local first=true
                for k,v in python.iterex(jobs) do
                    
                    local cls=GetClassByType('Job',k)
                    jobstr=jobstr..cls.ClassName
                    if not first then
                        jobstr=";"..jobstr
                    end
                    first=true
                end
                return jobstr
            end
             function GetJobHistoryList(pc)
                local jobs=LUA_CONTEXT.jobs;
                local list={}
                for k,v in python.iterex(jobs) do
                    list[#list+1]=tonumber(k)
                end
                return list
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
            
            function SyncFloor(number)
                return math.floor(number)
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
            function intToString(val)
                return tostring(math.floor(val),0)
            end
            function TryGetProp(item, prop, default)
                if item == nil then
                    return default
                end
                --print(debug.traceback("Stack trace"))
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
            function GetSkillOwner(skill) 
                if LUA_CONTEXT then
                    return LUA_CONTEXT.stats
                else
                    return {}
                end 
            
            end
            function GetClassCount(ies_key)

                return ies_by_ClassIDCount[string.lower(ies_key)]
    
            end
            function GetJobGradeByName(pc, name)
                local cls=GetClass("Job",name)
                local job=LUA_CONTEXT.jobs[intToString(cls.ClassID)]
                if job==nil then
                    return 0
                else
                    return 1
                end
            end
            function GetJobLevelByName(pc, name)
                local cls=GetClass("Job",name)
                local job=LUA_CONTEXT.jobs[intToString(cls.ClassID)]
                if job==nil then
                    return 0
                else
                    return job
                end
            end
            function GetSkill(pc, name)
                local cls=GetClass("Skill",name)
                if cls==nil or LUA_CONTEXT.skills[intToString(cls.ClassID)]==nil then
                    return  nil
                end
                cls.Level=LUA_CONTEXT.skills[intToString(cls.ClassID)]
                    print(""..cls.ClassID.."/"..intToString(cls.Level));
                return cls
            end
            function GetSkillByType(pc, type)
                local cls=GetClassByType("Skill",type)
                if cls==nil or LUA_CONTEXT.skills[intToString(cls.ClassID)]==nil then
                    return nil
                end
                cls.Level=LUA_CONTEXT.skills[intToString(cls.ClassID)]
                print(""..cls.ClassID.."/"..intToString(cls.Level));
                return cls
            end
            function GetAbility(pc, name)
                local cls=GetClass("Ability",name)
                if cls==nil or LUA_CONTEXT.abilities[intToString(cls.ClassID)]==nil then
                    return nil
                end
                cls.Level=LUA_CONTEXT.abilities[intToString(cls.ClassID)]
                return cls
            end

            
        ''' + '\n')


    def init_runtime(self):

        self.LUA_RUNTIME = {}
        self.LUA_SOURCE = {}

        for root, dirs, file_list in os.walk(self.constants.PATH_INPUT_DATA):
            for file_name in sorted(file_list):
                if file_name.upper().endswith('.LUA'):
                    file_path = os.path.join(root, file_name)
                    lua_function = []

                    with codecs.open(file_path, 'r',"utf-8",errors="replace") as file:
                        try:
                            # Remove multiline comments https://stackoverflow.com/a/40454391
                            file_content = file.readlines()

                            file_content = ''.join(file_content)
                            # ignore hangul
                            file_content = file_content.encode("ascii",errors="ignore").decode("ascii")
                            file_content = re.sub(r'--\[(=*)\[(.|\n)*?\]\1\]', '', file_content)
                            self.lua_function_load(file_content.split('\n'))
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
                                    self.lua_function_load(lua_function)
                                    lua_function = []

                                lua_function.append(line)

                            self.lua_function_load(lua_function)

                        except LuaError as error:
                            if file_name.upper().endswith("CALC_PROPERTY_SKILL.LUA"):
                                print("fail")
                            logging.warning('Failed to load %s, error: %s...', file_path, error)
                            continue

    def destroy(self):

        self.lua = None
        self.LUA_OVERRIDE = None
        self.LUA_RUNTIME = None
        self.LUA_SOURCE = None


    def lua_function_load(self,function_source):
        if len(function_source) == 0:
            return

        function_execute = [line.strip() for line in function_source if not line.startswith('--')]
        function_execute = [re.sub(r'local \w+ = require[ (]["\']\w+["\'][ )]*', '', line) for line in function_execute]
        function_execute = [line.replace('\xef\xbb\xbf', '') for line in function_execute]
        function_execute = [line.replace('\{', '\\\\{') for line in function_execute]
        function_execute = [line.replace('\}', '\\\\}') for line in function_execute]
        function_execute = '\n'.join(function_execute) + '\n'

        if function_source[0].startswith('function '):
            function_name = self.lua_function_name(function_source[0])

            # Ignore any function that was overridden
            if not any(function_name in s for s in self.LUA_OVERRIDE):
                self.lua.execute(function_execute)

                self.LUA_SOURCE[function_name] = '\n'.join(function_source)
                self.LUA_RUNTIME[function_name] = self.lua_function_reference(function_name)
        else:
            self.lua.execute(function_execute)


    def lua_function_name(self,function):
        return function[function.index('function ') + len('function '):function.index('(')].strip()


    def lua_function_reference(self,function_name):
        # In order to return a named LUA function, we need to add a return statement in the end
        # read more: https://github.com/scoder/lupa/issues/22
        return self.lua.execute('return ' + function_name)


    def lua_function_source(self,function):
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


    def lua_function_source_format(self,function_source):
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

    #
    # def lua_function_source_to_javascript(self,function_source):
    #     result = []
    #
    #     for line in self.lua_function_source_format(function_source):
    #         if line.strip().startswith('--'):
    #             continue
    #
    #         if '^' in line:
    #             parts = line.split('^')
    #             for i in range(len(parts)):
    #                 if i == len(parts) - 1:
    #                     break
    #
    #                 part_left = self.lua_function_source_to_javascript_argument(parts[i], -1)
    #                 part_right = self.lua_function_source_to_javascript_argument(parts[i + 1], 1)
    #
    #                 line = line.replace('^', '')
    #                 line = line.replace(part_left, 'Math.pow(' + part_left)
    #                 line = line.replace(part_right, ', ' + part_right + ')')
    #
    #         line = line + ' {' if line.find('function ') == 0 else line
    #         line = line.replace('~=', '!=')
    #         line = line.replace('local ', 'var ')
    #         line = line.replace('math.', 'Math.')
    #         line = line.replace(':', '.')
    #         line = re.sub(r'--(.+)', '', line)
    #         line = re.sub(r'#(\w+)', r'\1.length', line)
    #         line = re.sub(r'\band\b', ' && ', line)
    #         line = re.sub(r'\bor\b', ' || ', line)
    #         line = re.sub(r'\bend\b', '}', line)
    #         line = re.sub(r'\belse\b', '} else {', line)
    #         line = re.sub(r'\belseif\b', '} else if', line)
    #         line = re.sub(r'\bnil\b', 'null', line)
    #         line = re.sub(r'{((?:"\w+"[,\s]*)+)}', r'[\1]', line) # arrays
    #         line = re.sub(r'^(\s*)([^\s]+?),\s*([^\s]+?)\s*=\s*([^\s]+?),\s*([^\s]+?)$', r'\1\2 = \4; \3 = \5;', line) # multiple variable association
    #
    #         result.append(line)
    #
    #     result = '\n'.join(result)
    #
    #     result = re.sub(r'for ([^,]+?)=([^,]+?),([^,]+?),([^,]+?)do', r'for (var \1 = \2; \1 <= \3; \1 += \4) {', result, flags=re.DOTALL)
    #     result = re.sub(r'for ([^,]+?)=([^,]+?),([^,]+?)do', r'for (var \1 = \2; \1 <= \3; \1 ++) {', result, flags=re.DOTALL)
    #     result = re.sub(r'if (.+?) then', r'if (\1) {', result, flags=re.DOTALL)
    #     result = result.splitlines()
    #
    #     return result
    #
    #
    # def lua_function_source_to_javascript_argument(self,text, direction):
    #     i = 0
    #     parenthesis = 0
    #     parenthesis_open = '(' if direction == 1 else ')'
    #     parenthesis_close = ')' if direction == 1 else '('
    #
    #     text = text[::-1] if direction == -1 else text
    #     text = text + ' '  # hotfix: so i never stops at an interesting character
    #
    #     for i in range(len(text)):
    #         char = text[i]
    #
    #         if char in (' ', '\n', parenthesis_close) and i > 0 and parenthesis == 0:
    #             break
    #
    #         if char == parenthesis_open:
    #             parenthesis = parenthesis + 1
    #         if char == parenthesis_close:
    #             parenthesis = parenthesis - 1
    #
    #     return text[:i][::-1] if direction == -1 else text[:i]
