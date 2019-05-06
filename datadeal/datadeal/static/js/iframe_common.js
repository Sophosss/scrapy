function get_parent(child,xpath){
    var tag = child.get(0).tagName.toLocaleLowerCase();
    var i = child.index();
    if(child.parent().children().length == 1){
        var tag_name = tag;
    }else{
        var tag_name = tag+'['+(i+1)+']';
    }
    if(child.parent().attr('id')){
        var id = child.parent().attr('id');
        var root_name = child.parent().get(0).tagName.toLocaleLowerCase();
        xpath = '//'+root_name+'[@id=\''+id+'\']/'+tag_name+xpath;
        return xpath;
    }else{
        child = child.parent();
        xpath = '/'+tag_name+xpath;
        if(tag_name=='html'){
            return xpath;
        }else{
            return get_parent(child,xpath);
        } 
    }
}

function get_xpath(that){
    var xpath = '';
    xpath = get_parent(that,xpath);
    return xpath;
}