#encoding UTF-8 
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MiSolRNA</title>

    <!-- Bootstrap -->
    <link href="static/css/bootstrap.min.css" rel="stylesheet">

	<!-- Bootstrap theme -->
    <link href="static/css/bootstrap-theme.min.css" rel="stylesheet">


	<!-- Custom styles for this template -->
    <link href="static/css/theme.css" rel="stylesheet">


    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->



<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.8.1/build/fonts/fonts-min.css" /> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.8.1/build/autocomplete/assets/skins/sam/autocomplete.css" /> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/yahoo-dom-event/yahoo-dom-event.js"></script> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/animation/animation-min.js"></script> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/datasource/datasource-min.js"></script> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/autocomplete/autocomplete-min.js"></script>

#if $type=='search'
<script type="text/javascript" src="/${STATIC_URL}/js/toolt.js"></script>
<link rel="stylesheet" type="text/css" href="/${STATIC_URL}/css/autocomp.css" />
#end if

  </head>


#if $type == 'search'
<body class="yui-skin-sam" onload="ocultartodos();">
#else
<body>
#end if


<div class="container theme-showcase" role="main">


 <h1>MiSolRNAdb</h1>


	<ul class="nav nav-tabs" role="tablist">
        	<li class="#if $type=='index' then 'active' else ''#" role="presentation"><a href="/"><span class="glyphicon glyphicon-home"></span> Home</a></li>
        	<li class="#if $type=='search' then 'active' else ''#" role="presentation"><a href="search"><span class="glyphicon glyphicon-search"></span> Search</a></li>
        	<li class="#if $type=='blast' then 'active' else ''#" role="presentation"><a href="blast"><span class="glyphicon glyphicon-certificate"></span> BLAST</a></li>
        	<li class="#if $type=='help' then 'active' else ''#" role="presentation"><a href="help"><span class="glyphicon glyphicon-question-sign"></span> Help</a></li>
        	<li class="#if $type=='about' then 'active' else ''#" role="presentation"><a href="about"><span class="glyphicon glyphicon-paperclip"></span> About us</a></li>
	</ul>