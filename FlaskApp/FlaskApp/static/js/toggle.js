function toggle(option, category){
    for (i in option){
        $('#' + category + '-'+option[i]).button('toggle');
    }
}