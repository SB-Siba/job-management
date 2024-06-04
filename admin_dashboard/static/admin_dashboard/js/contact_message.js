function get_order_detail(element){
    
    var uid = element.getAttribute('uid');
    var url = '/admin_dashboard/order/order_detail/'+uid;

    document.getElementById('order_number').innerHTML = uid;

    axios.get(url)
    .then(function (response) {
        var res_data = response.data;
        console.log(response.data);

        var html1='\
        <p>Order Amount : <span>'+res_data.order_value+'</span></p>\
        <p>Transaction-ID : <span>'+res_data.transaction_id+'</span></p>\
        <p>Payment Status : <span>'+res_data.payment_status+'</span></p>\
        <p>Order Status : <span>'+res_data.order_status+'</span></p>\
        <p>Delivary Charge : <span>'+res_data.coupon+'</span></p>\
        <p>Coupon : <span>'+res_data.coupon+'</span></p>\
        <p>Address : <span>'+res_data.address+'</span></p>\
        '
        document.getElementById('order_details_data').innerHTML = html1;

        // product list 
        var target = document.getElementById('product_list');
        target.innerHTML='';

        for(var pro =0; pro < response.data.products.length; pro++){
            var data = response.data.products[pro];

            var html= '\
            <tr>\
                <th scope="row">'+pro+'</th>\
                <td>'+data['product']['uid']+'</td>\
                <td>'+data['quantity']+'</td>\
                <td>'+data['product']['brand']+'</td>\
            </tr>\
            '
            target.innerHTML+=html;
        }


        var myModal = new bootstrap.Modal(document.getElementById('order_details'));
        myModal.show();
    })
}

function message_detail(element){
    var uid = element.getAttribute('uid');
    var url = '/admin_dashboard/contact_messages/contact_message_detail/'+uid;

    var myModal = new bootstrap.Modal(document.getElementById('contact_message'));
    
    document.getElementById('contact_message_id').innerHTML = uid;

    

    axios.get(url)
    .then(function (response) {
        var data = response.data;
        document.getElementById('contact_message_message').innerHTML=data.message;

        // populating form
        var form = document.getElementById('message_reply_form');
        form.elements['reply'].innerHTML = data.reply;
        form.elements['status'].value = data.status;
        myModal.show();
    })
}

function submit_reply(){
    const formData = {};
    const form = document.getElementById('message_reply_form');
    const inputs = form.querySelectorAll('input, textarea, select');
    var uid = document.getElementById("contact_message_id").innerHTML;
    
    for (let i = 0; i < inputs.length; i++) {
      const input = inputs[i];
      const key = input.name; // Assuming the input elements have the 'name' attribute set
    
      formData[key] = input.value;
    }
    

    var headers= {
        'X-CSRFToken': formData.csrfmiddlewaretoken,
        'Content-Type': 'application/json'
    }
    url= '/admin_dashboard/contact_messages/contact_message_reply/'+uid;

    axios.post(url, data=formData, { headers: headers })
    .then(response => {
        if(response.data === 200){
            var html = '\
            <div  class="alert alert-success">\
              <strong>Success!</strong> Your Reply is Added..\
            </div>\
            '
            document.getElementById('reply_alert').innerHTML = html;
        }
        else{
            for(var i=0; i < response.data.length; i++){
                var html = '\
                    <div  class="alert alert-danger">\
                    '+response.data[i]+'\
                    </div>\
                '
                document.getElementById('reply_alert').innerHTML += html;
            }
        }
    })
    .catch(error => {
        console.error(error); // handle error
    });
}