get_test_list();
var test_list = {};

function populate_testlist(test_list){
    var target = document.getElementById("test_table_tbody");
    target.innerHTML='';
    for (test = 0; test < test_list.length; test++){

        var html = '\
        <tr>\
            <td>\
                <a class="text-heading text-primary-hover font-semibold"\
                    href="#">'+test_list[test]['name']+'</a>\
            </td>\
            <td>'+test_list[test]['test_search_id']+'</td>\
            <td>'+test_list[test]['price']+'</td>\
            <td>\
                <a test_pk = '+test_list[test]['id']+' onclick="get_parameter(this)"\
                    class="btn btn-sm btn-square btn-neutral">\
                    <i class="fa-solid fa-right-long fa-beat" style="color: #c01bee;"></i>\
                </a>\
            </td>\
        </tr>\
        '

        target.innerHTML += html;
    }
}

function get_test_list(){
    var url = "/admin_dashboard/test/test_list_ajax";
    axios.get(url)
    .then(function (response) {
        populate_testlist(response.data);
        test_list = response.data;
      })
      .catch(function (error) {
        console.log(error);
      })
}

// ------------------------------------------------------------------ test search ---------------------------------------------------

function test_search(element) {
    var query = element.value;
    var result = [];

    if (query === '') {
        location.reload();
    }
    let obj = test_list;

    for (i = 0; i < obj.length; i++) {
        if (obj[i]['test_search_id'].includes(query)) {
            result.push(obj[i]);
        }
    }
    populate_testlist(result);

}

// ------------------------------------------------ parameter list ---------------------------------


function show_parameter(parameter_list, test_pk){
    var target = document.getElementById("parameter_list");
    target.innerHTML = '';
    document.getElementById('test_uid').value = test_pk;

    for(parameter = 0; parameter <parameter_list.length; parameter++ ){      
        console.log(parameter_list[parameter])  
        var html = '\
        <li class="list-group-item">\
            <input checked name="parameter_name" class="form-check-input me-1" type="checkbox" value="'+parameter_list[parameter]['name']+'" aria-label="...">\
            '+parameter_list[parameter]['name'] +' -- '+ parameter_list[parameter]['unit'] +'\
        </li>\
        '
        target.innerHTML += html;
    }
    
}


function get_parameter(element){
    var test_pk = element.getAttribute("test_pk");
    var url = "/admin_dashboard/test/get_parametr_list/"+test_pk;
    axios.get(url)
    .then(function (response) {

        show_parameter(response.data, test_pk)

      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
}

