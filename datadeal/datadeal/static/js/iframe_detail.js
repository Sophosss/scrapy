var variable = [];
var v_dict = {};
$('*').click(function(){
    if($(this).children().length == 0){
        var xpath = get_xpath($(this));
        $(this).css('border','3px dotted #000');
        if($.inArray(xpath, variable) == -1){
            variable.push(xpath);
            v_dict[xpath] = $(this);
            parent.set_variable(variable,'detail_table');
        }
    }   
})

function childrenup(xpath) {
    change_xpath = xpath.replace(/danyin/g,'\'');
    var that = v_dict[change_xpath];
    var new_xpath = get_xpath(that.parent());
    if($.inArray(xpath, variable) != -1){
        variable.splice($.inArray(xpath,variable),1);
        that.css('border','');
        that.parent().css('border','3px dotted #000');
        if($.inArray(new_xpath, variable) == -1){
            variable.push(new_xpath);
            v_dict[new_xpath] = that.parent();
            parent.set_variable(variable,'detail_table');
        }
    }
    
}

function del_v(xpath){
    change_xpath = xpath.replace(/danyin/g,'\'');
    var that = v_dict[change_xpath];
    if($.inArray(xpath, variable) != -1){
        variable.splice($.inArray(xpath,variable),1);
        that.css('border','');
    }
}