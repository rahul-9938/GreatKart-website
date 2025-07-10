// some scripts

// jquery ready start
$(document).ready(function() {
	// jQuery code


    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other

    */ ///////////////////////////////////////
    

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });


    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });



	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if

 
    $('#pay-button').click(function (event) {
    event.preventDefault();
    const amount = $('#amount').val();

    if (!amount || amount <= 0) {
      alert('Please enter a valid amount.');
      return;
    }

    console.log("Amount: ", amount);
    console.log("CSRF Token: ", $('input[name="csrfmiddlewaretoken"]').val());

    // AJAX request to create Razorpay order
    $.ajax({
      url: '/orders/create-order/',
      type: 'POST',
      data: {
        amount: amount,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
      },
      success: function (data) {
        console.log("API Response: ", data);

        const options = {
          key: data.key, // Razorpay API key
          amount: data.amount, // Amount in paisa (e.g., 10000 = ₹100)
          currency: 'INR',
          order_id: data.order_id,
          name: 'GreatKart Payments',
          description: 'Payment for your order',
          handler: function (response) {
            // alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
            console.log("Payment Response: ", response);

            // Verify payment on the server
            $.ajax({
              url: '/orders/verify-payment/',
              type: 'POST',
              data: {
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
              },
              success: function (verificationResponse) {
                console.log("Verification Response:", verificationResponse);
                if (verificationResponse.success) {
                  alert("Payment verified successfully!");
                  window.location.href = '/orders/payment_success/';

                } else {
                  alert("Payment verification failed: " + verificationResponse.error);
                }
              },
              error: function (error) {
                alert("Error verifying payment.");
                console.error(error);
              }
            });
          }
        };

        const rzp = new Razorpay(options);
        rzp.open();
      },
      error: function (error) {
        console.error('Order creation error:', error);
        alert('Error creating order.');
      }
    });
  });




    
}); 
// jquery end


setTimeout(function(){
  $('#message').fadeOut('slow')
}, 4000)