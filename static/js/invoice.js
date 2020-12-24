$(document).ready(function(){
    var i=1;
    $("#add_row").click(function(){b=i-1;
        $('#addr'+i).html($('#addr'+b).html()).find('td:first-child').html(i+1);
        $('#tab_logic').append('<tr id="addr'+(i+1)+'"></tr>');
        i++; 
    });
    $("#delete_row").click(function(){
      if(i>1){
    $("#addr"+(i-1)).html('');
    i--;
    }
    calc();
  });
  
  $('#tab_logic tbody').on('keyup change',function(){
    calc();
  });
 
  

});


function calc()
{
  $('#tab_logic tbody tr').each(function(i, element) {
    var html = $(this).html();
    if(html!='')
    {
      var qty = $(this).find('.qty').val();
      var price = $(this).find('.price').val();
      var taxpercent = $(this).find('.taxpercent').val();
      var amountwithouttax = $(this).find('.withoutaxamount').val();
      amountwithouttax = qty*price;
      $(this).find('.withoutaxamount').val(amountwithouttax);
      var tax_amount = (amountwithouttax/100 * taxpercent) ;
     
      $(this).find('.tax_amount').val(tax_amount);
      var total_amount = parseFloat($(this).find('.total_amount').val( (amountwithouttax+tax_amount).toFixed(2)));
      
      var grand_total = 0
      $('.total_amount').each(function() {
        grand_total += parseFloat($(this).val());
      });

      $('#grand_total_amount').val((grand_total).toFixed(2));
    }
    });
}
