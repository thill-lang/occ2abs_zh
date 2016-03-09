$(document).ready(function(){

    var init = function(){

        $("#occ-selector").val('');
        $('input[name=sort_options]')[0].checked=true;

    }

    var launch_query = function(){

        occ = $("#occ-selector").val();
        if(occ == ''){ $("#results-table").css({"visibility" : "hidden"});}
        else{ $("#results-table").css({"visibility" : "visible"}); }
        $("#results-table tbody tr").remove();
        search_params = {};
        search_params['occ'] = occ;
        search_params['sort_by'] = $('input[name=sort_options]:checked').val();
        $.ajax({url:'people', data:search_params, datatype:"json"}).done(function(data){ $("#err-msg").html(''); display_people(data);  });

    }

    var display_people = function(data){

        json_data = $.parseJSON(data);

        if(json_data.hasOwnProperty('err_msg')){

            alert("Error: " + json_data['err_msg']);

        }
        else{
            $.each(json_data, function(index, item){
                var name_zh = item["name_zh"]["value"];
                var abstract_zh = item["abstract_zh"]["value"];
                var name_en = item["name_en"]["value"]
                var abstract_en = item["abstract_en"]["value"]
                var tr = $("<tr></tr>");
                $(tr).append("<td class=\"name-zh-simple\">" + name_zh + "</td>");
                $(tr).append("<td class=\"name-en\">" + name_en  + "</td>");
                $(tr).append("<td class=\"abs-zh-simple\">" + abstract_zh + "</td>");
                $(tr).append("<td class=\"abs-en\">" + abstract_en + "</td>");
                $("#results-table tbody").append($(tr));
            })
         }


    }

    var change_sort_order = function(){

        reorder_occ_selector();
        launch_query();

    }

    var reorder_occ_selector = function(){
        /* Sorts the occupation list either by display string (for Chinese) or
           by URL (for English).

           TODO: Hacky. Refactor.
        */
        var current_value = $("#occ-selector").val();
        var sort_preference = $('input[name=sort_options]:checked').val();
        var occ_selector = $("#occ-selector");
        var options = $("#occ-selector option");
        var new_selector = $("<select><select>");
        var sort_array = []
        for (var i = 0; i < options.length; i++){

            if(sort_preference == 'zh'){ sort_array.push($(options[i]).text()); }
            else{ sort_array.push($(options[i]).val()) }

        }

        sort_array.sort();

        for(var i = 0; i < sort_array.length; i++){

            new_option = "";

            if(sort_preference == 'zh'){ new_option = $("#occ-selector option").filter(function(){ return $(this).text() == sort_array[i]}).clone(); }
            else{ new_option = $("#occ-selector option").filter(function(){ return $(this).val() == sort_array[i]}).clone();  }
            $(new_selector).append($(new_option));
        }

        $(occ_selector).replaceWith(new_selector);
        $(new_selector).attr("id", "occ-selector");
        $(new_selector).val(current_value);
        $(new_selector).change(launch_query);
    }

    init();
    $("#occ-selector").change(launch_query);
    $("#sort-selector").change(change_sort_order)

})