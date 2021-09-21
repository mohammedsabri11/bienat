$(document).ready(function()
{

$('#ep').change(function(){

   var idd= $(this).val()
//var id = console.log($(this).val());
   $.ajax({
    type: 'GET',
    url: "{%  url 'report-load'  %}",
    data: {"id":idd},
datatype:'json',
    success: function(response){
var k ='<thead class="uu">';



                 k+=   '<th colspan="2">اسم الطالبة</th>';
               k+=   ' <th>نسبة التجويد</th>';
                k+=    ' <th>نسبة النحو</th>';
             k+=       ' <th>نسبة المتشابهات</th>';



  k+= '<th>نسبة المراجعة</th>';



    k+= '<th>نسبة الترتيل</th>';

    k+= '<th>مجموع عدد الاوجة</th>';
   k+= '<th> عدد ايام الحضور</th>';




             k+=    '</thead>';

 k+=  '<tbody>';

//for (i=1;i<response.resu2; i++)
for (res  in response.resu2)
{
var hi3="hi";
var scores_list=response.resu2 [res];
  k+=  '<tr>';

     k+= '<td colspan="2">' + scores_list.name+'</td>';


  k+= '<td>' + scores_list.intonation+'</td>';
                 k+= '<td>' + scores_list.review+'</td>';
   k+= '<td>' + scores_list.reading +'</td>';
     k+= '<td>' + scores_list.memorize+'</td>';

   k+= '<td>' + scores_list.grammer+'</td>';

  k+= '<td>' + scores_list.num_of_faces+'</td>';


k+= '<td>';
     if (scores_list.att == 0 )
     k+= '<span class="label label-danger pull-right">غياب دائم</span>';
 else
   k+= '<span class="label label-warning pull-right">'+ scores_list.att +'</span>';
k+= '</td>';








           k+=  '</tr>';
 }
                k+=  '</tbody>';
               document.getElementById('example1').html(k);
    }

  });

  });
 });

