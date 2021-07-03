

CODE_ETHER_PROP_TOOLTIP='''
return function(obj,arg,arg2)
    local prop_name_list = AETHER_GET_ITEM_PROP_NAME_LIST(session.GetInvItemByGuid(obj.ClassID), tostring(obj.ClassID));
    local inner_prop_count = 0;
    local real_text_all=""
    for i = 1, #prop_name_list do
        local title = prop_name_list[i]["Title"];
        local prop_name = prop_name_list[i]["PropName"];
        local prop_value = prop_name_list[i]["PropValue"];
        local use_operator = prop_name_list[i]["UseOperator"];
        local prop_opt_desc = prop_name_list[i]["OptDesc"];
        if title ~= nil then
            --inner_ctrl_set = property_gbox:CreateOrGetControlSet("tooltip_each_gem_property", title, 0, inner_ypos);
            --local type_text = GET_CHILD_RECURSIVELY(inner_ctrl_set, "type_text", "ui::CRichText");
            --local type_icon = GET_CHILD_RECURSIVELY(inner_ctrl_set, "type_icon", "ui::CPicture");
    
            --tolua.cast(ctrl_set, "ui::CControlSet");
            --local img_name = GET_ICONNAME_BY_WHENEQUIPSTR(ctrl_set, title);
            --type_icon:SetImage(img_name);
            real_text_all=real_text_all.."  "..ClMsg(title)
            inner_prop_count = 0;
            --inner_prop_ypos = type_text:GetHeight() + type_text:GetY();
        else
            --local type_text = GET_CHILD_RECURSIVELY(inner_ctrl_set, "type_text", "ui::CRichText");
            --inner_inner_ctrlset = inner_ctrl_set:CreateOrGetControlSet("tooltip_each_gem_property_each_text", "proptext"..inner_prop_count, 0, inner_prop_ypos);
    
            local real_text = nil;
            if prop_name == "CoolDown" then
                prop_value = prop_value / 1000;
                real_text = ScpArgMsg("CoolDown : {Sec} Sec", "Sec", prop_value);
            elseif prop_name == "OptDesc" then
                real_text = prop_opt_desc;
            else
                if use_operator ~= nil and prop_value > 0 then
                    real_text = ScpArgMsg(prop_name).." : ".."{img green_up_arrow 16 16}"..prop_value;
                else
                    real_text = ScpArgMsg(prop_name).." : ".."{img red_down_arrow 16 16}"..prop_value;
                end
            end
    
            --local prop_text = GET_CHILD_RECURSIVELY(inner_inner_ctrlset, "prop_text", "ui::CRichText");
            if prop_name == "OptDesc" then real_text = prop_opt_desc; end
            --prop_text:SetText(real_text);
            inner_prop_count = inner_prop_count + 1;
            real_text_all=real_text_all..real_text
            --tolua.cast(inner_ctrl_set, "ui::CControlSet");
            --local bottom_margin = inner_ctrl_set:GetUserConfig("BOTTOM_MARGIN");
            --if bottom_margin == "None" then bottom_margin = 10; end
    
            --inner_prop_ypos = inner_inner_ctrlset:GetY() + inner_inner_ctrlset:GetHeight();
            --inner_ctrl_set:Resize(inner_ctrl_set:GetOriginalWidth(), inner_inner_ctrlset:GetY() + inner_inner_ctrlset:GetHeight() + bottom_margin);
            --inner_ypos = inner_ctrl_set:GetY() + inner_ctrl_set:GetHeight();
        end
    end
    
    return real_text_all
end

'''