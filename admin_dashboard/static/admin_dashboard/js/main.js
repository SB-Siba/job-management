// *************************************************************test parameter*******************************************
// delete test prameter

function delete_test_parameter(element, target_tr){
    
    var url = element.getAttribute('url');
    axios.get(url)
    .then(function (response) {
        document.getElementById(target_tr).style.display = "none";
    })
    .catch(function (error) {
        console.log(error);
    })   
}

//  add formula to test

function formula_click(element){
    parameter_name = element.getAttribute('parameter_name')
    parameter_id = element.getAttribute('parameter_id')
    document.getElementById('add_formula_h4').innerHTML = parameter_name + '('+parameter_id+')';
    document.getElementById('add_formula_parameter_name').value = parameter_name;
    document.getElementById('add_formula_button').type = "submit";
    
}

function formula_see(element){
    
    var parameter_name = element.getAttribute("parameter_name");
    var formula = element.getAttribute("formula");
    alert(formula);
 }

function add_formula_var(){
    var element = document.getElementById('parameter_formula_data');

    var formula_data = element.value;
    element.value = formula_data+'{parameter_id}';
    


}


// user manage

function change_user_password(element){
    var user_id = element.getAttribute("user_id");
    var myModal = new bootstrap.Modal(document.getElementById('change__user_password')); //modal id
    document.getElementById("password_change_user_id").value = user_id;
    myModal.show()

    
}

function user_active_inactive(element){
    var user_id = element.getAttribute("user_id");
    var url= "/admin_dashboard/credential/change_user_status" +'?user_id='+user_id
    axios.get(url)
    .then(function (response) {
        console.log(response.data);
        if (response.data === true){
            element = element.checked;
        }
        else{
            element.checked = false;
        }
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })

    
}