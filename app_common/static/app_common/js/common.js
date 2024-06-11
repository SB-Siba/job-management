function delete_doctor(element, target_tr){
    
    var url = element.getAttribute('url');
    axios.get(url)
    .then(function (response) {
        document.getElementById(target_tr).style.display = "none";
    })
    .catch(function (error) {
        console.log(error);
    })   
}