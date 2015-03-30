
</div>


<div class="container">

<div class="row">
  <div class="col-md-2">

    <a href="http://www.bithosting.pw"><img src="/${STATIC_URL}/imgs/powered_1.png"></a>

  </div>
  <div class="col-md-9"></div>


  <div class="col-md-1">



    <a href="/${STATIC_URL}/rss.xml"><i class="fa fa-rss fa-3x"></i></a>
</div>
</div>




</div>


    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/${STATIC_URL}/js/bootstrap.min.js"></script>

#if $type=='blast'
<script type="text/javascript" src="/${STATIC_URL}/js/blastajax.js"></script>
#end if


#if $type=='search'
<script>

\$( document ).ready(function() {

  \$('#btnbin').on('click', function () {
mostrarsolo1('searchbin');    
  })

  \$('#mirnacb').on('click', function () {
mostrarsolo1('searchmicro');    
  })

  \$('#targetcb').on('click', function () {
mostrarsolo1('searchtarget');    
  })  

  \$('#keywordcb').on('click', function () {
mostrarsolo1('searchkey');    
  })


});



</script>
#end if



<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
var pageTracker = _gat._getTracker("UA-99055-8");
pageTracker._initData();
pageTracker._trackPageview();
</script>



  </body>
</html>
