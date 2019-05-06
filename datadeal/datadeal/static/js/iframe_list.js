function get_cycle(str1,str2){
    var cut = 0;
    for(i in str1){
        if(str1[i] == '['){
            cut = i;
        }
        if(str1[i] != str2[i]){
            break
        }
    }
    var cycle = str1.substr(0,cut);
    var variable = str2.substr(cut).split('/');
    variable.splice(0,1);
    variable = variable.join('/');
    return [cycle,variable]
}

var choice = [];
var cycle = '';
var v_list = [];
$('*').click(function(){
    if($(this).children().length == 0){
        var xpath = get_xpath($(this));
        choice.push(xpath);
        if(choice.length > 1){
            var array = get_cycle(choice[0],choice[choice.length-1]);
            cycle = array[0];
            parent.set_cycle(cycle);
            var variable = array[1];
            if(variable){
                if($.inArray(variable, v_list) == -1){
                    v_list.push(variable);
                    parent.set_variable(v_list,'list_table');
                }
            }
        }
        $(this).css('border','3px dotted #000');
    }   
})